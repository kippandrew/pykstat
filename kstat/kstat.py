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
    
    def __init__(self, kstat, kstat_data_type):
        # cast kstat data to data type
        self._kstat = kstat
        if self._kstat != None and self._kstat.ks_data != None:
            self._kstat_data_p = CTYPES.cast(kstat.ks_data, CTYPES.POINTER(kstat_data_type))
        else:
            self._kstat_data_p = None

    @property
    def module(self):
        return self._kstat.ks_module 

    @property
    def instance(self):
        return self._kstat.ks_instance 
    
    @property
    def name(self):
        return self._kstat.ks_name 

    @property
    def data(self):
        return self._kstat_data_p

    @property
    def data_count(self):
        return self._kstat.ks_ndata

    @property
    def data_type(self):
        return libkstat.kstat_type_names[self._kstat.ks_type] 

    @property
    def data_class(self):
        return self._kstat.ks_class 

    def __repr__(self):
        return str({'module': self.module, 'instance': self.instance, 'name': self.name, 'type': self.data_type, 'class': self.data_class, 'data': self.data})

class KstatNamedData(KstatData):
    def __init__(self, kstat):
        # Initialize superclass 
        KstatData.__init__(self, kstat, libkstat._kstat_named_t) 
        
        self._values = dict()
        for i in range(self.data_count):
            if self.data[i].data_type == libkstat.KSTAT_DATA_CHAR:
                self._values[self.data[i].name] = self.data[i].value.c
            elif self.data[i].data_type == libkstat.KSTAT_DATA_INT32:
                self._values[self.data[i].name] = self.data[i].value.i32
            elif self.data[i].data_type == libkstat.KSTAT_DATA_UINT32:
                self._values[self.data[i].name] = self.data[i].value.ui32
            elif self.data[i].data_type == libkstat.KSTAT_DATA_INT64:
                self._values[self.data[i].name] = self.data[i].value.i64
            elif self.data[i].data_type == libkstat.KSTAT_DATA_UINT64:
                self._values[self.data[i].name] = self.data[i].value.ui64
 
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
        # Initialize superclass 
        KstatData.__init__(self, kstat, libkstat._kstat_io_t) 
 
    def __getitem__(self, k):
        if not hasattr(self.data.contents, k):
            raise KeyError()
        attr = getattr(self.data.contents, k)
        return attr 

class KstatRawData(KstatData):
    def __init__(self, kstat, raw_data_type):
        # Initialize superclass 
        KstatData.__init__(self, kstat, raw_data_type)

    def __getitem__(self, k):
        if not hasattr(self.data.contents, k):
            raise KeyError()
        attr = getattr(self.data.contents, k)
        return attr 

def main():
    k = Kstat()
    import stats
    print k.retrieve('unix', 0, 'sysinfo', stats.sysinfo_t)['runque']
    print k.retrieve('cpu_stat', 0, 'cpu_stat0', stats.cpu_sys_stats_t)['cpu_ticks_user']
    print k.retrieve('sd', 0, 'sd0')
    #print list(k.retrieve_all('lgrp', -1, None))
    #print k.read(kstat_p)
    #print k.read(kstat_p) 
    #print k.dump()

if __name__ == '__main__':
    main()
