[CmdletBinding()]
param(
    [ValidatePattern('^\d+\.\d+\.\d+$')]
    [string] $Version = '1.0.0'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$env:PYTHONUTF8 = '1'


$ScriptDirectory = Split-Path `
    -Parent `
    $MyInvocation.MyCommand.Path

$ProjectDirectory = (
    Resolve-Path (
        Join-Path `
            $ScriptDirectory `
            '..\..'
    )
).Path


$RequirementsFile = Join-Path `
    $ScriptDirectory `
    'requirements.txt'

$SpecFile = Join-Path `
    $ScriptDirectory `
    'LedgerFlow.windows.spec'

$IconGenerator = Join-Path `
    $ScriptDirectory `
    'create_icon.py'

$SourceIcon = Join-Path `
    $ProjectDirectory `
    'assets\ledgerflow.png'


$WindowsBuildDirectory = Join-Path `
    $ProjectDirectory `
    'build\windows'

$PyInstallerWorkDirectory = Join-Path `
    $ProjectDirectory `
    'build\pyinstaller-windows'

$DistributionDirectory = Join-Path `
    $ProjectDirectory `
    'dist\windows'

$ApplicationDistributionDirectory = Join-Path `
    $DistributionDirectory `
    'LedgerFlow'


$PackageName = (
    "LedgerFlow-{0}-windows-x86_64" -f $Version
)

$PackageStageDirectory = Join-Path `
    $ProjectDirectory `
    'build\windows-package'

$PackageDirectory = Join-Path `
    $PackageStageDirectory `
    $PackageName


$ReleaseDirectory = Join-Path `
    $ProjectDirectory `
    'release'

$OutputZip = Join-Path `
    $ReleaseDirectory `
    "$PackageName.zip"


$RequiredFiles = @(
    $RequirementsFile
    $SpecFile
    $IconGenerator
    $SourceIcon
    (
        Join-Path `
            $ProjectDirectory `
            'main.py'
    )
)


foreach ($RequiredFile in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $RequiredFile)) {
        throw "Required file not found: $RequiredFile"
    }
}


Write-Host ""
Write-Host "Building LedgerFlow $Version for Windows x64..."
Write-Host ""


# ---------------------------------------------------------
# Prepare directories
# ---------------------------------------------------------

New-Item `
    -ItemType Directory `
    -Force `
    -Path $WindowsBuildDirectory `
    | Out-Null

New-Item `
    -ItemType Directory `
    -Force `
    -Path $ReleaseDirectory `
    | Out-Null


# ---------------------------------------------------------
# Install dependencies
# ---------------------------------------------------------

Write-Host "Installing Windows build dependencies..."

& python `
    -m pip `
    install `
    --disable-pip-version-check `
    --requirement $RequirementsFile

if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}


# ---------------------------------------------------------
# Validate imports
# ---------------------------------------------------------

Write-Host "Validating Python imports..."

& python `
    -c `
    "import tkinter; import openpyxl; import platformdirs; import main; print('Imports validated successfully.')"

if ($LASTEXITCODE -ne 0) {
    throw "Python import validation failed."
}


# ---------------------------------------------------------
# Generate Windows icon
# ---------------------------------------------------------

$GeneratedIcon = Join-Path `
    $WindowsBuildDirectory `
    'ledgerflow.ico'

Write-Host "Generating Windows icon..."

