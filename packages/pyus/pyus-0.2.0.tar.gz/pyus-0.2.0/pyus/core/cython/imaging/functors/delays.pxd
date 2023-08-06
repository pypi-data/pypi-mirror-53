from pyus.core.cython.utils.types cimport float3
cimport cython

cdef extern from "pulse/delay_law/delay_law.h" namespace "pulse":
    cdef:
        cppclass PlaneWave2D:
            PlaneWave2D()
            PlaneWave2D(
                    float mean_sound_speed,
                    float angle,
                    float offset
            )
            float operator()(float3 pos_im, float3 pos_td)

        cppclass PlaneWave3D:
            PlaneWave3D()
            PlaneWave3D(
                    float mean_sound_speed,
                    float angle_x,
                    float angle_y,
                    float offset
            )
            float operator()(float3 pos_im, float3 pos_td)

        cppclass DivergingWave:
            DivergingWave()
            DivergingWave(
                    float mean_sound_speed,
                    float3 virtual_source,
                    float offset
            )
            float operator()(float3 pos_im, float3 pos_td)


cdef class _PlaneWave2D:
    cdef PlaneWave2D* _thisptr

cdef class _PlaneWave3D:
    cdef PlaneWave3D* _thisptr

cdef class _DivergingWave2D:
    cdef DivergingWave* _thisptr

ctypedef fused delay_type:
    _PlaneWave2D
    _PlaneWave3D
    _DivergingWave2D
