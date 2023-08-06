# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def copywindow_int64(self, that, np.uint32_t startframe, np.uint32_t endframe):
    cdef np.ndarray[np.int64_t] py_self_buf = self.buf
    cdef np.int64_t* self_buf = &py_self_buf[0]
    cdef np.ndarray[np.int64_t] py_that_buf = that.buf
    cdef np.int64_t* that_buf = &py_that_buf[0]
    cdef np.uint32_t i
    for i in range(endframe - startframe):
        self_buf[i] = that_buf[startframe]
        startframe += 1
