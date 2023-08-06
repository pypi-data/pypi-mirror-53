from libcpp.vector cimport vector

cdef extern from 'cuda_runtime_api.h':
    struct float2:
        float x, y

    struct float3:
        float x, y, z

    struct float4:
        float x, y, z, w

    struct int2:
        int x, y

    struct int3:
        int x, y, z

    struct int4:
        int x, y, z, w

# Interface thrust complex type
cdef extern from 'thrust/complex.h' namespace 'thrust':
    cdef cppclass complex[T]:
        pass

cdef extern from "pulse/helper/functor.h" namespace "pulse":
    void apply_functor[T](vector[float3]* input_1, vector[float3]* input_2,
        vector[float]* output, T functor)

ctypedef fused float_complex_cpu:
    float
    float complex

ctypedef fused float_complex_gpu:
    float
    complex[float]