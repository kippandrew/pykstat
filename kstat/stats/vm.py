import ctypes as CTYPES 

#typedef struct vminfo {		/* (update freq) update action		*/
#	uint64_t freemem; 	/* (1 sec) += freemem in pages		*/
#	uint64_t swap_resv;	/* (1 sec) += reserved swap in pages	*/
#	uint64_t swap_alloc;	/* (1 sec) += allocated swap in pages	*/
#	uint64_t swap_avail;	/* (1 sec) += unreserved swap in pages	*/
#	uint64_t swap_free;	/* (1 sec) += unallocated swap in pages	*/
#	uint64_t updates;	/* (1 sec) ++				*/
#} vminfo_t;

class vminfo_t(CTYPES.Structure):
    _fields_ = [
        ('freemem', CTYPES.c_uint64),
        ('swap_resv', CTYPES.c_uint64),
        ('swap_alloc', CTYPES.c_uint64),
        ('swap_avail', CTYPES.c_uint64),
        ('swap_free', CTYPES.c_uint64),
        ('updates', CTYPES.c_uint64)
    ]

vminfo_t_p = CTYPES.POINTER(vminfo_t)
