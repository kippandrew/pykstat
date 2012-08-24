#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Copyright 2011 Grigale Ltd. All rigths reserved.
# Use is sujbect to license terms.
#
import ctypes as CTYPES 

KSTAT_TYPE_RAW = 0
KSTAT_TYPE_NAMED = 1
KSTAT_TYPE_INTR = 2
KSTAT_TYPE_IO = 3
KSTAT_TYPE_TIMER = 4

kstat_type_names = {
    KSTAT_TYPE_RAW: 'raw', KSTAT_TYPE_NAMED: 'named',
    KSTAT_TYPE_INTR: 'intr', KSTAT_TYPE_IO: 'io', KSTAT_TYPE_TIMER: 'timer'
    }

KSTAT_STRLEN = 31

kstat_string = CTYPES.c_char * KSTAT_STRLEN
hrtime_t = CTYPES.c_longlong
kid_t = CTYPES.c_int

#typedef struct kstat {
#        /*
#         * Fields relevant to both kernel and user
#         */
#        hrtime_t        ks_crtime;      /* creation time (from gethrtime()) */
#        struct kstat    *ks_next;       /* kstat chain linkage */
#        kid_t           ks_kid;         /* unique kstat ID */
#        char            ks_module[KSTAT_STRLEN]; /* provider module name */
#        uchar_t         ks_resv;        /* reserved, currently just padding */
#        int             ks_instance;    /* provider module's instance */
#        char            ks_name[KSTAT_STRLEN]; /* kstat name */
#        uchar_t         ks_type;        /* kstat data type */
#        char            ks_class[KSTAT_STRLEN]; /* kstat class */
#        uchar_t         ks_flags;       /* kstat flags */
#        void            *ks_data;       /* kstat type-specific data */
#        uint_t          ks_ndata;       /* # of type-specific data records */
#        size_t          ks_data_size;   /* total size of kstat data section */
#        hrtime_t        ks_snaptime;    /* time of last data shapshot */
#        /*
#         * Fields relevant to kernel only
#         */
#        int             (*ks_update)(struct kstat *, int); /* dynamic update */
#        void            *ks_private;    /* arbitrary provider-private data */
#        int             (*ks_snapshot)(struct kstat *, void *, int);
#        void            *ks_lock;       /* protects this kstat's data */
#} kstat_t;

class _kstat_t(CTYPES.Structure):
    pass

_kstat_t_p = CTYPES.POINTER(_kstat_t)

_kstat_t._fields_ = [
    ('ks_crtime', hrtime_t),
    ('ks_next', _kstat_t_p),
    ('ks_kid', kid_t),
    ('ks_module', kstat_string),
    ('ks_resv', CTYPES.c_ubyte),
    ('ks_instance', CTYPES.c_int),
    ('ks_name', kstat_string),
    ('ks_type', CTYPES.c_ubyte),
    ('ks_class', kstat_string),
    ('ks_flags', CTYPES.c_ubyte),
    ('ks_data', CTYPES.c_void_p),
    ('ks_ndata', CTYPES.c_uint),
    ('ks_data_size', CTYPES.c_size_t),
    ('ks_snaptime', hrtime_t),

    ('ks_update', CTYPES.c_void_p),
    ('ks_private', CTYPES.c_void_p),
    ('ks_snapshot', CTYPES.c_void_p),
    ('ks_lock', CTYPES.c_void_p)
]

#typedef struct kstat_ctl {
#        kid_t   kc_chain_id;    /* current kstat chain ID       */
#        kstat_t *kc_chain;      /* pointer to kstat chain       */
#        int     kc_kd;          /* /dev/kstat descriptor        */
#} kstat_ctl_t;

class _kstat_ctl_t(CTYPES.Structure):
    _fields_ = [
        ('kc_chain_id', kid_t),
        ('kc_chain', _kstat_t_p),
        ('kc_kd', CTYPES.c_int)
    ]

_kstat_ctl_t_p = CTYPES.POINTER(_kstat_ctl_t)

#typedef struct kstat_named {
#        char    name[KSTAT_STRLEN];     /* name of counter */
#        uchar_t data_type;              /* data type */
#        union {
#                char            c[16];  /* enough for 128-bit ints */
#                int32_t         i32;
#                uint32_t        ui32;
#                struct {
#                        union {
#                                char            *ptr;   /* NULL-term string */
#                                char            __pad[8]; /* 64-bit padding */
#                        } addr;
#                        uint32_t        len;    /* # bytes for strlen + '\0' */
#                } str;
##if defined(_INT64_TYPE)
#                int64_t         i64;
#                uint64_t        ui64;
##endif
#                long            l;
#                ulong_t         ul;
#
#                /* These structure members are obsolete */
#
#                longlong_t      ll;
#                u_longlong_t    ull;
#                float           f;
#                double          d;
#        } value;                        /* value of counter */
#} kstat_named_t;

