param(
    [string]$ImagePath = "$PSScriptRoot\..\buildroot-src\output\images\cuda-distro.img",
    [string]$OvmfCode = $env:OVMF_CODE,
    [int]$RamMB = 4096,
    [int]$Cpus = 4,
    [int]$SshPort = 2222
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $ImagePath)) { Write-Error "Missing disk image: $ImagePath"; exit 1 }
if (-not $OvmfCode -or -not (Test-Path -LiteralPath $OvmfCode)) { Write-Error 'Set OVMF_CODE to non-Secure-Boot x86_64 UEFI firmware'; exit 1 }
$QemuExe = (Get-Command qemu-system-x86_64.exe -ErrorAction SilentlyContinue).Source
if (-not $QemuExe) { $QemuExe = 'C:\Program Files\qemu\qemu-system-x86_64.exe' }
if (-not (Test-Path -LiteralPath $QemuExe)) { Write-Error 'QEMU executable not found'; exit 1 }
python "$PSScriptRoot\validate-image.py" $ImagePath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $QemuExe -accel tcg -cpu max -m $RamMB -smp $Cpus `
    -drive "if=pflash,format=raw,readonly=on,file=$OvmfCode" `
    -drive "file=$ImagePath,if=none,format=raw,id=hd0,snapshot=on" `
    -device virtio-blk-pci,drive=hd0 -netdev user,id=net0 `
    -device virtio-net-pci,netdev=net0 -display none -serial mon:stdio -no-reboot
exit $LASTEXITCODE
