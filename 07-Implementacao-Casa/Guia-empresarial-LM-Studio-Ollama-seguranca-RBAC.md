# LM Studio e Ollama em empresa — segurança, auditoria e RBAC

**Estado:** `draft` até teste em ambiente corporativo. **Data:** 2026-09-02. **Escopo:** serving local de modelos, APIs compatíveis com OpenAI, RAG e agentes. Este guia não transforma LM Studio ou Ollama isoladamente em uma plataforma completa de IAM; o controle corporativo deve ser colocado em uma camada de acesso, gateway e observabilidade.

## 1. Princípio arquitetural

A regra mais importante é **não expor diretamente** a porta do LM Studio ou do Ollama para a rede corporativa, muito menos para a Internet. O Ollama escuta em `127.0.0.1:11434` por padrão e pode ser alterado por `OLLAMA_HOST` [1]. O LM Studio oferece tokens de API e autenticação no servidor [2], mas isso não substitui identidade corporativa, RBAC, rate limit, auditoria e gestão de ciclo de vida.

A topologia recomendada é: usuário ou aplicação autenticada; proxy/gateway corporativo; serviço de autorização; pool de inferência; armazenamento de modelos somente leitura; observabilidade; e cofre de segredos. O gateway termina TLS, valida OIDC/OAuth2, aplica RBAC/ABAC, registra o request sem conteúdo sensível por padrão e encaminha para um backend privado. O backend fica em uma sub-rede sem entrada direta de usuários.

```text
Usuário/App
   |
   | TLS + OIDC/OAuth2 + RBAC + rate limit + auditoria
   v
API Gateway / Reverse Proxy / WAF
   |
   | rede privada, mTLS opcional, allowlist de modelos
   +--> LM Studio Server (host privado)
   +--> Ollama (127.0.0.1 ou VLAN privada)
   +--> vLLM/TensorRT-LLM (produção de maior throughput)
   |
   +--> logs, métricas, traces, SIEM
   +--> registry de modelos + hash + licença + aprovação
```

## 2. Modelo de ameaças

Os riscos principais são exposição de uma API sem autenticação, carregamento de modelo malicioso ou adulterado, vazamento de prompts e documentos, abuso de contexto para consumo excessivo, execução de ferramentas por agentes, acesso lateral ao host, logs contendo dados pessoais e impossibilidade de atribuir uma chamada a um usuário.

O modelo de ameaça deve incluir também o cliente local. Uma estação com LM Studio ou Ollama pode ter usuários com privilégios administrativos, diretórios de modelos graváveis e processos que aceitam conexões da rede local. Em empresa, o endpoint deve ser tratado como um serviço controlado, não como uma aplicação desktop informal.

## 3. Controles mínimos obrigatórios

| Controle | LM Studio | Ollama | Evidência exigida |
|---|---|---|---|
| Bind local por padrão | Manter servidor em loopback quando possível | Manter `127.0.0.1:11434`; não usar `0.0.0.0` sem firewall/gateway | Configuração exportada e teste de porta |
| TLS | Terminar no gateway; usar mTLS em alto risco | Terminar no gateway; backend privado | Certificado, cipher policy e teste TLS |
| Autenticação | Ativar Require Authentication e tokens do servidor [2] | Colocar gateway com OIDC/API key; não presumir RBAC nativo | Request negado sem credencial |
| RBAC | Mapear grupos para modelos/rotas no gateway | Mapear grupos no gateway | Matriz usuário-grupo-ação |
| Autorização de modelo | Allowlist por rota e tamanho | Allowlist por nome/tag; impedir pulls arbitrários | Registro de aprovação |
| Auditoria | Request ID, sujeito, modelo, latência, tokens e resultado | Mesmos campos no gateway; logs nativos não bastam | Evento no SIEM |
| Segredos | Token por aplicação, rotação e cofre | Segredos no gateway/cofre | Rotação testada |
| Rede | VLAN/sub-rede privada e egress controlado | Mesmo controle; porta 11434 não pública | Firewall e scan autorizado |
| Dependências | Atualização assinada/testada | Atualização de runtime, imagens e modelos | SBOM, versão e changelog |
| Dados | Redação, retenção curta e classificação | Redação, retenção curta e classificação | Política de logs e DLP |
| Continuidade | Imagem/configuração versionada | Model registry e configuração versionada | Backup e restauração testados |

