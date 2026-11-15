#!/bin/sh
set -eu
TARGET_DIR="$1"
BOARD_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$BOARD_DIR/../../.." && pwd)
mkdir -p "$TARGET_DIR/etc/runlevels/boot" "$TARGET_DIR/etc/runlevels/default" \
    "$TARGET_DIR/etc/conf.d" "$TARGET_DIR/usr/bin" "$TARGET_DIR/etc/sysctl.d" \
    "$TARGET_DIR/var" "$TARGET_DIR/tmp" "$TARGET_DIR/run" "$TARGET_DIR/boot"
# OpenRC inspects the root's ro option; noauto avoids /dev/root fsck/mount attempts.
cat > "$TARGET_DIR/etc/fstab" <<'EOF'
/dev/root / ext4 ro,noauto,noatime 0 0
tmpfs /tmp tmpfs mode=1777,nosuid,nodev,size=256m 0 0
tmpfs /run tmpfs mode=0755,nosuid,nodev 0 0
EOF
ln -sfn /proc/self/mounts "$TARGET_DIR/etc/mtab"
# /etc itself stays immutable. Resolver is the deliberate writable exception.
rm -f "$TARGET_DIR/etc/resolv.conf"
ln -s /run/resolv.conf "$TARGET_DIR/etc/resolv.conf"
cat > "$TARGET_DIR/etc/sysctl.d/99-cuda-hardening.conf" <<'EOF'
kernel.randomize_va_space = 2
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
fs.suid_dumpable = 0
EOF
ln -sf /etc/init.d/cuda-writable "$TARGET_DIR/etc/runlevels/boot/cuda-writable"
test -f "$TARGET_DIR/etc/init.d/cgroups"
ln -sf /etc/init.d/cgroups "$TARGET_DIR/etc/runlevels/boot/cgroups"
printf '\nrc_cgroup_mode="unified"\n' >> "$TARGET_DIR/etc/rc.conf"
ln -sf /etc/init.d/S99cuda-benchmark "$TARGET_DIR/etc/runlevels/default/cuda-benchmark"
# The OpenRC sysv bridge also scans S??*: move the real OpenRC script to a
# non-SysV name so it is started exactly once via native runlevel registration.
mv "$TARGET_DIR/etc/init.d/S99cuda-benchmark" "$TARGET_DIR/etc/init.d/cuda-benchmark"
ln -sf /etc/init.d/cuda-benchmark "$TARGET_DIR/etc/runlevels/default/cuda-benchmark"
chmod 0755 "$TARGET_DIR/etc/init.d/cuda-benchmark" "$TARGET_DIR/etc/init.d/cuda-writable" \
    "$TARGET_DIR/usr/local/bin/cuda-benchmark" "$TARGET_DIR/usr/local/bin/verify-runtime" "$TARGET_DIR/usr/local/bin/container-smoke" "$TARGET_DIR/usr/local/bin/verify-gpu-stack"
ln -sf /usr/local/bin/cuda-benchmark "$TARGET_DIR/usr/bin/cuda-benchmark"
# Lock root independent of mkpasswd's interpretation of the configured marker.
sed -i 's/^root:[^:]*:/root:!:/' "$TARGET_DIR/etc/shadow"
if [ -n "${CUDA_DEMO_PASSWORD_HASH_FILE:-}" ]; then
    hash=$(cat "$CUDA_DEMO_PASSWORD_HASH_FILE")
    case "$hash" in
        '$6$'*) ;;
        *) echo 'Demo password file must contain a SHA-512 crypt hash generated with openssl passwd -6' >&2; exit 1 ;;
    esac
    case "$hash" in *:*|*' '*|*'&'*) echo 'Invalid password hash characters' >&2; exit 1 ;; esac
    awk -F: -v hash="$hash" 'BEGIN {OFS=FS} $1=="root" {$2=hash} {print}' "$TARGET_DIR/etc/shadow" > "$TARGET_DIR/etc/shadow.new"
    mv "$TARGET_DIR/etc/shadow.new" "$TARGET_DIR/etc/shadow"
fi
chmod 0600 "$TARGET_DIR/etc/shadow"
# No network login server is selected. Provision a hashed console password
# offline in the staged shadow file if an interactive demo login is required.
