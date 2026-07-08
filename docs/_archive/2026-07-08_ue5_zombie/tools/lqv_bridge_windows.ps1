# LQV Bridge — Reverse SSH tunnel from this Windows laptop to the Ai-Whisperers VPS
#
# What this does:
#   Opens a persistent reverse SSH tunnel so the VPS can SSH/connect INTO
#   this laptop as if it were a local host. The VPS reaches:
#     - This laptop's SSH (port 22 on Windows = OpenSSH server) via localhost:2222 on the VPS
#     - This laptop's WinRM (port 5985) via localhost:5986 on the VPS (if WinRM is enabled)
#     - Anything else you tunnel
#
# How to run:
#   1. Save this file as C:\Users\<you>\lqv-bridge.ps1
#   2. Open PowerShell 7+ as Administrator
#   3. Allow scripts for this session:  Set-ExecutionPolicy -Scope Process Bypass
#   4. Run:  pwsh -ExecutionPolicy Bypass -File lqv-bridge.ps1
#   5. Leave it running. The script auto-reconnects if the tunnel drops.
#
# To stop: Ctrl+C in the PowerShell window.

$VPS_HOST       = '72.61.44.159'
$VPS_SSH_PORT   = 22
$VPS_USER       = 'root'
$BRIDGE_KEY     = 'C:\Users\Public\lqv-bridge\id_ed25519'   # private key file path
$REMOTE_PORT    = 2222                                       # tunnel end on VPS side
$LOCAL_PORT     = 22                                         # SSH server on this laptop (OpenSSH)
$WINRM_REMOTE   = 5986                                       # WinRM tunnel end on VPS side
$WINRM_LOCAL    = 5985                                       # WinRM on this laptop
$RETRY_DELAY    = 10                                         # seconds between reconnect attempts

# Banner
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " LQV Bridge — Reverse SSH tunnel to Ai-Whisperers VPS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " VPS target:     ${VPS_USER}@${VPS_HOST}:${VPS_SSH_PORT}" -ForegroundColor Gray
Write-Host " Laptop local:   ${LOCAL_PORT} (SSH) / ${WINRM_LOCAL} (WinRM)" -ForegroundColor Gray
Write-Host " VPS tunnel end: ${REMOTE_PORT} (SSH) / ${WINRM_REMOTE} (WinRM)" -ForegroundColor Gray
Write-Host " Bridge key:     ${BRIDGE_KEY}" -ForegroundColor Gray
Write-Host " Retry delay:    ${RETRY_DELAY}s" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1) Verify prerequisites
Write-Host "[1/4] Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Path $BRIDGE_KEY)) {
    Write-Host "  ✗ Bridge private key not found: $BRIDGE_KEY" -ForegroundColor Red
    Write-Host "  Save the private key (id_ed25519, no passphrase) to that path." -ForegroundColor Yellow
    Write-Host "  The matching public key is in /root/.ssh/lqv_bridge.pub on the VPS." -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ Bridge key present"

