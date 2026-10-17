# One-click setup for people who don't use a terminal. Started by "Extract game data.bat" (Windows PowerShell 5.1 compatible).
# Gets a Python that UnityPy supports, installs the dependencies into .venv, finds the game, runs build_data.py and opens the creator.
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$venvDir = Join-Path $root '.venv'
$venvPy = Join-Path $venvDir 'Scripts\python.exe'
$gameFile = Join-Path $root '.game-folder'
$de = (Get-UICulture).TwoLetterISOLanguageName -eq 'de'
# UnityPy's dependencies only ship for these versions; 3.15 has no wheels yet
$pythonVersions = '3.14', '3.13', '3.12', '3.11', '3.10'
$pythonCheck = 'import sys; sys.exit(0 if (3, 10) <= sys.version_info[:2] <= (3, 14) else 1)'

function Say($en, $deText, $color = 'Gray') { Write-Host $(if ($de) { $deText } else { $en }) -ForegroundColor $color }
function Step($en, $deText) { Write-Host; Say $en $deText 'Cyan' }
function Finish($code) {
  Write-Host
  Read-Host $(if ($de) { 'Zum Schließen Enter drücken' } else { 'Press Enter to close' }) | Out-Null
  exit $code
}
function Fail($en, $deText) {
  Write-Host
  Say $en $deText 'Red'
  Say 'If you are stuck, open an issue on GitHub and include a screenshot of this window:' 'Wenn du nicht weiterkommst, eröffne ein Issue auf GitHub und füge einen Screenshot dieses Fensters bei:'
  Write-Host 'https://github.com/MaSch0212/walkabout-minigolf-character-creator/issues'
  Finish 1
}

function Test-Python($exe, $pyArgs) {
  try { & $exe @pyArgs -c $pythonCheck 2>$null | Out-Null; return $LASTEXITCODE -eq 0 } catch { return $false }
}
function Find-Python {
  $candidates = @()
  if (Get-Command py -ErrorAction SilentlyContinue) { foreach ($v in $pythonVersions) { $candidates += , @('py', "-$v") } }
  if (Get-Command python -ErrorAction SilentlyContinue) { $candidates += , @('python') }
  foreach ($c in $candidates) {
    $pyArgs = @($c | Select-Object -Skip 1)
    if (Test-Python $c[0] $pyArgs) { return , $c }
  }
  return $null
}

