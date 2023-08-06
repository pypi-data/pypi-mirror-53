from libcpp.vector cimport vector
from libcpp.complex cimport complex

ctypedef complex[float] std_complex

cdef extern from "pulse/signal/hilbert_fft_host.h" namespace "pulse":
    cdef cppclass HilbertFFTHost:
        HilbertFFTHost(
                int len_signal,
                int batch
        )

        void analytic_signal(float* x_mat, complex[float]* x_a_mat)


cdef extern from "pulse/signal/hilbert_fft_device.h" namespace "pulse":
    cdef cppclass HilbertFFTDevice:
        HilbertFFTDevice(
                int len_signal,
                int batch
        )

        void analytic_signal(float* x_mat, complex[float]* x_a_mat)


cdef extern from "pulse/signal/hilbert_fir_host.h" namespace "pulse":
    cdef cppclass HilbertFIRHost:
        HilbertFIRHost(
                int len_signal,
                int batch,
                int n_taps,
                float beta
        )

        HilbertFIRHost(
                int len_signal,
                int batch,
                vector[std_complex] fir_filter
        )

        void analytic_signal(float* x_mat, complex[float]* x_a_mat)


cdef extern from "pulse/signal/hilbert_fir_device.h" namespace "pulse":
    cdef cppclass HilbertFIRDevice:
        HilbertFIRDevice(
                int len_signal,
                int batch,
                int n_taps,
                float beta
        )

        HilbertFIRDevice(
                int len_signal,
                int batch,
                vector[std_complex] fir_filter
        )

        void analytic_signal(float* x_mat, complex[float]* x_a_mat)


cdef class _hilbert_fft_host:
    cdef HilbertFFTHost* _thisptr
    cpdef call_analytic_signal(self, float[:,::1], float complex[:,::1])


cdef class _hilbert_fft_device:
    cdef HilbertFFTDevice* _thisptr
    cpdef call_analytic_signal(self, input, output)


cdef class _hilbert_fir_host:
    cdef HilbertFIRHost* _thisptr
    cpdef call_analytic_signal(self, float[:,::1], float complex[:,::1])


cdef class _hilbert_fir_device:
    cdef HilbertFIRDevice* _thisptr
    cpdef call_analytic_signal(self, input, output)