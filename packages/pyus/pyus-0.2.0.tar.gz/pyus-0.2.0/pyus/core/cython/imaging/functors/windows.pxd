from pyus.core.cython.utils.types cimport float3


cdef extern from "pulse/window/window_functor.h" namespace "pulse":
    cdef:
        cppclass Selfridge2D:
            Selfridge2D()
            Selfridge2D(float wavelength, float el_width)
            float operator()(float3 pos_im, float3 pos_td)

        cppclass Selfridge3D:
            Selfridge3D(float wavelength, float el_width_x, float el_width_y)
            float operator()(float3 pos_im, float3 pos_td)

        cppclass Boxcar:
            Boxcar()
            Boxcar(float f_number)
            float operator()(float3 pos_im, float3 pos_td)

        cppclass Hanning:
            Hanning(float f_number)
            float operator()(float3 pos_im, float3 pos_td)

        cppclass Hamming:
            Hamming(float f_number)
            float operator()(float3 pos_im, float3 pos_td)

        cppclass Tukey:
            Tukey(float alpha, float f_number)
            float operator()(float3 pos_im, float3 pos_td)

        cppclass IdentityWindow:
            IdentityWindow()
            float operator()(float3 pos_im, float3 pos_td)


cdef class _Selfridge2D:
    cdef Selfridge2D* _thisptr

cdef class _Selfridge3D:
    cdef Selfridge3D* _thisptr

cdef class _Boxcar:
    cdef Boxcar* _thisptr

cdef class _Hanning:
    cdef Hanning* _thisptr

cdef class _Hamming:
    cdef Hamming* _thisptr

cdef class _Tukey:
    cdef Tukey* _thisptr

cdef class _IdentityWindow:
    cdef IdentityWindow* _thisptr

ctypedef fused window_type:
    _Boxcar
    _Hanning
    _Hamming
    _IdentityWindow
    _Selfridge2D
    _Selfridge3D
    _Tukey
