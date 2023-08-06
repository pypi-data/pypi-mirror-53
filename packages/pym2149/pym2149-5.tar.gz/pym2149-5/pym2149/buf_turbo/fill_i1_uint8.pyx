# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fill_i1_uint8(self, np.int8_t value):
    cdef np.ndarray[np.uint8_t] py_self_buf = self.buf
    cdef np.uint8_t* self_buf = &py_self_buf[0]
    cdef np.uint8_t v
    cdef np.uint32_t i
    v = value # Cast once.
    for i in range(py_self_buf.size):
        self_buf[i] = v
