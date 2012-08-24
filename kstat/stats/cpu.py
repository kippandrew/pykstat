import ctypes as CTYPES

#typedef struct cpu_sys_stats {
#    uint64_t cpu_ticks_idle;    /* CPU utilization */
#    uint64_t cpu_ticks_user;
#    uint64_t cpu_ticks_kernel;
#    uint64_t cpu_ticks_wait;
#    uint64_t wait_ticks_io;     /* CPU wait time breakdown */
#    uint64_t bread;         /* physical block reads */
#    uint64_t bwrite;        /* physical block writes (sync+async) */
#    uint64_t lread;         /* logical block reads */
#    uint64_t lwrite;        /* logical block writes */
#    uint64_t phread;        /* raw I/O Reads */
#    uint64_t phwrite;       /* raw I/O writes */
#    uint64_t pswitch;       /* context switches */
#    uint64_t trap;          /* traps */
#    uint64_t intr[PIL_MAX];     /* device interrupts per PIL */
#    uint64_t syscall;       /* system calls */
#    uint64_t sysread;       /* read() + readv() system calls */
#    uint64_t syswrite;      /* write() + writev() system calls */
#    uint64_t sysfork;       /* forks */
#    uint64_t sysvfork;      /* vforks */
#    uint64_t sysexec;       /* execs */
#    uint64_t readch;        /* bytes read by rdwr() */
#    uint64_t writech;       /* bytes written by rdwr() */
#    uint64_t rcvint;        /* XXX: unused (mostly) */
#    uint64_t xmtint;        /* XXX: unused */
#    uint64_t mdmint;        /* XXX: unused */
#    uint64_t rawch;         /* terminal input characters */
#    uint64_t canch;         /* chars handled in canonical mode */
#    uint64_t outch;         /* terminal output characters */
#    uint64_t msg;           /* msg count (msgrcv() + msgsnd()) */
#    uint64_t sema;          /* semaphore ops count (semop()) */
#    uint64_t namei;         /* pathname lookups */
#    uint64_t ufsiget;       /* ufs_iget() calls */
#    uint64_t ufsdirblk;     /* directory blocks read */
#    uint64_t ufsipage;      /* inodes taken with attached pages */
#    uint64_t ufsinopage;        /* inodes taken with no attached pgs */
#    uint64_t procovf;       /* failed forks */
#    uint64_t intrblk;       /* ints blkd/prempted/rel'd (swtch) */
#    uint64_t intrunpin;     /* intr thread unpins pinned thread */
#    uint64_t idlethread;        /* times idle thread scheduled */
#    uint64_t inv_swtch;     /* involuntary context switches */
#    uint64_t nthreads;      /* thread_create()s */
#    uint64_t cpumigrate;        /* cpu migrations by threads */
#    uint64_t xcalls;        /* xcalls to other cpus */
#    uint64_t mutex_adenters;    /* failed mutex enters (adaptive) */
#    uint64_t rw_rdfails;        /* rw reader failures */
#    uint64_t rw_wrfails;        /* rw writer failures */
#    uint64_t modload;       /* times loadable module loaded */
#    uint64_t modunload;         /* times loadable module unloaded */
#    uint64_t bawrite;       /* physical block writes (async) */
#    uint64_t iowait;        /* count of waiters for block I/O */
#} cpu_sys_stats_t;

PIL_MAX = 15

class cpu_sys_stats_t(CTYPES.Structure):
    _fields_ = [
        ('cpu_ticks_idle', CTYPES.c_uint64),
        ('cpu_ticks_user', CTYPES.c_uint64),
        ('cpu_ticks_kernel', CTYPES.c_uint64),
        ('cpu_ticks_wait', CTYPES.c_uint64),
        ('wait_ticks_io', CTYPES.c_uint64), 
        ('bread', CTYPES.c_uint64),
        ('bwrite', CTYPES.c_uint64),
        ('lread', CTYPES.c_uint64), 
        ('lwrite', CTYPES.c_uint64), 
        ('phread', CTYPES.c_uint64), 
        ('phwrite', CTYPES.c_uint64),  
        ('pswitch', CTYPES.c_uint64), 
        ('trap', CTYPES.c_uint64), 
        ('intr', CTYPES.c_uint64 * PIL_MAX),
        ('syscall', CTYPES.c_uint64),  
        ('sysread', CTYPES.c_uint64),  
        ('syswrite', CTYPES.c_uint64), 
        ('sysfork', CTYPES.c_uint64),  
        ('sysvfork', CTYPES.c_uint64),  
        ('sysexec', CTYPES.c_uint64), 
        ('readch', CTYPES.c_uint64), 
        ('writech', CTYPES.c_uint64), 
        ('rcvint', CTYPES.c_uint64), 
        ('xmtint', CTYPES.c_uint64), 
        ('mdmint', CTYPES.c_uint64), 
        ('rawch', CTYPES.c_uint64), 
        ('canch', CTYPES.c_uint64), 
        ('outch', CTYPES.c_uint64), 
        ('msg', CTYPES.c_uint64), 
        ('sema', CTYPES.c_uint64), 
        ('namei', CTYPES.c_uint64), 
        ('ufsiget', CTYPES.c_uint64), 
        ('ufsdirblk', CTYPES.c_uint64), 
        ('ufsipage', CTYPES.c_uint64), 
        ('ufsinopage', CTYPES.c_uint64), 
        ('procovf', CTYPES.c_uint64), 
        ('intrblk', CTYPES.c_uint64), 
        ('intrunpin', CTYPES.c_uint64), 
        ('idlethread', CTYPES.c_uint64), 
        ('inv_swtch', CTYPES.c_uint64), 
        ('nthreads', CTYPES.c_uint64), 
        ('cpumigrate', CTYPES.c_uint64), 
        ('xcalls', CTYPES.c_uint64), 
        ('mutex_adenters', CTYPES.c_uint64), 
        ('rw_rdfails', CTYPES.c_uint64), 
        ('rw_wrfails', CTYPES.c_uint64), 
        ('modload', CTYPES.c_uint64), 
        ('modunload', CTYPES.c_uint64), 
        ('bawrite', CTYPES.c_uint64), 
        ('iowait', CTYPES.c_uint64)
    ]

cpu_sys_stats_t_p = CTYPES.POINTER(cpu_sys_stats_t)
