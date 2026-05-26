$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $root "src"

& "C:\Users\ryan hui\anaconda3\python.exe" -m wear_edge_opea.run_demo

