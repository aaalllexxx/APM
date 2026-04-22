$apmHome = Join-Path $env:APPDATA "apm"
$apmPython = Join-Path $apmHome "venv\Scripts\python.exe"
$apmMain = Join-Path $apmHome "apm.py"

if (Test-Path $apmPython) {
    & $apmPython $apmMain @args
} else {
    python $apmMain @args
}

$tmpFile = "$env:TEMP\apm_goto.tmp"

if (Test-Path $tmpFile) {
    $apmGotoPath = [System.IO.File]::ReadAllText(
        $tmpFile,
        [System.Text.Encoding]::GetEncoding([System.Globalization.CultureInfo]::CurrentCulture.TextInfo.OEMCodePage)
    ).Trim()

    Remove-Item $tmpFile
    Set-Location -Path $apmGotoPath
}
