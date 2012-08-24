import ctypes as CTYPES 

#typedef struct sysinfo {    /* (update freq) update action      */
#    uint_t  updates;    /* (1 sec) ++               */
#    uint_t  runque;     /* (1 sec) += num runnable procs    */
#    uint_t  runocc;     /* (1 sec) ++ if num runnable procs > 0 */
#    uint_t  swpque;     /* (1 sec) += num swapped procs     */
#    uint_t  swpocc;     /* (1 sec) ++ if num swapped procs > 0  */
#    uint_t  waiting;    /* (1 sec) += jobs waiting for I/O  */
#} sysinfo_t;

class sysinfo_t(CTYPES.Structure):
    _fields_ = [
        ('updates', CTYPES.c_uint),
        ('runque', CTYPES.c_uint),
        ('runocc', CTYPES.c_uint),
        ('swpque', CTYPES.c_uint),
        ('swpocc', CTYPES.c_uint),
        ('waiting', CTYPES.c_uint)
    ]

sysinfo_p = CTYPES.POINTER(sysinfo_t)

