################################################################################
# Headless compute driver; separate name from Buildroot's legacy nvidia-driver.
################################################################################
CUDA_NVIDIA_DRIVER_VERSION = 550.127.05
CUDA_NVIDIA_DRIVER_SITE = https://download.nvidia.com/XFree86/Linux-x86_64/$(CUDA_NVIDIA_DRIVER_VERSION)
CUDA_NVIDIA_DRIVER_SOURCE = NVIDIA-Linux-x86_64-$(CUDA_NVIDIA_DRIVER_VERSION).run
CUDA_NVIDIA_DRIVER_LICENSE = NVIDIA Software License
CUDA_NVIDIA_DRIVER_LICENSE_FILES = LICENSE
CUDA_NVIDIA_DRIVER_REDISTRIBUTE = NO
CUDA_NVIDIA_DRIVER_DEPENDENCIES = linux host-kmod
CUDA_NVIDIA_DRIVER_MODULE_SUBDIRS = nvidia-extracted/kernel
CUDA_NVIDIA_DRIVER_MODULE_MAKE_OPTS = SYSSRC="$(LINUX_DIR)" SYSOUT="$(LINUX_DIR)" NV_KERNEL_SOURCES="$(LINUX_DIR)" NV_KERNEL_OUTPUT="$(LINUX_DIR)" NV_KERNEL_MODULES="nvidia nvidia-uvm nvidia-modeset nvidia-drm"
CUDA_NVIDIA_DRIVER_LIBS = libcuda.so.$(CUDA_NVIDIA_DRIVER_VERSION) libnvidia-ml.so.$(CUDA_NVIDIA_DRIVER_VERSION) libnvidia-ptxjitcompiler.so.$(CUDA_NVIDIA_DRIVER_VERSION) libnvidia-gpucomp.so.$(CUDA_NVIDIA_DRIVER_VERSION) libnvidia-nvvm.so.4.0.0

define CUDA_NVIDIA_DRIVER_EXTRACT_CMDS
	$(SHELL) $(CUDA_NVIDIA_DRIVER_DL_DIR)/$(CUDA_NVIDIA_DRIVER_SOURCE) --extract-only --target $(@D)/nvidia-extracted
	cp $(@D)/nvidia-extracted/LICENSE $(@D)/LICENSE
endef

define CUDA_NVIDIA_DRIVER_INSTALL_TARGET_CMDS
	$(INSTALL) -d $(TARGET_DIR)/usr/lib
	set -e; for lib in $(CUDA_NVIDIA_DRIVER_LIBS); do \
		$(INSTALL) -m 0755 $(@D)/nvidia-extracted/$$lib $(TARGET_DIR)/usr/lib/; \
		soname="$$($(TARGET_READELF) -d $(@D)/nvidia-extracted/$$lib | sed -n 's/.*(SONAME).*\[\(.*\)\].*/\1/p')"; \
		test -n "$$soname"; \
		if [ "$$soname" != "$$lib" ]; then ln -sf "$$lib" $(TARGET_DIR)/usr/lib/$$soname; fi; \
	done
	ln -sf libcuda.so.1 $(TARGET_DIR)/usr/lib/libcuda.so
	$(INSTALL) -D -m 0755 $(@D)/nvidia-extracted/nvidia-smi $(TARGET_DIR)/usr/bin/nvidia-smi
	$(INSTALL) -D -m 0755 $(@D)/nvidia-extracted/nvidia-modprobe $(TARGET_DIR)/usr/bin/nvidia-modprobe
	$(INSTALL) -D -m 0644 $(@D)/nvidia-extracted/LICENSE $(TARGET_DIR)/usr/share/licenses/cuda-nvidia-driver/LICENSE
endef

$(eval $(kernel-module))
$(eval $(generic-package))
