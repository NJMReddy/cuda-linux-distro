#include <cuda_runtime.h>
#include <cudnn.h>
#include <cstdio>
#include <vector>

#define CUDA(call) do { auto rc=(call); if(rc!=cudaSuccess){std::fprintf(stderr,"FAIL %s: %s\n",#call,cudaGetErrorString(rc)); return 1;} } while(0)
#define DNN(call) do { auto rc=(call); if(rc!=CUDNN_STATUS_SUCCESS){std::fprintf(stderr,"FAIL %s: %s\n",#call,cudnnGetErrorString(rc)); return 1;} } while(0)
__global__ void add(const float *a,const float *b,float *out,int n){
    int i=blockDim.x*blockIdx.x+threadIdx.x;
    if(i<n) out[i]=a[i]+b[i];
}
int main(){
    int count=0;
    auto status=cudaGetDeviceCount(&count);
    if(status==cudaErrorNoDevice || (status==cudaSuccess && !count)){
        std::puts("BLOCKED: no CUDA device"); return 77;
    }
    CUDA(status);
    constexpr int n=1048576, iterations=100;
    constexpr size_t bytes=n*sizeof(float);
    std::vector<float> x(n),y(n),result(n);
    for(int i=0;i<n;++i){x[i]=float(i%127)-64; y[i]=float(i%17);}
    float *a,*b,*out;
    CUDA(cudaMalloc(&a,bytes)); CUDA(cudaMalloc(&b,bytes)); CUDA(cudaMalloc(&out,bytes));
    CUDA(cudaMemcpy(a,x.data(),bytes,cudaMemcpyHostToDevice));
    CUDA(cudaMemcpy(b,y.data(),bytes,cudaMemcpyHostToDevice));
    cudaEvent_t start,stop;
    CUDA(cudaEventCreate(&start)); CUDA(cudaEventCreate(&stop));
    add<<<n/256,256>>>(a,b,out,n); CUDA(cudaGetLastError()); CUDA(cudaDeviceSynchronize());
    CUDA(cudaEventRecord(start));
    for(int j=0;j<iterations;++j) add<<<n/256,256>>>(a,b,out,n);
    CUDA(cudaGetLastError()); CUDA(cudaEventRecord(stop)); CUDA(cudaEventSynchronize(stop));
    float ms; CUDA(cudaEventElapsedTime(&ms,start,stop));
    if(!(ms>0)) return 1;
    CUDA(cudaMemcpy(result.data(),out,bytes,cudaMemcpyDeviceToHost));
    for(int i=0;i<n;++i) if(result[i]!=x[i]+y[i]){std::fprintf(stderr,"FAIL add element %d\n",i);return 1;}
    cudnnHandle_t handle; cudnnTensorDescriptor_t tensor; cudnnActivationDescriptor_t relu;
    DNN(cudnnCreate(&handle)); DNN(cudnnCreateTensorDescriptor(&tensor));
    DNN(cudnnSetTensor4dDescriptor(tensor,CUDNN_TENSOR_NCHW,CUDNN_DATA_FLOAT,1,1,1,n));
    DNN(cudnnCreateActivationDescriptor(&relu));
    DNN(cudnnSetActivationDescriptor(relu,CUDNN_ACTIVATION_RELU,CUDNN_PROPAGATE_NAN,0));
    float alpha=1,beta=0;
    DNN(cudnnActivationForward(handle,relu,&alpha,tensor,out,&beta,tensor,a));
    CUDA(cudaMemcpy(result.data(),a,bytes,cudaMemcpyDeviceToHost));
    for(int i=0;i<n;++i){float v=x[i]+y[i]; if(result[i]!=(v>0?v:0)){std::fprintf(stderr,"FAIL ReLU element %d\n",i);return 1;}}
    cudaDeviceProp device; CUDA(cudaGetDeviceProperties(&device,0));
    int runtime; CUDA(cudaRuntimeGetVersion(&runtime));
    std::printf("PASS GPU=%s CUDA=%d cuDNN=%zu elements=%d iterations=%d mean_ms=%g effective_GBps=%g\n",device.name,runtime,cudnnGetVersion(),n,iterations,ms/iterations,3.*bytes*iterations/(ms*1e6));
    return 0;
}
