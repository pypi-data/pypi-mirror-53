# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fillpart_int64(self, np.uint32_t startframe, np.uint32_t endframe, np.int64_t value):
    cdef np.ndarray[np.int64_t] py_self_buf = self.buf
    cdef np.int64_t* self_buf = &py_self_buf[0]
    while startframe < endframe:
        self_buf[startframe] = value
        startframe += 1
