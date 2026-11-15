#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
IMAGES_DIR="$PROJECT_ROOT/buildroot-src/output/images"
DISK_IMG="${DISK_IMAGE:-$IMAGES_DIR/cuda-distro.img}"
command -v qemu-system-x86_64 >/dev/null || { echo 'BLOCKED: install qemu-system-x86' >&2; exit 1; }
python3 "$PROJECT_ROOT/scripts/validate-image.py" "$DISK_IMG"
accel=(-accel tcg -cpu max)
[[ -r /dev/kvm && -w /dev/kvm ]] && accel=(-accel kvm -cpu host)
boot=()
if [[ ${DIRECT_KERNEL_BOOT:-0} == 1 ]]; then
    [[ -s "$IMAGES_DIR/bzImage" ]] || { echo 'Missing bzImage' >&2; exit 1; }
    boot=(-kernel "$IMAGES_DIR/bzImage" -append 'console=ttyS0,115200 root=PARTUUID=87d7c7b4-faf3-4ed8-928f-e41529ab9939 ro rootwait')
    echo 'Direct kernel boot does not test GRUB/EFI.' >&2
else
    firmware=${OVMF_CODE:-/usr/share/OVMF/OVMF_CODE.fd}
    [[ -r $firmware ]] || { echo 'BLOCKED: install ovmf or set OVMF_CODE to non-Secure-Boot OVMF firmware' >&2; exit 1; }
    boot=(-drive "if=pflash,format=raw,readonly=on,file=$firmware")
fi
serial=(-serial mon:stdio)
[[ -n ${SERIAL_LOG:-} ]] && serial=(-serial "file:$SERIAL_LOG" -monitor none)
exec qemu-system-x86_64 "${accel[@]}" "${boot[@]}" \
    -m "${QEMU_RAM_MB:-4096}" -smp "${QEMU_VCPUS:-4}" \
    -drive "file=$DISK_IMG,if=none,id=hd0,format=raw,snapshot=on" \
    -device virtio-blk-pci,drive=hd0,bootindex=1 \
    -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
    -display none "${serial[@]}" -no-reboot "$@"
