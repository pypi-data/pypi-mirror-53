import nose.tools as nt
import stopwatch.stopwatch as sw
import stopwatch.countdown as cd
import unittest
import time
import stopwatch.utilityfunctions as uf

class TestCountdown(unittest.TestCase):
    
    def setUp(self):
        self.fake_time = uf.make_fake_time_function(range(10000))
        self.countdown = cd.Countdown(self.fake_time)
        self.countdown.countdowntime = (0, 0, 10, 0)
        
    def test_init(self):
        nt.assert_true(isinstance(self.countdown.timer, sw.Stopwatch))
        nt.assert_equal(self.countdown.countdowntime, 10)
        
    def test_start_countdown(self):
        self.countdown.start_countdown()
        nt.assert_true(self.countdown.timer.running)
        
    def test_stop_countdown(self):
        with nt.assert_raises(RuntimeError):
            self.countdown.stop_countdown()
        self.countdown.start_countdown()
        self.countdown.stop_countdown()
        nt.assert_false(self.countdown.timer.running)
        
    def test_time_remaining(self):
        self.countdown.start_countdown()
        self.countdown.stop_countdown()
        nt.assert_equal(self.countdown.time_remaining(), 9)
        self.countdown.start_countdown()
        self.countdown.stop_countdown()
        nt.assert_equal(self.countdown.time_remaining(), 8)
        
    def test_reset_countdown(self):
        self.countdown.start_countdown()
        self.countdown.stop_countdown()
        nt.assert_true(self.countdown.time_remaining() != 10)
        self.countdown.reset_countdown()
        nt.assert_equal(self.countdown.time_remaining(), 10)
        
        
    def test_countdowntime_setter(self):
        nt.assert_equal(self.countdown.countdowntime, 10)
        nt.assert_raises(TypeError, self.countdown.countdowntime, 15)
        self.countdown.countdowntime = (0, 0, 15, 0)
        nt.assert_equal(self.countdown.countdowntime, 15)
        
    def test_context_manager(self):
        with self.countdown:
            nt.assert_true(self.countdown.timer.running)
        nt.assert_false(self.countdown.timer.running)
        
if __name__ == '__main__':
    unittest.main()

