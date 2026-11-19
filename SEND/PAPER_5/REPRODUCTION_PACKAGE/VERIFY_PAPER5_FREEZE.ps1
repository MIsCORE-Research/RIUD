param([string]$Package = $PSScriptRoot)
$manifest = Join-Path $Package 'SHA256_MANIFEST.txt'
$bad = @()
foreach ($line in Get-Content $manifest) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $parts = $line -split '  ', 2
    $path = Join-Path $Package $parts[1]
    if (!(Test-Path -LiteralPath $path)) { $bad += "MISSING $($parts[1])"; continue }
    $got = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($got -ne $parts[0].ToLowerInvariant()) { $bad += "HASH_FAIL $($parts[1])" }
}
if ($bad.Count) { $bad; exit 1 }
'VERIFY_PAPER5_FREEZE=PASS'
