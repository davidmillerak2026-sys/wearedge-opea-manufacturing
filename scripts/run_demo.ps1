$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $root "src"

$python = Get-Command python -ErrorAction SilentlyContinue
$condaPython = Join-Path $HOME "anaconda3\python.exe"
$localPython = Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"
if ($python) {
  & $python.Source -m wear_edge_opea.run_demo
} elseif (Test-Path $condaPython) {
  & $condaPython -m wear_edge_opea.run_demo
} elseif (Test-Path $localPython) {
  & $localPython -m wear_edge_opea.run_demo
} else {
  py -3 -m wear_edge_opea.run_demo
}