KSTAT_DATA_CHAR = 0
KSTAT_DATA_INT32 = 1
KSTAT_DATA_UINT32 = 2
KSTAT_DATA_INT64 = 3
KSTAT_DATA_UINT64 = 4
KSTAT_DATA_STRING = 9

class addr_union(CTYPES.Union):
    _fields_ = [
        ('ptr', CTYPES.c_char_p),
        ('__pad', CTYPES.c_char * 8),
    ]

class str_struct(CTYPES.Structure):
    _fields_ = [
        ('addr', addr_union),
        ('len', CTYPES.c_uint32),
    ]

class value_union(CTYPES.Union):
    _fields_ = [
        ('c', CTYPES.c_char * 16),
	('i32', CTYPES.c_int32),
	('ui32', CTYPES.c_uint32),
	('i64', CTYPES.c_int64),
	('ui64', CTYPES.c_uint64),
    ]

class _kstat_named_t(CTYPES.Structure):
    _fields_ = [
        ('name', kstat_string),
        ('data_type', CTYPES.c_ubyte),
        ('value', value_union),
    ]

#typedef struct kstat_io {  
# /*  
# * Basic counters.  
# */  
#  u_longlong_t nread;    /* number of bytes read */  
#  u_longlong_t nwritten; /* number of bytes written */  
#  uint_t       reads;    /* number of read operations */  
#  uint_t       writes;   /* number of write operations */  
#  hrtime_t wtime;           /* cumulative wait (pre-service) time */  
#  hrtime_t wlentime;        /* cumulative wait length*time product*/  
#  hrtime_t wlastupdate;     /* last time wait queue changed */  
#  hrtime_t rtime;           /* cumulative run (service) time */  
#  hrtime_t rlentime;        /* cumulative run length*time product */  
#  hrtime_t rlastupdate;     /* last time run queue changed */  
#  uint_t wcnt;              /* count of elements in wait state */  
#  uint_trcnt;              /* count of elements in run state */  
#} kstat_io_t;

class _kstat_io_t(CTYPES.Structure):
    _fields_ = [
        ('nread', CTYPES.c_ulonglong),
        ('nwritten', CTYPES.c_ulonglong),
        ('reads', CTYPES.c_uint),
        ('writes', CTYPES.c_uint),
        ('wtime', hrtime_t),
        ('wlentime', hrtime_t),
        ('wlastupdate', hrtime_t),
        ('rtime', hrtime_t),
        ('rlentime', hrtime_t),
        ('rlastupdate', hrtime_t), 
        ('wcnt', CTYPES.c_uint),
        ('rcnt', CTYPES.c_uint) 
    ]

_kstat_io_t_p = CTYPES.POINTER(_kstat_io_t)

_libkstat = CTYPES.CDLL('libkstat.so.1')

kstat_open = _libkstat.kstat_open
kstat_open.argtypes = []
kstat_open.restype = _kstat_ctl_t_p

kstat_close = _libkstat.kstat_close
kstat_close.argtypes = [_kstat_ctl_t_p]

kstat_read = _libkstat.kstat_read
kstat_read.argtypes = [_kstat_ctl_t_p, _kstat_t_p, CTYPES.c_void_p]
kstat_read.restype = kid_t

kstat_write = _libkstat.kstat_write
kstat_write.argtypes = [_kstat_ctl_t_p, _kstat_t_p, CTYPES.c_void_p]
kstat_write.restype = kid_t

kstat_chain_update = _libkstat.kstat_chain_update
kstat_chain_update.argtypes = [_kstat_ctl_t_p]
kstat_chain_update.restype = kid_t

kstat_lookup = _libkstat.kstat_lookup
kstat_lookup.argtypes = [_kstat_ctl_t_p, CTYPES.c_char_p, CTYPES.c_int, CTYPES.c_char_p]
kstat_lookup.restype = _kstat_t_p

kstat_data_lookup = _libkstat.kstat_data_lookup
kstat_data_lookup.argtypes = [_kstat_t_p]
kstat_data_lookup.restype = CTYPES.c_void_p
