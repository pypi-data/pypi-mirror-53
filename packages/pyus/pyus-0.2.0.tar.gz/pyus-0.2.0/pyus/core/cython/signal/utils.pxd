from libcpp.string cimport string
from libcpp.vector cimport vector
from pyus.core.cython.utils.types cimport complex

cdef extern from "pulse/signal/utils.h" namespace "pulse":

    void magnitude_host(float complex* input, size_t size, float* output);

    void magnitude_device(complex[float]* input, size_t size, float* output);

    void env2bmode_host(float* env, size_t len_env, size_t nb_batches,
                          string norm, float* norm_factors, float* bmode)

    void env2bmode_device(float* env, size_t len_env, size_t nb_batches,
                            string norm, float* norm_factors, float* bmode)

    void iq2bmode_host(
            float complex* iq_data, size_t len_data, size_t nb_batches,
            string norm, float* norm_factors, float* bmode
    )

    void iq2bmode_device(
            complex[float]* iq_data, size_t len_data, size_t nb_batches,
            string norm, float* norm_factors, float* bmode
    )

    void rf2bmode_host(
            float* rf_data, size_t len_data, size_t nb_batches,
            vector[float complex] fir_filter, string norm,
            float* norm_factors, float* bmode
    )

    void rf2bmode_device(
            float* rf_data, size_t len_data, size_t nb_batches,
            vector[float complex] fir_filter, string norm,
            float* norm_factors, float* bmode
    )
