# Bootstrap GitHub repo for AI Infra Daily (SSH version)
# -------------------------------------------------------
# Run once to push the local repo to GitHub via SSH.
# Prerequisite: empty repo xmwen/daily-ai-infra already created on GitHub.

param(
    [string]$Owner = "xmwen",
    [string]$RepoName = "daily-ai-infra"
)

$ErrorActionPreference = "Continue"
$Root = "D:\workbuddy\daily_news"

Set-Location $Root

# 0) verify SSH
Write-Host "[1/5] Verifying SSH to GitHub..." -ForegroundColor Cyan
$sshResult = & ssh -T -o StrictHostKeyChecking=accept-new -o BatchMode=yes git@github.com 2>&1 | Out-String
if ($sshResult -match "successfully authenticated") {
    Write-Host "      SSH OK" -ForegroundColor Green
} else {
    Write-Host "ERROR: SSH failed. Make sure your public key is added to GitHub." -ForegroundColor Red
    Write-Host "       output: $sshResult"
    exit 1
}

# 1) git init (idempotent)
if (-not (Test-Path ".git")) {
    Write-Host "[2/5] git init..." -ForegroundColor Cyan
    git init -b main | Out-Null
} else {
    Write-Host "[2/5] Already a git repo, skipping init." -ForegroundColor DarkGray
}

# 1.5) configure identity (idempotent)
$gn = git config user.name 2>$null
if (-not $gn) {
    git config user.name $Owner
    git config user.email "$Owner@users.noreply.github.com"
    Write-Host "      Configured git user: $Owner"
}

# 2) first commit (if none yet)
git rev-parse --verify HEAD 2>$null | Out-Null
$hasCommit = ($LASTEXITCODE -eq 0)
if (-not $hasCommit) {
    Write-Host "[3/5] Creating initial commit..." -ForegroundColor Cyan
    git add -A
    git commit -m "chore: bootstrap daily AI infra digest site" | Out-Null
} else {
    Write-Host "[3/5] Commit already exists, skipping." -ForegroundColor DarkGray
}

# 3) configure SSH remote
$sshUrl = "git@github.com:$Owner/$RepoName.git"
$existingRemote = git remote get-url origin 2>$null
if (-not $existingRemote) {
    Write-Host "[4/5] Adding origin: $sshUrl" -ForegroundColor Cyan
    git remote add origin $sshUrl
} elseif ($existingRemote -ne $sshUrl) {
    Write-Host "[4/5] Updating origin: $existingRemote -> $sshUrl" -ForegroundColor Cyan
    git remote set-url origin $sshUrl
} else {
    Write-Host "[4/5] origin already correct." -ForegroundColor DarkGray
}

# 4) push
Write-Host "[5/5] Pushing main to GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: push failed. Possible reasons:" -ForegroundColor Red
    Write-Host "   - repo $Owner/$RepoName does not exist on GitHub yet" -ForegroundColor Yellow
    Write-Host "   - or the repo is not empty (README/.gitignore was auto-created)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   -> create an empty repo at https://github.com/new and retry." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "SUCCESS: code pushed!" -ForegroundColor Green
Write-Host "   Repo : https://github.com/$Owner/$RepoName"
Write-Host ""
Write-Host "NEXT STEP: enable GitHub Pages (about 30 seconds)" -ForegroundColor Yellow
Write-Host "   1) open: https://github.com/$Owner/$RepoName/settings/pages"
Write-Host "   2) Source: 'Deploy from a branch'"
Write-Host "   3) Branch: main   Folder: / (root)   -> Save"
Write-Host "   4) wait 1-2 minutes, dashboard URL: https://$Owner.github.io/$RepoName/"
Write-Host ""
Write-Host "From now on, daily push is handled by scripts/publish.py"
