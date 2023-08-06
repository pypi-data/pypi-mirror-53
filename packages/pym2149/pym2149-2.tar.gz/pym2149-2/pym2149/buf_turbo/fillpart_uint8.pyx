# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fillpart_uint8(self, np.uint32_t startframe, np.uint32_t endframe, np.uint8_t value):
    cdef np.ndarray[np.uint8_t] py_self_buf = self.buf
    cdef np.uint8_t* self_buf = &py_self_buf[0]
    while startframe < endframe:
        self_buf[startframe] = value
        startframe += 1
