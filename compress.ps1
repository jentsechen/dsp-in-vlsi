param(
    [string]$Source,
    [string]$OutputName
)
Compress-Archive -Path $Source -DestinationPath "$OutputName.zip" -Force