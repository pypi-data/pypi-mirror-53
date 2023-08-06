# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def mapbuf_int16(self, that, np.ndarray[np.int16_t] py_lookup):
    cdef np.ndarray[np.int16_t] py_self_buf = self.buf
    cdef np.int16_t* self_buf = &py_self_buf[0]
    cdef np.ndarray[np.uint8_t] py_that_buf = that.buf
    cdef np.uint8_t* that_buf = &py_that_buf[0]
    cdef np.int16_t* lookup = &py_lookup[0]
    cdef np.uint32_t i
    for i in range(py_that_buf.size):
        self_buf[i] = lookup[that_buf[i]]
