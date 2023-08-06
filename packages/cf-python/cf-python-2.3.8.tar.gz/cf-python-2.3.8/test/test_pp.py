import atexit
import datetime
import os
import tempfile
import time
import unittest

import numpy

import cf

tmpfile  = tempfile.mktemp('.cf-python_test')
tmpfiles = [tmpfile]
def _remove_tmpfiles():
    '''
'''
    for f in tmpfiles:
        try:
            os.remove(f)
        except OSError:
            pass
#--- End: def
atexit.register(_remove_tmpfiles)

class ppTest(unittest.TestCase):
    def setUp(self):
        self.ppfilename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       'wgdos_packed.pp')

        self.new_table = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'new_STASH_to_CF.txt')

        text_file = open(self.new_table, 'w')
        text_file.write('1!24!SURFACE TEMPERATURE AFTER TIMESTEP  !Pa!!!NEW_NAME!!')
        text_file.close()
        
        self.chunk_sizes = (17, 34, 300, 100000)[::-1]
        self.original_chunksize = cf.CHUNKSIZE()
        self.test_only = ()
    #--- End: def

    def test_PP_load_stash2standard_name(self):
        f = cf.read(self.ppfilename)[0]
        self.assertTrue(f.name() == 'surface_temperature')
        self.assertTrue(f.Units == cf.Units('K'))
        for merge in (True, False):
            cf.um.read.load_stash2standard_name(self.new_table, merge=merge)
            f = cf.read(self.ppfilename)[0]
            self.assertTrue(f.name() == 'NEW_NAME')
            self.assertTrue(f.Units == cf.Units('Pa'))
            cf.um.read.load_stash2standard_name()
            f = cf.read(self.ppfilename)[0]
            self.assertTrue(f.name() == 'surface_temperature')
            self.assertTrue(f.Units == cf.Units('K'))
        #--- End: for
        cf.um.read.load_stash2standard_name()
    #--- End: def

    def test_PP_WGDOS_UNPACKING(self):
        f = cf.read(self.ppfilename)[0]

        self.assertTrue(f.min() > 221.71,
                        'Bad unpacking of WGDOS packed data')
        self.assertTrue(f.max() < 310.45,
                        'Bad unpacking of WGDOS packed data')
        
        array = f.array
    
        for chunksize in self.chunk_sizes:   
            cf.CHUNKSIZE(chunksize) 

            f = cf.read(self.ppfilename)[0]

            for fmt in ('NETCDF4', 'CFA4'):
                cf.write(f, tmpfile, fmt=fmt)
                g = cf.read(tmpfile)[0]

                self.assertTrue((f.array == array).all(),
                                'Bad unpacking of WGDOS packed data')

                self.assertTrue(f.equals(g, traceback=True),
                                'Bad writing/reading. format='+fmt)
        #--- End: for
        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def

#--- End: class

if __name__ == '__main__':
    print 'Run date:', datetime.datetime.utcnow()
    cf.environment()
    print
    unittest.main(verbosity=2)