## 4. Configuração do LM Studio

No LM Studio, habilitar o servidor apenas quando necessário e preferir escuta local. Em **Developer/Server Settings**, ativar autenticação, criar tokens separados por aplicação e apagar tokens antigos. O token deve ser enviado no cabeçalho `Authorization: Bearer <token>` conforme a documentação da API [2]. Nunca colocar o token em repositório, prompt, log ou variável exposta em frontend.

Para uso empresarial, não distribuir uma configuração manual por usuário. Criar uma imagem ou procedimento corporativo com versão aprovada, diretório de modelos somente leitura, política de atualização, lista de modelos aprovados e configuração do gateway. O LM Studio local pode ser usado como estação de desenvolvimento; o serving compartilhado deve preferir uma camada de API corporativa e, para produção de maior escala, um engine de serving validado.

O gateway deve verificar o usuário antes de encaminhar a chamada. O backend não deve confiar em um campo `user` enviado no JSON pelo cliente. O sujeito deve vir do token OIDC validado. O log mínimo deve guardar `request_id`, `subject_hash`, grupo/tenant, rota, modelo aprovado, versão/hash do modelo, timestamp, duração, tokens de entrada/saída, status e motivo de bloqueio. O conteúdo integral do prompt só deve ser armazenado com base legal, necessidade operacional e retenção definida.

## 5. Configuração do Ollama

Ollama é simples para uso local, mas a API não deve ser tratada como um serviço empresarial completo por padrão. A FAQ oficial informa o bind padrão em `127.0.0.1:11434` e a possibilidade de alterar o endereço com `OLLAMA_HOST` [1]. Portanto, não definir `OLLAMA_HOST=0.0.0.0:11434` sem uma arquitetura de rede, firewall e gateway que imponham autenticação.

Para uma instalação Linux, o serviço deve usar uma conta sem privilégios, um diretório de modelos com permissões restritas, firewall bloqueando a porta direta e egress limitado ao registry permitido. O gateway pode expor somente `/v1/*` ou rotas explicitamente necessárias, com autenticação, autorização, rate limit e limite de tamanho de request. O endpoint administrativo e a capacidade de baixar modelos devem ficar restritos a uma rota de operação separada.

As tags do Ollama devem ser fixadas e registradas. Um nome como `modelo:latest` não é uma política de reprodutibilidade. O catálogo interno deve registrar nome, tag, digest quando disponível, fonte, licença, quantização, template, data de aprovação e resultado de avaliação. Pull de modelo em produção deve passar pelo registry corporativo; o host de inferência não deve ter liberdade de baixar qualquer artefato da Internet.

## 6. RBAC recomendado

| Papel | Pode consultar | Pode executar | Pode baixar/carregar | Pode administrar |
|---|---|---|---|---|
| Leitor | Modelos aprovados | Não | Não | Não |
| Usuário | Modelos aprovados do seu grupo | Rotas autorizadas | Não | Não |
| Desenvolvedor | Modelos de desenvolvimento | Sandbox própria | Modelos aprovados em sandbox | Não |
| Operador | Status e métricas | Testes operacionais | Registry aprovado | Reiniciar/rollback |
| Curador de modelos | Cards, licenças, avaliações | Testes | Importar para staging | Aprovar promoção |
| Auditor | Logs, versões e evidências | Read-only | Não | Não |
| Administrador | Tudo conforme segregação | Sim | Sim | Sim, com MFA e registro |

Para multi-tenant, não confiar apenas no nome do modelo. O gateway deve associar sujeito, tenant, rota, quota e política de dados. O armazenamento de prompts, documentos RAG, embeddings e logs deve respeitar a mesma fronteira de tenant. Agentes que podem chamar ferramentas devem ter uma política ainda mais restrita, com allowlist de ferramentas, escopo de parâmetros, confirmação humana para efeitos externos e timeout.

