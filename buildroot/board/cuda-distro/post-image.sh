#!/bin/sh
set -eu
BINARIES_DIR="$1"
BOARD_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
for f in rootfs.ext4 bzImage efi-part/EFI/BOOT/bootx64.efi; do
    test -s "$BINARIES_DIR/$f" || { echo "Missing boot artifact: $f" >&2; exit 1; }
done
cp "$BOARD_DIR/grub.cfg" "$BINARIES_DIR/efi-part/EFI/BOOT/grub.cfg"
# No mounts, loop devices or host grub installation; all tools are Buildroot hosts.
GENIMAGE_TMP=$(mktemp -d "${BUILD_DIR}/genimage.XXXXXX")
trap 'rmdir "$GENIMAGE_TMP" 2>/dev/null || true' EXIT
"$HOST_DIR/bin/genimage" --rootpath "$TARGET_DIR" --tmppath "$GENIMAGE_TMP" \
    --inputpath "$BINARIES_DIR" --outputpath "$BINARIES_DIR" --config "$BOARD_DIR/genimage.cfg"
python3 "$BOARD_DIR/../../../scripts/validate-image.py" "$BINARIES_DIR/cuda-distro.img"
ln -sf cuda-distro.img "$BINARIES_DIR/disk.img"
echo 'Image assembled and structure checked; boot execution still requires QEMU/hardware.'
