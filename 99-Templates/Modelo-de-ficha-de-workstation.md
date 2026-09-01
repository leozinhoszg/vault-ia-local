# Modelo de ficha de workstation

<!-- validador: sem-referencias: template vazio; cada ficha preenchida carrega as próprias fontes -->

Use este template para cada máquina candidata (mini-PC com superchip, PC com GPU discreta, Mac, servidor). A ficha alimenta a tabela e a matriz de [[03-Hardware/Comparativo-workstations-vs-GPU]]. Sem data, fonte e preço datado, a linha não entra na comparação.

## Template obrigatório

| Campo | Valor |
|---|---|
| Nome exato / SKU | A preencher |
| Fabricante / URL da página | A preencher |
| Data de verificação | AAAA-MM-DD |
| Classe no vault | Uma das linhas de [[03-Hardware/Sizing-9B-14B-27B-70B]] (ex.: "GPU 24 GB VRAM + 64 GB RAM", "128 GB unificados") |
| CPU | Núcleos, arquitetura (x86/ARM) |
| Acelerador | GPU/NPU, arquitetura, geração de Tensor Cores |
| Memória do acelerador | Capacidade, tipo, dedicada ou unificada |
| Largura de banda | GB/s, com fonte (é o que limita o decode) |
| RAM do sistema | Capacidade e tipo (se separada da memória do acelerador) |
| Armazenamento | Capacidade, interface |
| Rede / expansão | Portas, PCIe, possibilidade de segunda GPU ou segunda unidade |
| Energia | TGP/TDP ou consumo de sistema declarado; fonte |
| Sistema operacional / stack | Windows, Linux (x86_64 ou aarch64), macOS; CUDA, Metal, ROCm |
| Preço datado | R$ à vista, vendedor, URL e data; "não publicado" se for o caso |
| Alegações do fabricante | O que o marketing promete (ex.: "até 200B") e em que precisão |
| Modelos viáveis em modo 1 | Lista com arquivo quantizado real e GB, conforme [[02-Modelos/Local-real-vs-cloud]] |
| Modelos em modo 2 | Os que só rodam com offload |
| Teto de decode por banda | `banda_GB/s ÷ GB_lidos_por_token`; rotular como triagem |
| Velocidade medida | tokens/s, TTFT, modelo, contexto, runtime e versão — ou "não medido" |
| Incógnitas | O que ainda precisa ser confirmado antes da compra |
| Estado | Candidata, cotada, comprada, descartada |
| Dono da ficha | Pessoa |
| Próxima revisão | Data |

## Regras

1. Registrar a banda de memória com fonte do fabricante ou de base técnica reconhecida; sem banda, não há estimativa de decode.
2. Separar **capacidade** (o que cabe) de **velocidade** (quantos tokens/s); a matriz do comparativo usa os dois.
3. Em memória unificada, descontar sistema operacional, RAG e aplicações antes de alocar ao LLM (regra de [[03-Hardware/Mac-Studio-e-IA-local]]).
4. Preço sem data e sem URL é opinião, não fato; a regra é a mesma de [[03-Hardware/BOM-brasileira-datada]].
5. Alegação de fabricante ("suporta X bilhões de parâmetros") entra no campo próprio e nunca na coluna de modelos viáveis.