## 7. Auditoria e observabilidade

A auditoria deve responder quem chamou, qual modelo e versão foram usados, de onde veio a chamada, quais controles foram aplicados, quanto tempo levou, quantos tokens consumiu e se houve bloqueio. O evento de auditoria não deve registrar segredos nem conteúdo integral por padrão.

| Evento | Campos mínimos |
|---|---|
| Inferência | `request_id`, sujeito, tenant, modelo, digest, rota, timestamp, latência, tokens, status |
| Download | sujeito, modelo, fonte, URL, hash, licença, aprovação, destino |
| Alteração de configuração | sujeito, mudança, antes/depois, justificativa, aprovação |
| Falha de política | sujeito, regra, rota, payload reduzido, decisão |
| Ferramenta de agente | sujeito, ferramenta, parâmetros redigidos, aprovação, resultado |
| Incidente | alerta, severidade, host, containment, timeline e responsável |

Enviar logs estruturados para SIEM, métricas para Prometheus/OpenTelemetry e alertas para comportamento anômalo: aumento de tokens, chamadas fora do horário, tentativa de modelo não aprovado, repetição de prompts, erro de autenticação, download fora do registry e crescimento de latência/memória.

## 8. Dados, LGPD e retenção

Classificar os dados antes de permitir que sejam enviados ao modelo. Dados públicos, internos, confidenciais e altamente restritos devem ter rotas e modelos diferentes. PII, segredos, chaves, dados de saúde e documentos regulados devem ser bloqueados, mascarados ou processados em uma zona autorizada. A solução local reduz transferência para terceiros, mas não elimina riscos de acesso interno, logs, backups e operadores.

Definir retenção por tipo de evento. Logs de segurança podem exigir retenção maior que prompts; prompts e respostas devem ter retenção mínima necessária. O controlador deve documentar finalidade, base legal, responsáveis, direitos do titular e procedimento de eliminação quando aplicável. Este guia não constitui parecer jurídico.

## 9. Testes de aceitação

Antes de liberar o serviço, testar que uma chamada sem credencial retorna 401/403, que um usuário de grupo A não acessa o modelo do grupo B, que a porta do backend não é acessível da rede de usuário, que o gateway redige segredos, que cada chamada gera um evento no SIEM e que quotas impedem consumo ilimitado.

Testar também rollback para a versão anterior do modelo, restauração do registry, revogação de token, expiração de sessão, bloqueio de pull externo, execução de prompt injection em RAG, chamada de ferramenta não autorizada, overflow de contexto, arquivo PDF hostil e interrupção do backend. O resultado deve ser arquivado como evidência com data, versão e responsável.

## 10. Quando não usar LM Studio/Ollama isoladamente

LM Studio e Ollama são excelentes para desenvolvimento, laboratório, desktop e serviços pessoais. Em produção empresarial com múltiplos usuários, SSO, quotas, tenants, HA, auditoria formal e SLO, eles devem ficar atrás de um gateway ou ser substituídos por uma camada de serving que ofereça os controles necessários. O backend de inferência não deve ser confundido com IAM.

Para uma empresa pequena, uma arquitetura mínima viável é gateway com OIDC, serviço em host privado, allowlist de modelos, logs estruturados, backup de configuração e RBAC de quatro papéis. Para uma empresa regulada, acrescentar mTLS, SIEM, DLP, cofre de segredos, segregação de ambientes, aprovação de modelos, HA, resposta a incidentes e revisão periódica baseada no NIST AI RMF para IA generativa [3].

## Referências

[1]: https://docs.ollama.com/faq "Ollama FAQ — bind padrão e configuração OLLAMA_HOST"
[2]: https://lmstudio.ai/docs/developer/core/authentication "LM Studio — autenticação e tokens de API"
[3]: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence "NIST — AI RMF Generative AI Profile"
[4]: https://lmstudio.ai/docs/developer/rest/quickstart "LM Studio — API REST e cabeçalho de autorização"
