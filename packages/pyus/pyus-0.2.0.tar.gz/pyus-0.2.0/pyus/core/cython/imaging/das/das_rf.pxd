from libcpp.vector cimport vector
from pyus.core.cython.utils.types cimport float_complex_cpu, float_complex_gpu
from pyus.core.cython.imaging.functors.delays cimport delay_type
from pyus.core.cython.imaging.interpolator.interpolator cimport interp_type
from pyus.core.cython.imaging.functors.windows cimport window_type


cdef extern from "pulse/beamformer/beamformer_host.h" namespace "pulse":
    cdef cppclass BeamformerHost:

        BeamformerHost(
                vector[float] element_positions,
                vector[float] t_axis,
                vector[float] x_im_axis,
                vector[float] y_im_axis,
                vector[float] z_im_axis)

        void reconstruct[float_complex_cpu, Delay, Interp, Apod](
                const float_complex_cpu* raw_data,
                int frame_number,
                vector[Delay] delays,
                Interp interp,
                Apod apod,
                float_complex_cpu* rf_image
        )


cdef extern from "pulse/beamformer/beamformer_device.h" namespace "pulse":
    cdef cppclass BeamformerDevice:

        BeamformerDevice(
                vector[float] element_positions,
                vector[float] t_axis,
                vector[float] x_im_axis,
                vector[float] y_im_axis,
                vector[float] z_im_axis)

        void reconstruct[float_complex_gpu, Delay, Interp, Apod](
                const float_complex_gpu* raw_data,
                int frame_number,
                vector[Delay] delays,
                Interp interp,
                Apod apod,
                float_complex_gpu* rf_image
        )


cdef class _das_rf_host:
    cdef BeamformerHost* _thisptr

    cdef tuple size_image

    cpdef call_reconstruct(
            self,
            float[:,:,:,::1] raw_data,
            delay_type dummy,
            delay_type[::1] delay,
            interp_type interp,
            window_type window,
            float[:,:,:,::1] rf_image
    )

    cpdef call_reconstruct_iq(
            self,
            float complex[:,:,:,::1] raw_data,
            delay_type dummy,
            delay_type[::1] delay,
            interp_type interp,
            window_type window,
            float complex[:,:,:,::1] rf_image
    )


cdef class _das_rf_device:
    cdef BeamformerDevice* _thisptr

    cdef tuple size_image

    cpdef call_reconstruct(
            self,
            raw_data_gpu,
            delay_type dummy,
            delay_type[::1] delay,
            interp_type interp,
            window_type window,
            rf_image_gpu
    )

    cpdef call_reconstruct_iq(
            self,
            raw_data_gpu,
            delay_type dummy,
            delay_type[::1] delay,
            interp_type interp,
            window_type window,
            rf_image_gpu
    )
