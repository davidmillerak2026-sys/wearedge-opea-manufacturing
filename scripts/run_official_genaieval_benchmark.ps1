# SPDX-License-Identifier: MIT

param(
  [string]$GenAIEvalDir = "C:\tmp\GenAIEval",
  [string]$BenchmarkYaml = "evals\genaieval\official_wearedge_benchmark.yaml",
  [string]$TokenizerModel = "bert-base-uncased",
  [switch]$InstallDeps
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$sourceYaml = Join-Path $repoRoot $BenchmarkYaml

if (-not (Test-Path -LiteralPath $sourceYaml)) {
  throw "Benchmark YAML not found: $sourceYaml"
}

if (-not (Test-Path -LiteralPath $GenAIEvalDir)) {
  git clone --depth 1 https://github.com/opea-project/GenAIEval.git $GenAIEvalDir
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $GenAIEvalDir)) {
    throw "Unable to clone official GenAIEval repository into $GenAIEvalDir"
  }
}

$benchmarkDir = Join-Path $GenAIEvalDir "evals\benchmark"
if (-not (Test-Path -LiteralPath $benchmarkDir)) {
  throw "Official GenAIEval benchmark directory not found: $benchmarkDir"
}

if ($env:OS -eq "Windows_NT") {
  $loadTestPy = Join-Path $benchmarkDir "stresscli\commands\load_test.py"
  if (Test-Path -LiteralPath $loadTestPy) {
    $loadTestSource = Get-Content -LiteralPath $loadTestPy -Raw
    $processesPattern = '(?m)^\s*"--processes",\r?\n\s*str\(runspec\["processes"\]\),\r?\n'
    if ($loadTestSource -match $processesPattern) {
      $loadTestSource = [regex]::Replace($loadTestSource, $processesPattern, "")
      Set-Content -LiteralPath $loadTestPy -Value $loadTestSource -NoNewline
      Write-Host "[WearEdge] Applied Windows Locust compatibility patch: removed --processes from local GenAIEval stresscli."
    }
  }
}

$targetYaml = Join-Path $benchmarkDir "official_wearedge_benchmark.yaml"
Copy-Item -LiteralPath $sourceYaml -Destination $targetYaml -Force

if ($InstallDeps) {
  Push-Location $GenAIEvalDir
  try {
    python -m pip install -r requirements.txt
    python -m pip install opea-eval
  } finally {
    Pop-Location
  }
}

Push-Location $benchmarkDir
try {
  $env:PYTHONIOENCODING = "utf-8"
  if (-not $env:MODEL_NAME) {
    $env:MODEL_NAME = $TokenizerModel
  }
  $tokenizerProbe = "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained(r'$TokenizerModel', local_files_only=True)"
  python -c $tokenizerProbe
  if ($LASTEXITCODE -ne 0) {
    Write-Host "[WearEdge] Tokenizer '$TokenizerModel' is not cached; attempting one online download before benchmark."
    $tokenizerFetch = "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained(r'$TokenizerModel')"
    python -c $tokenizerFetch
    if ($LASTEXITCODE -ne 0) {
      throw "Tokenizer '$TokenizerModel' is unavailable. Choose a public/cached tokenizer with -TokenizerModel."
    }
  }
  $env:TRANSFORMERS_OFFLINE = "1"
  $env:HF_HUB_OFFLINE = "1"
  $beforeRun = Get-Date
  python benchmark.py --yaml official_wearedge_benchmark.yaml
  if ($LASTEXITCODE -ne 0) {
    throw "Official GenAIEval benchmark failed with exit code $LASTEXITCODE"
  }
  $outputRoot = Join-Path $benchmarkDir "benchmark_output\wearedge"
  $latestRun = Get-ChildItem -LiteralPath $outputRoot -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -ge $beforeRun.AddSeconds(-5) } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  if ($latestRun) {
    $failure = Get-ChildItem -LiteralPath $latestRun.FullName -Filter "*_output.log" -ErrorAction SilentlyContinue |
      Select-String -Pattern "Traceback|ModuleNotFoundError|GatedRepoError|Cannot access gated repo|Failed with request|is not supported in Windows" |
      Select-Object -First 1
    if ($failure) {
      throw "Official GenAIEval benchmark produced an internal failure in $($latestRun.FullName): $($failure.Line.Trim())"
    }
    $statsFiles = Get-ChildItem -LiteralPath $latestRun.FullName -Filter "*_stats.csv" -ErrorAction SilentlyContinue
    if (-not $statsFiles) {
      throw "Official GenAIEval benchmark did not produce Locust stats CSV files in $($latestRun.FullName)"
    }
    Write-Host "[WearEdge] Official GenAIEval output: $($latestRun.FullName)"
  }
} finally {
  Pop-Location
}