& python `
    $IconGenerator `
    --source $SourceIcon `
    --output $GeneratedIcon

if ($LASTEXITCODE -ne 0) {
    throw "Windows icon generation failed."
}


# ---------------------------------------------------------
# Generate Windows version information
# ---------------------------------------------------------

$VersionParts = $Version.Split('.')

$MajorVersion = [int] $VersionParts[0]
$MinorVersion = [int] $VersionParts[1]
$PatchVersion = [int] $VersionParts[2]

$FourPartVersion = "$Version.0"

$VersionInformationFile = Join-Path `
    $WindowsBuildDirectory `
    'version_info.txt'


$VersionInformation = @"
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(
            $MajorVersion,
            $MinorVersion,
            $PatchVersion,
            0
        ),
        prodvers=(
            $MajorVersion,
            $MinorVersion,
            $PatchVersion,
            0
        ),
        mask=0x3F,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct(
                            'CompanyName',
                            'Daniel Garcia Acebo'
                        ),
                        StringStruct(
                            'FileDescription',
                            'LedgerFlow Financial Excel Organizer'
                        ),
                        StringStruct(
                            'FileVersion',
                            '$FourPartVersion'
                        ),
                        StringStruct(
                            'InternalName',
                            'LedgerFlow'
                        ),
                        StringStruct(
                            'LegalCopyright',
                            'Copyright (c) 2026 Daniel Garcia Acebo'
                        ),
                        StringStruct(
                            'OriginalFilename',
                            'LedgerFlow.exe'
                        ),
                        StringStruct(
                            'ProductName',
                            'LedgerFlow'
                        ),
                        StringStruct(
                            'ProductVersion',
                            '$FourPartVersion'
                        )
                    ]
                )
            ]
        ),
        VarFileInfo(
            [
                VarStruct(
                    'Translation',
                    [1033, 1200]
                )
            ]
        )
    ]
)
"@


Set-Content `
    -LiteralPath $VersionInformationFile `
    -Value $VersionInformation `
    -Encoding utf8NoBOM


# ---------------------------------------------------------
# Clean previous PyInstaller output
# ---------------------------------------------------------

Write-Host "Cleaning previous Windows build output..."

Remove-Item `
    -LiteralPath $DistributionDirectory `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $PyInstallerWorkDirectory `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue


# ---------------------------------------------------------
# Build with PyInstaller
# ---------------------------------------------------------

Write-Host "Running PyInstaller..."

Push-Location $ProjectDirectory

try {
    & python `
        -m PyInstaller `
        --noconfirm `
        --clean `
        --distpath $DistributionDirectory `
        --workpath $PyInstallerWorkDirectory `
        $SpecFile

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller build failed."
    }
}
finally {
    Pop-Location
}


$ExecutablePath = Join-Path `
    $ApplicationDistributionDirectory `
    'LedgerFlow.exe'


if (-not (Test-Path -LiteralPath $ExecutablePath)) {
    throw "LedgerFlow.exe was not generated: $ExecutablePath"
}


# ---------------------------------------------------------
# Prepare portable package
# ---------------------------------------------------------

Write-Host "Preparing portable Windows package..."

Remove-Item `
    -LiteralPath $PackageStageDirectory `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

New-Item `
    -ItemType Directory `
    -Force `
    -Path $PackageDirectory `
    | Out-Null


Copy-Item `
    -Path (
        Join-Path `
            $ApplicationDistributionDirectory `
            '*'
    ) `
    -Destination $PackageDirectory `
    -Recurse `
    -Force


$PortableReadme = @"
LedgerFlow $Version for Windows x64
===================================

LedgerFlow is a portable application.

How to run
----------

1. Extract the complete ZIP file.
2. Open the extracted folder.
3. Double-click LedgerFlow.exe.

Do not move LedgerFlow.exe outside this directory.
The _internal directory contains required application files.

Application data
----------------

LedgerFlow stores user data locally, normally in:

%LOCALAPPDATA%\LedgerFlow

Uninstall
---------

This portable version does not require uninstallation.

Delete the extracted LedgerFlow folder to remove the application.
Personal application data is not deleted automatically.
"@


Set-Content `
    -LiteralPath (
        Join-Path `
            $PackageDirectory `
            'README.txt'
    ) `
    -Value $PortableReadme `
    -Encoding utf8NoBOM


# ---------------------------------------------------------
# Create ZIP
# ---------------------------------------------------------

Write-Host "Creating release ZIP..."

Remove-Item `
    -LiteralPath $OutputZip `
    -Force `
    -ErrorAction SilentlyContinue


Add-Type `
    -AssemblyName System.IO.Compression.FileSystem


[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $PackageStageDirectory,
    $OutputZip,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $false
)


if (-not (Test-Path -LiteralPath $OutputZip)) {
    throw "Windows ZIP was not generated: $OutputZip"
}


Write-Host ""
Write-Host "Windows portable build created successfully:"
Write-Host $OutputZip
Write-Host ""