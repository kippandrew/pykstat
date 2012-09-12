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

import pprint
import ctypes as CTYPES
import libkstat

class Kstat():
    def __init__(self):
        self._kstat_ctl = libkstat.kstat_open()

    def __del__(self):
        libkstat.kstat_close(self._kstat_ctl)

    def write(self):
        pass

    def read(self, kstat_p, raw_data_type=None):
        libkstat.kstat_read(self._kstat_ctl, kstat_p, None)
        kstat = kstat_p.contents  
        # kstat can store multiple types of data, return the appropriate type 
        if kstat.ks_type == libkstat.KSTAT_TYPE_RAW:
            if not raw_data_type:
                raise TypeError('raw_data_type not specified for ks_type = KSTAT_TYPE_RAW')
            return KstatRawData(kstat, raw_data_type)
        elif kstat.ks_type == libkstat.KSTAT_TYPE_NAMED:
            return KstatNamedData(kstat)
        elif kstat.ks_type == libkstat.KSTAT_TYPE_INTR:
            return KstatIntrData(kstat) 
        elif kstat.ks_type == libkstat.KSTAT_TYPE_IO:
            return KstatIOData(kstat) 
        elif kstat.ks_type == libkstat.KSTAT_TYPE_TIMER:
            pass
        else:
            pass
        return value

    def update(self):
        libkstat.kstat_chain_update(self._kstat_ctl)
    
    def lookup(self, module, instance, name):
        kstat_p = libkstat.kstat_lookup(self._kstat_ctl, module, instance, name)
        if kstat_p is None:
            return KeyError((module, instance, name))
        return kstat_p

    def retrieve_all(self, module, instance, name, raw_data_type=None):
        kstat_p = self.lookup(module, instance, name)
        ksp = kstat_p
        while ksp:
            ks = ksp.contents
            match = True 
            if module and ks.ks_module != module:
                match = False  
            if name and ks.ks_name != name:
                match = False 
            if instance >= 0 and ks.ks_instance != instance:
                match = False
            if match:
                yield self.read(ksp, raw_data_type)
            ksp = ksp.contents.ks_next

    def retrieve(self, module, instance, name, raw_data_type=None):
        kstat_p = self.lookup(module, instance, name)
        return self.read(kstat_p, raw_data_type)

    def dump_kstat_info(self, kstat_p):
        ksp = kstat_p
        while ksp:
            ks = ksp.contents
            print ks.ks_module, ks.ks_instance, ks.ks_name, libkstat.kstat_type_names[ks.ks_type], ks.ks_class, ks.ks_ndata, ks.ks_data_size
            ksp = ks.ks_next

class KstatData():
    pass

class KstatNamedData(KstatData):
    def __init__(self, kstat):
        self._kstat_data_p = CTYPES.cast(kstat.ks_data, CTYPES.POINTER(libkstat._kstat_named_t))
        self._kstat_data = self._kstat_data_p.contents
        self._values = dict()
        for i in range(kstat.ks_ndata):
            if self._kstat_data_p[i].data_type == libkstat.KSTAT_DATA_CHAR:
                self.values[self._kstat_data_p[i].name] = self._kstat_data_p[i].value.c
            elif self._kstat_data_p[i].data_type == libkstat.KSTAT_DATA_INT32:
                self.values[self._kstat_data_p[i].name] = self._kstat_data_p[i].value.i32
            elif self._kstat_data_p[i].data_type == libkstat.KSTAT_DATA_UINT32:
                self._values[self._kstat_data_p[i].name] = self._kstat_data_p[i].value.ui32
            elif self._kstat_data_p[i].data_type == libkstat.KSTAT_DATA_INT64:
                self._values[self._kstat_data_p[i].name] = self._kstat_data_p[i].value.i64
            elif self._kstat_data_p[i].data_type == libkstat.KSTAT_DATA_UINT64:
                self._values[self._kstat_data_p[i].name] = self._kstat_data_p[i].value.ui64
    
    def __len__(self):
        return len(self._values)

    def __getitem__(self, k):
        return self._values[k]

    def __iter__(self):
        for i in self._values:
            yield i 

    def __repr__(self):
        return str(self._values)

class KstatIOData(KstatData):
    def __init__(self, kstat):
        self._kstat_data_p = CTYPES.cast(kstat.ks_data, CTYPES.POINTER(libkstat._kstat_io_t))
        self._kstat_data = self._kstat_data_p.contents
        print self._kstat_data   
 
    def __len__(self):
        return len(self._kstat_data)

    def __getitem__(self, k):
        pass

class KstatRawData(KstatData):
    def __init__(self, kstat, raw_data_type):
        self._kstat_data_p = CTYPES.cast(kstat.ks_data, CTYPES.POINTER(raw_data_type))
        self._kstat_data = self._kstat_data_p.contents

    def __getitem__(self, k):
        attr = getattr(self._kstat_data, k)
        return attr 

def main():
    k = Kstat()
    #print k.retrieve('unix', 0, 'sysinfo', sysinfo_t)['runque']
    #print k.retrieve('cpu_stat', 0, 'cpu_stat0', cpu_sys_stats_t)['cpu_ticks_user']
    #print k.retrieve('sd', 0, 'sd1')
    #print list(k.retrieve_all('lgrp', -1, None))
    #print k.read(kstat_p)
    #print k.read(kstat_p) 
    #print k.dump()

if __name__ == '__main__':
    main()
