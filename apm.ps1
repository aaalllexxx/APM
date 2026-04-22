$apmDir = Join-Path $env:APPDATA 'apm'
$venvPython = Join-Path $apmDir 'venv\Scripts\python.exe'
$runnerPython = if (Test-Path $venvPython) { $venvPython } else { 'python' }

& $runnerPython (Join-Path $apmDir 'apm.py') @args
$exitCode = $LASTEXITCODE

$tmpFile = Join-Path $env:TEMP 'apm_goto.tmp'

if (Test-Path $tmpFile) {
    $encoding = [System.Text.Encoding]::GetEncoding([System.Globalization.CultureInfo]::CurrentCulture.TextInfo.OEMCodePage)
    $apmGotoPath = [System.IO.File]::ReadAllText($tmpFile, $encoding).Trim()

    Remove-Item $tmpFile -ErrorAction SilentlyContinue

    if ($apmGotoPath) {
        Set-Location -Path $apmGotoPath
    }
}

exit $exitCode
