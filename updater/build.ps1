param(
    [string]$Configuration = "Release",
    [string]$Output = "$(Join-Path $PSScriptRoot 'publish')"
)

$ErrorActionPreference = "Stop"
dotnet publish (Join-Path $PSScriptRoot "Actualizador.csproj") `
    --configuration $Configuration `
    --runtime win-x64 `
    --self-contained true `
    --property:PublishSingleFile=true `
    --property:IncludeNativeLibrariesForSelfExtract=true `
    --output $Output

Write-Host "Actualizador generado en: $Output"
