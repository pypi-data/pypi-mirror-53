# Cuda Library
from numba import cuda
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
from math import sqrt
import numpy as np
from array import array

drv.init()
mod = SourceModule("""
__global__ void cuda_add(double *a,double *c, int N)
{ 
  extern __shared__ double sharedMem[256];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){
     sharedMem[threadIdx.x]+=a[i];
  }
   
   __syncthreads();
   
   for(int offset=blockDim.x/2;offset>0;offset>>=1){
      if(threadIdx.x<offset){
      sharedMem[threadIdx.x]+=sharedMem[threadIdx.x+offset];
      }
      __syncthreads();
   }
   if(threadIdx.x==0){
      c[blockIdx.x]=sharedMem[0];
   }
   
}
""")
cuda_add1 = mod.get_function("cuda_add")

drv.init()
mod = SourceModule("""
__global__ void cuda_mean(double *a, double *c, double *d, int N)
{ 
  extern __shared__ double sharedMem[256];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){
     sharedMem[threadIdx.x]+=a[i]*d[i];
  }
   
   __syncthreads();
   
   for(int offset=blockDim.x/2;offset>0;offset>>=1){
      if(threadIdx.x<offset){
      sharedMem[threadIdx.x]+=sharedMem[threadIdx.x+offset];
      }
      __syncthreads();
   }
   if(threadIdx.x==0){
      c[blockIdx.x]=sharedMem[0];
   }
   
}
""")
cuda_mean1 = mod.get_function("cuda_mean")



drv.init()
mod = SourceModule("""
__global__ void cuda_var1(double *a,double b, double *c,double *d, int N)
{ 
  extern __shared__ double sharedMem[256];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){ 
    sharedMem[threadIdx.x]+=(a[i]-b)*(a[i]-b)*d[i];
  }
   
   __syncthreads();
   
   for(int offset=blockDim.x/2;offset>0;offset>>=1){
      if(threadIdx.x<offset){
      sharedMem[threadIdx.x]+=sharedMem[threadIdx.x+offset];
      }
      __syncthreads();
   }
   if(threadIdx.x==0){
      c[blockIdx.x]=sharedMem[0];
   }
   
}
""")
cuda_var1 = mod.get_function("cuda_var1")

def cuda_add(nump1):
    leng1 = len(nump1)
    nThreads = 256
    nBlocks = 68
    c1 = np.zeros((68, 1))
    input_num = np.float64(nump1.copy(order='C'))
    N = np.int32(leng1)
    cuda_add1(drv.InOut(input_num), drv.InOut(c1), N,
              block=(nThreads, 1, 1), grid=(nBlocks, 1))
    result = sum(c1)
    return(result[0])

def cuda_mean(nump1, nump2, yl):
    leng1, ncol = nump1.shape
    mean_num = np.zeros((ncol, 1))
    result = np.zeros((ncol, 1))
    weight_np = np.zeros((ncol, 1))
    nThreads = 256
    nBlocks = 68
    c1 = np.zeros((68, 1))
    for i in range(0, ncol):
        input_num = np.float64(nump1[:, i].copy(order='C'))
        weight_np = np.float64(nump2.copy(order='C'))
        N = np.int32(leng1)
        cuda_mean1(drv.InOut(input_num), drv.InOut(c1), drv.InOut(
            weight_np), N, block=(nThreads, 1, 1), grid=(nBlocks, 1))
        result[i] = sum(c1)/yl
    return(result)

def cuda_var(nump1, nump2, yl):
    leng1, ncol = nump1.shape
    mean_vec = cuda_mean(nump1, nump2, yl)
    result = np.zeros((ncol, 1))
    weight_np = np.zeros((ncol, 1))
    nThreads = 256
    nBlocks = 68
    c1 = np.zeros((68, 1))

    for i in range(0, ncol):
        input_num = np.float64(nump1[:, i].copy(order='C'))
        weight_np = np.float64(nump2.copy(order='C'))
        N = np.int32(leng1)
        mean1 = mean_vec[i]
        cuda_var1(drv.InOut(input_num), mean1, drv.InOut(c1), drv.InOut(
            weight_np), N, block=(nThreads, 1, 1), grid=(nBlocks, 1))
        result[i] = sum(c1)*leng1/((leng1-1)*yl)
    return(result)

def guass_normal(nump1, nump2, nump3):
    leng1, ncol = nump1.shape
    weight_np = nump3
    total = cuda_add(weight_np)
    mean_vec = cuda_mean(nump2, weight_np, total)
    var_vec = cuda_var(nump2, weight_np, total)
    result = np.zeros((leng1, ncol))
    for i in range(0, ncol):
        result[:, i] = (nump1[:, i]-mean_vec[i])/sqrt(var_vec[i]+0.001)
    return(result)

drv.init()
mod=SourceModule("""
__global__ void cuda_cut(double *a, double *b, double *c,double thre, int N)
{ 
  extern __shared__ double sharedMem[256];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){
     if(a[i]>thre){
     sharedMem[threadIdx.x]+=b[i];
     }
  }
   
   __syncthreads();
   
   for(int offset=blockDim.x/2;offset>0;offset>>=1){
      if(threadIdx.x<offset){
      sharedMem[threadIdx.x]+=sharedMem[threadIdx.x+offset];
      }
      __syncthreads();
   }
   if(threadIdx.x==0){
      c[blockIdx.x]=sharedMem[0];
   }
   
}
""")
cuda_cut1=mod.get_function("cuda_cut") 

def cuda_cut(nump1,nump2,th):
    num1=np.float64(nump1.copy(order='C'))
    num2=np.float64(nump2.copy(order='C'))
    thres=np.float64(th)
    nThreads=256
    nBlocks=68
    c1=np.zeros((68,1))
    N=np.int32(len(nump1))
    cuda_cut1(drv.InOut(num1),drv.InOut(num2),drv.InOut(c1),thres,N,block=(nThreads, 1, 1),grid=(nBlocks,1))
    return(sum(c1))