function Test-GameFolder($dir) {
  if (-not $dir) { return $false }
  # plain strings instead of Join-Path, which complains about drives that no longer exist
  foreach ($sub in '*_Data\StreamingAssets\aa\StandaloneWindows64\', 'StreamingAssets\aa\StandaloneWindows64\', '') {
    $bundle = "$($dir.TrimEnd('\'))\$($sub)avatarsandputters_assets_all.bundle"
    if (Resolve-Path $bundle -ErrorAction SilentlyContinue) { return $true }
  }
  return $false
}
function Find-Game {
  $candidates = @()
  if (Test-Path $gameFile) { $candidates += (Get-Content -LiteralPath $gameFile -TotalCount 1) }
  # Meta Quest Link app: every library has its games under <library>\Software\<app name>
  $libraries = 'HKCU:\Software\Oculus VR, LLC\Oculus\Libraries'
  if (Test-Path $libraries) {
    foreach ($lib in Get-ChildItem $libraries) {
      $p = Get-ItemProperty $lib.PSPath
      foreach ($path in $p.OriginalPath, $p.Path) { if ($path) { $candidates += "$path\Software\mighty-coconut-walkabout-mini-golf" } }
    }
  }
  $candidates += "$env:ProgramFiles\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf"
  # Steam: check every game folder of every Steam library
  $steam = (Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction SilentlyContinue).SteamPath
  if ($steam) {
    $steamLibraries = @($steam)
    $vdf = "$steam\steamapps\libraryfolders.vdf"
    if (Test-Path $vdf) {
      foreach ($m in [regex]::Matches((Get-Content -Raw -LiteralPath $vdf), '"path"\s+"([^"]+)"')) { $steamLibraries += $m.Groups[1].Value -replace '\\\\', '\' }
    }
    foreach ($lib in $steamLibraries) {
      $candidates += Get-ChildItem -Directory "$lib\steamapps\common" -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
    }
  }
  foreach ($c in $candidates) { if (Test-GameFolder $c) { return $c } }
  return $null
}
function Select-GameFolder {
  Add-Type -AssemblyName System.Windows.Forms
  while ($true) {
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = $(if ($de) { 'Wähle den Installationsordner von Walkabout Mini Golf aus' } else { 'Select the Walkabout Mini Golf install folder' })
    $owner = New-Object System.Windows.Forms.Form -Property @{ TopMost = $true }
    $result = $dialog.ShowDialog($owner)
    $owner.Dispose()
    if ($result -ne 'OK') { return $null }
    if (Test-GameFolder $dialog.SelectedPath) { return $dialog.SelectedPath }
    Say "Walkabout Mini Golf was not found in $($dialog.SelectedPath). Please try again." "In $($dialog.SelectedPath) wurde Walkabout Mini Golf nicht gefunden. Bitte versuche es noch einmal." 'Yellow'
  }
}

Say 'Walkabout Mini Golf Character Creator - setup' 'Walkabout Mini Golf Avatar-Editor - Einrichtung' 'White'

# 1. Python environment (only needed the first time, or when it broke)
if ((Test-Path $venvPy) -and -not (Test-Python $venvPy @())) { Remove-Item -Recurse -Force $venvDir }
if (-not (Test-Path $venvPy)) {
  Step 'Looking for Python...' 'Suche Python...'
  $python = Find-Python
  if (-not $python -and (Get-Command py -ErrorAction SilentlyContinue)) {
    # The Python install manager can fetch a matching version itself; the old py launcher can't ("install" fails there)
    & py install --dry-run 3.14 *> $null
    if ($LASTEXITCODE -eq 0) {
      Step 'Installing Python 3.14 (this can take a few minutes)...' 'Installiere Python 3.14 (das kann ein paar Minuten dauern)...'
      & py install -y 3.14
      $python = Find-Python
    }
  }
  if (-not $python) {
    Write-Host
    Say 'Python is not installed (or only a version that is too new or too old).' 'Python ist nicht installiert (oder nur eine zu neue oder zu alte Version).' 'Yellow'
    Say 'The Microsoft Store now opens the "Python Install Manager". Click "Install" (or "Get"),' 'Der Microsoft Store öffnet jetzt den "Python Install Manager". Klicke auf "Installieren" (oder "Herunterladen"),'
    Say 'wait until it is done, and then double-click "Extract game data.bat" again.' 'warte, bis die Installation fertig ist, und doppelklicke dann erneut auf "Extract game data.bat".'
    Start-Process 'ms-windows-store://pdp/?ProductId=9NQ7512CXL7T'
    Finish 1
  }
  Step 'Setting up a private Python environment for the creator...' 'Richte eine eigene Python-Umgebung für den Editor ein...'
  $pyArgs = @($python | Select-Object -Skip 1)
  & $python[0] @pyArgs -m venv $venvDir
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPy)) { Fail 'Could not set up the Python environment.' 'Die Python-Umgebung konnte nicht eingerichtet werden.' }
}

# 2. Dependencies (-U picks up UnityPy fixes for newer game versions)
Step 'Downloading the helper components (UnityPy, numpy, Pillow)...' 'Lade die Hilfskomponenten herunter (UnityPy, numpy, Pillow)...'
& $venvPy -m pip install --disable-pip-version-check -q -U -r (Join-Path $root 'requirements.txt')
if ($LASTEXITCODE -ne 0) { Fail 'Could not download the helper components. Check your internet connection and try again.' 'Die Hilfskomponenten konnten nicht heruntergeladen werden. Prüfe deine Internetverbindung und versuche es erneut.' }

# 3. Game folder
Step 'Looking for Walkabout Mini Golf...' 'Suche Walkabout Mini Golf...'
$game = Find-Game
if (-not $game) {
  Say 'The game was not found automatically. Please select its install folder in the window that opens.' 'Das Spiel wurde nicht automatisch gefunden. Bitte wähle im folgenden Fenster seinen Installationsordner aus.' 'Yellow'
  $game = Select-GameFolder
  if (-not $game) { Fail 'No game folder selected.' 'Kein Spielordner ausgewählt.' }
}
Set-Content -LiteralPath $gameFile -Value $game
Say "Found: $game" "Gefunden: $game" 'Green'

# 4. Extract
Step 'Reading the models from the game (about a minute)...' 'Lese die Modelle aus dem Spiel (etwa eine Minute)...'
& $venvPy (Join-Path $root 'tools\build_data.py') $game
if ($LASTEXITCODE -ne 0) { Fail 'Reading the game data failed. A game update may have changed the files; see "After a game update" in the README.' 'Das Auslesen der Spieldaten ist fehlgeschlagen. Vielleicht hat ein Spiel-Update die Dateien geändert; siehe "Nach einem Spiel-Update" in der README.' }

Write-Host
Say 'Done! The creator now opens in your browser. Next time, just double-click index.html.' 'Fertig! Der Editor öffnet sich jetzt im Browser. Beim nächsten Mal einfach index.html doppelklicken.' 'Green'
Start-Process (Join-Path $root 'index.html')
Finish 0
