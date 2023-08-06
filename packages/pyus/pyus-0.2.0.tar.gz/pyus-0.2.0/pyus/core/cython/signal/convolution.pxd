from pyus.core.cython.utils.types cimport float_complex_cpu, float_complex_gpu


cdef extern from "pulse/signal/conv_direct_1d_host.h" namespace "pulse":
    cdef cppclass ConvolutionDirect1DHost:

        ConvolutionDirect1DHost()

        void convolve_full[float_complex_cpu](
                const float_complex_cpu* input, int input_size, int nb_inputs,
                const float_complex_cpu* filter, int filter_size, int nb_filters,
                float_complex_cpu* output
        )

        void convolve_same[float_complex_cpu](
                const float_complex_cpu* input, int input_size, int nb_inputs,
                const float_complex_cpu* filter, int filter_size, int nb_filters,
                float_complex_cpu* output
        )

        void convolve_valid[float_complex_cpu](
                const float_complex_cpu* input, int input_size, int nb_inputs,
                const float_complex_cpu* filter, int filter_size, int nb_filters,
                float_complex_cpu* output
        )


cdef extern from "pulse/signal/conv_direct_1d_device.h" namespace "pulse":
    cdef cppclass ConvolutionDirect1DDevice:

        ConvolutionDirect1DDevice()

        void convolve_full[float_complex_gpu](
                const float_complex_gpu* input, int input_size, int nb_inputs,
                const float_complex_gpu* filter, int filter_size, int nb_filters,
                float_complex_gpu* output
        )

        void convolve_same[float_complex_gpu](
                const float_complex_gpu* input, int input_size, int nb_inputs,
                const float_complex_gpu* filter, int filter_size, int nb_filters,
                float_complex_gpu* output
        )

        void convolve_valid[float_complex_gpu](
                const float_complex_gpu* input, int input_size, int nb_inputs,
                const float_complex_gpu* filter, int filter_size, int nb_filters,
                float_complex_gpu* output
        )


cdef class _conv_direct_1D_host:
    cdef ConvolutionDirect1DHost* _thisptr
    cpdef call_convolve(self,
                        float_complex_cpu[:,::1] input,
                        float_complex_cpu[:,::1] filter,
                        float_complex_cpu[:,::1] output,
                        mode_str)

cdef class _conv_direct_1D_device:
    cdef ConvolutionDirect1DDevice* _thisptr
    cpdef call_convolve(self, input, filter, output, mode_str)
