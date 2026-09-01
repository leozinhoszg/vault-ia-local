# Recalcula a planilha TCO via Excel (COM), garante tabelas estruturadas e salva com valores em cache.
# Uso: powershell -ExecutionPolicy Bypass -File 99-Templates/recalcular_tco.ps1
$ErrorActionPreference = 'Stop'
$path = (Resolve-Path (Join-Path $PSScriptRoot '..\09-Servicos-e-Custos\TCO-local-vs-OpenAI.xlsx')).Path
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false; $excel.DisplayAlerts = $false
try {
  $wb = $excel.Workbooks.Open($path)
  $tables = @{
    'Premissas'   = @('tPremissas', 'A1:D26');
    'API_OpenAI'  = @('tAPI', 'A1:G4');
    'Local'       = @('tLocal', 'A1:C11');
    'Break_even'  = @('tBreakEven', 'A1:H4');
    'Checks'      = @('tChecks', 'A1:F11')
  }
  foreach ($name in $tables.Keys) {
    $ws = $wb.Worksheets.Item($name)
    if ($ws.AutoFilterMode) { $ws.AutoFilterMode = $false }
    foreach ($lo in @($ws.ListObjects)) { $lo.Unlist() }
    $lo = $ws.ListObjects.Add(1, $ws.Range($tables[$name][1]), $null, 1)
    $lo.Name = $tables[$name][0]; $lo.TableStyle = 'TableStyleMedium2'
  }
  $ws = $wb.Worksheets.Item('Sensibilidade')
  if ($ws.AutoFilterMode) { $ws.AutoFilterMode = $false }
  foreach ($lo in @($ws.ListObjects)) { $lo.Unlist() }
  $blocks = @(@('tSensCambio','A1:H6'), @('tSensVidaUtil','A8:F11'), @('tSensUtilizacao','A13:F17'), @('tSensTarifa','A19:F24'))
  foreach ($b in $blocks) { $lo = $ws.ListObjects.Add(1, $ws.Range($b[1]), $null, 1); $lo.Name = $b[0]; $lo.TableStyle = 'TableStyleMedium2' }
  $excel.CalculateFullRebuild()
  $status = $wb.Worksheets.Item('Checks').Range('E11').Text
  Write-Output ("Local!C7 = " + $wb.Worksheets.Item('Local').Range('C7').Value2)
  Write-Output ("Break_even!E2:E4 = " + (($wb.Worksheets.Item('Break_even').Range('E2:E4').Value2 | ForEach-Object { [math]::Round($_, 2) }) -join ', '))
  Write-Output ("Checks!STATUS GERAL = " + $status)
  $wb.Save(); $wb.Close($false)
} finally {
  $excel.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
}
