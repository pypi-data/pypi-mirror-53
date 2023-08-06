cdef extern from "pulse/interpolation/interpolation.h":
    ctypedef int Nearest "pulse::InterpScheme::NEAREST"
    ctypedef int Linear "pulse::InterpScheme::LINEAR"
    ctypedef int Keys "pulse::InterpScheme::KEYS"
    ctypedef int Bspline3 "pulse::InterpScheme::BSPLINE_3"
    ctypedef int Bspline4 "pulse::InterpScheme::BSPLINE_4"
    ctypedef int Bspline5 "pulse::InterpScheme::BSPLINE_5"
    ctypedef int Omoms3 "pulse::InterpScheme::OMOMS_3"

cdef extern from "pulse/interpolation/interpolation.h" namespace "pulse":
    cdef:
        cppclass InterpFunctor[InterpScheme]:
            InterpFunctor()
            InterpFunctor(float first_sample, float last_sample, size_t nb_samples,
                  float sampling_freq)

            float operator()(float abscissa, const float* data, size_t channel)

cdef class _Nearest:
    cdef InterpFunctor[Nearest]* _thisptr

cdef class _Linear:
    cdef InterpFunctor[Linear]* _thisptr

cdef class _Keys:
    cdef InterpFunctor[Keys]* _thisptr

cdef class _Bspline3:
    cdef InterpFunctor[Bspline3]* _thisptr

cdef class _Bspline4:
    cdef InterpFunctor[Bspline4]* _thisptr

cdef class _Bspline5:
    cdef InterpFunctor[Bspline5]* _thisptr

cdef class _Omoms3:
    cdef InterpFunctor[Omoms3]* _thisptr

ctypedef fused interp_type:
    _Nearest
    _Linear
    _Keys
    _Bspline3
    _Bspline4
    _Bspline5
    _Omoms3