# Find ssh.exe (Windows 10+ ships with OpenSSH client at this path; OpenSSH-Beta paths covered)
$ssh = $null
$candidates = @(
    "$env:WINDIR\System32\OpenSSH\ssh.exe",
    "$env:ProgramFiles\OpenSSH\ssh.exe",
    "$env:ProgramFiles(x86)\OpenSSH\ssh.exe",
    (Get-Command ssh.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source)
)
foreach ($c in $candidates) {
    if ($c -and (Test-Path $c)) { $ssh = $c; break }
}
if (-not $ssh) {
    Write-Host "  ✗ ssh.exe not found. Install OpenSSH Client: " -ForegroundColor Red
    Write-Host "    Settings → Apps → Optional Features → Add → OpenSSH Client" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ SSH client: $ssh"

# 2) Test SSH connectivity to VPS
Write-Host "[2/4] Testing SSH to VPS..." -ForegroundColor Yellow
$testCmd = "& '$ssh' -i '$BRIDGE_KEY' -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 -o BatchMode=yes ${VPS_USER}@${VPS_HOST} 'echo LQV_BRIDGE_OK'"
$testOut = Invoke-Expression $testCmd 2>&1
if ($LASTEXITCODE -ne 0 -or ($testOut -notmatch "LQV_BRIDGE_OK")) {
    Write-Host "  ✗ Cannot reach VPS via SSH. Error:" -ForegroundColor Red
    Write-Host "    $testOut" -ForegroundColor Red
    Write-Host "  Common causes:" -ForegroundColor Yellow
    Write-Host "    - Port 22 on this laptop is firewalled for outbound (check Windows Firewall)" -ForegroundColor Gray
    Write-Host "    - VPS firewall blocks your IP (shouldn't — VPS listens on 0.0.0.0:22)" -ForegroundColor Gray
    Write-Host "    - Bridge private key doesn't match the public key in authorized_keys" -ForegroundColor Gray
    Write-Host "    - Your ISP blocks outbound SSH (rare)" -ForegroundColor Gray
    exit 1
}
Write-Host "  ✓ SSH to VPS works"

# 3) Verify the laptop's SSH server is actually listening (OpenSSH on Windows)
Write-Host "[3/4] Checking local SSH server (laptop side)..." -ForegroundColor Yellow
$sshdTest = Test-NetConnection -ComputerName 127.0.0.1 -Port $LOCAL_PORT -WarningAction SilentlyContinue -InformationLevel Quiet
if (-not $sshdTest) {
    Write-Host "  ✗ No SSH server on localhost:$LOCAL_PORT — the VPS can't tunnel to it." -ForegroundColor Red
    Write-Host "  Install OpenSSH Server on this laptop:" -ForegroundColor Yellow
    Write-Host "    Settings → Apps → Optional Features → Add → OpenSSH Server → Install" -ForegroundColor Gray
    Write-Host "    Then in PowerShell (Admin):" -ForegroundColor Gray
    Write-Host "      Start-Service sshd" -ForegroundColor Gray
    Write-Host "      Set-Service -Name sshd -StartupType 'Automatic'" -ForegroundColor Gray
    Write-Host "      New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  ALSO: on this Windows machine, the built-in SSH server uses Windows" -ForegroundColor Yellow
    Write-Host "  account passwords OR public keys. To use key auth:" -ForegroundColor Yellow
    Write-Host "    1. Generate a key on this laptop:  ssh-keygen -t ed25519" -ForegroundColor Gray
    Write-Host "    2. Add the .pub to C:\Users\<you>\.ssh\authorized_keys (create the file if missing)" -ForegroundColor Gray
    Write-Host "    3. Restart the sshd service" -ForegroundColor Gray
    exit 1
}
Write-Host "  ✓ Local SSH server listening on :$LOCAL_PORT"

# 4) Open the tunnel — persistent loop with auto-reconnect
Write-Host "[4/4] Opening reverse tunnel (Ctrl+C to stop)..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  >>> After this, the VPS operator can reach this laptop via:" -ForegroundColor Green
Write-Host "      ssh -p $REMOTE_PORT root@localhost          (from the VPS box)" -ForegroundColor Green
Write-Host ""

$attempt = 0
while ($true) {
    $attempt++
    Write-Host "[$attempt] Connecting tunnel: VPS localhost:${REMOTE_PORT} → laptop :${LOCAL_PORT}" -ForegroundColor Cyan

    # Build the tunnel args
    $tunnelArgs = @(
        '-i', "`"$BRIDGE_KEY`""
        '-o', 'StrictHostKeyChecking=accept-new'
        '-o', 'ServerAliveInterval=30'
        '-o', 'ServerAliveCountMax=3'
        '-o', 'ExitOnForwardFailure=yes'
        '-o', 'TCPKeepAlive=yes'
        '-N'                                          # no command, just tunnel
        '-R', "`"${REMOTE_PORT}:127.0.0.1:${LOCAL_PORT}""   # reverse SSH tunnel
        '-R', "`"${WINRM_REMOTE}:127.0.0.1:${WINRM_LOCAL}"" # reverse WinRM tunnel (optional)
        "${VPS_USER}@${VPS_HOST}"
    )

    $proc = Start-Process -FilePath $ssh -ArgumentList $tunnelArgs -NoNewWindow -PassThru -Wait
    $code = $proc.ExitCode

    Write-Host "  Tunnel exited with code $code at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Yellow
    Write-Host "  Reconnecting in ${RETRY_DELAY}s..." -ForegroundColor Yellow
    Start-Sleep -Seconds $RETRY_DELAY
}