# Runtime binaries; SDK headers go to staging only. No nvcc on the target.
CUDA_RUNTIME_VERSION = 12.4.127
CUDA_RUNTIME_SITE = https://developer.download.nvidia.com/compute/cuda/redist/cuda_cudart/linux-x86_64
CUDA_RUNTIME_SOURCE = cuda_cudart-linux-x86_64-12.4.127-archive.tar.xz
CUDA_RUNTIME_LICENSE = NVIDIA proprietary license
CUDA_RUNTIME_LICENSE_FILES = LICENSE
CUDA_RUNTIME_REDISTRIBUTE = NO
CUDA_RUNTIME_DEPENDENCIES = cuda-nvidia-driver
CUDA_RUNTIME_INSTALL_STAGING = YES

define CUDA_RUNTIME_INSTALL_STAGING_CMDS
	$(INSTALL) -d $(STAGING_DIR)/usr/include $(STAGING_DIR)/usr/lib
	cp -a $(@D)/include/. $(STAGING_DIR)/usr/include/
	test -f $(@D)/lib/libcudart.so.12.4.127
	cp -a $(@D)/lib/libcudart*.so* $(STAGING_DIR)/usr/lib/
endef

define CUDA_RUNTIME_INSTALL_TARGET_CMDS
	$(INSTALL) -d $(TARGET_DIR)/usr/lib
	test -f $(@D)/lib/libcudart.so.12.4.127
	cp -a $(@D)/lib/libcudart*.so* $(TARGET_DIR)/usr/lib/
	$(INSTALL) -D -m 0644 $(@D)/LICENSE $(TARGET_DIR)/usr/share/licenses/cuda-runtime/LICENSE
endef

$(eval $(generic-package))
