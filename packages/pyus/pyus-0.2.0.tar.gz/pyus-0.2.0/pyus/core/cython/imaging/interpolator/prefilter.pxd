from pyus.core.cython.utils.types cimport complex
from pyus.core.cython.imaging.interpolator.interpolator cimport interp_type

cdef extern from "pulse/interpolation/prefilter.h" namespace "pulse":

    void prefilterChannelHost[Interp](
            float* raw_data, int nb_elem, int nb_samples,
            char bc_type);

    # Trick to use different names for overloaded functions as Cython does not
    # seem to be able to handle them
    void prefilterChannelHost_c "pulse::prefilterChannelHost"[Interp](
            float complex* raw_data, int nb_elem, int nb_samples,
            char bc_type);

    void prefilterChannelDevice[Interp](
            float* raw_data, int nb_elem, int nb_samples,
            char bc_type);

    void prefilterChannelDevice_c "pulse::prefilterChannelDevice"[Interp](
            complex[float]* raw_data, int nb_elem, int nb_samples,
            char bc_type);


cpdef call_prefilter_host(float[:,:,:,::1] raw_data, boundary, interp_type interpolator)
cpdef call_prefilter_iq_host(float complex[:,:,:,::1] raw_data, boundary, interp_type interpolator)
cpdef call_prefilter_device(raw_data, boundary, interp_type interpolator)
cpdef call_prefilter_iq_device(raw_data, boundary, interp_type interpolator)