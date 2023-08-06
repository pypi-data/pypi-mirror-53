import nose.tools as nt
import stopwatch.stopwatch as sw
import unittest
import time
import stopwatch.utilityfunctions as uf

#see if you can use the with statement in here
#look up and understand unittest
#look up and understand nose.tools

class TestStopwatch(unittest.TestCase):
    
    def setUp(self):
        self.fake_time = uf.make_fake_time_function(range(10000))
        self.mytimer = sw.Stopwatch(self.fake_time)
    
    def test_init(self):
        nt.assert_equal(self.mytimer._stop_time, 0)
        nt.assert_equal(self.mytimer.elapsed_time, 0)
        nt.assert_equal(self.mytimer._start_time, None)
        nt.assert_equal(self.mytimer._now, self.fake_time)
        nt.assert_equal(self.mytimer.elapsed(), 0)
        
    def test_start_timer(self):
        self.mytimer.start_timer()
        
        nt.assert_equal(self.mytimer._start_time, 0)
        nt.assert_true(self.mytimer._start_time is not None)
        nt.assert_raises(RuntimeError, self.mytimer.start_timer)
        
    def test_stop_timer(self):
        self.mytimer.start_timer()
        self.mytimer.stop_timer()
        
        nt.assert_equal(self.mytimer._stop_time, 1)
        nt.assert_true(self.mytimer._start_time is None)
        nt.assert_equal(self.mytimer.elapsed(), 1)
        
        self.mytimer.start_timer()
        self.mytimer.stop_timer()
        
        nt.assert_equal(self.mytimer.elapsed(), 2)
        nt.assert_raises(RuntimeError, self.mytimer.stop_timer)
        
    def test_elapsed(self):
        self.mytimer.start_timer()
        self.mytimer.stop_timer()
        
        nt.assert_equal(self.mytimer.elapsed(), 1)
        
        self.mytimer.start_timer()
        
        nt.assert_equal(self.mytimer.elapsed(), 2)
        nt.assert_equal(self.mytimer.elapsed(), 3)
        
        self.mytimer.stop_timer()
        
        nt.assert_equal(self.mytimer.elapsed(), 4)
        
    def test_reset(self):
        self.mytimer.start_timer()
        self.mytimer.stop_timer()
        self.mytimer.start_timer()
        self.mytimer.stop_timer()
        
        nt.assert_equal(self.mytimer.elapsed(), 2)
        nt.assert_equal(self.mytimer._start_time, None)
        nt.assert_equal(self.mytimer._stop_time, 3)
        
        self.mytimer.reset()
        
        nt.assert_equal(self.mytimer._start_time, None)
        nt.assert_equal(self.mytimer._stop_time, 0)
        nt.assert_equal(self.mytimer.elapsed_time, 0)
        
if __name__ == '__main__':
    unittest.main()



