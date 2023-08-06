# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def correlate(np.ndarray[np.int32_t] py_kernel, np.uint32_t kernelsize, np.ndarray[np.int32_t] py_history, np.uint32_t maxphase):
    cdef np.int32_t* kernel = &py_kernel[0]
    cdef np.int32_t* history = &py_history[0]
    cdef np.uint32_t phase
    cdef np.int32_t score
    cdef np.uint32_t j
    cdef np.uint32_t i
    cdef np.uint32_t p
    cdef np.int32_t s
    phase = 0
    score = 0
    j = maxphase
    for i in range(kernelsize):
        score += kernel[i] * history[j]
        j += 1
    for p in range(1, maxphase + 1):
        s = 0
        j = maxphase - p
        for i in range(kernelsize):
            s += kernel[i] * history[j]
            j += 1
        if s > score:
            phase = p
            score = s
    return phase, score
