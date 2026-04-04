param(
    [string]$Source,
    [string]$OutputName
)
$leafName = Split-Path $OutputName -Leaf
$tmpDir = Join-Path ([System.IO.Path]::GetTempPath()) $leafName
Copy-Item -Path $Source -Destination $tmpDir -Recurse -Force
Compress-Archive -Path $tmpDir -DestinationPath "$OutputName.zip" -Force
Remove-Item $tmpDir -Recurse -Force