#pomodoro testing module

import nose.tools as nt
import stopwatch.stopwatch as sw
import unittest
import stopwatch.countdown as ct
import stopwatch.pomodoro as pom
import stopwatch.utilityfunctions as uf

class TestPomodoro(unittest.TestCase):
    
    def setUp(self):
        self.mypom = pom.Pomodoro()
        
    def test_init(self):
        nt.assert_true(isinstance(self.mypom.work_countdown, ct.Countdown))
        nt.assert_true(isinstance(self.mypom.break_countdown, ct.Countdown))
        nt.assert_equal(self.mypom.rounds_before_break, 4)
        nt.assert_equal(self.mypom.current_round, 0)
        
    def test_advance_round(self):
        self.mypom.advance_round()
        nt.assert_equal(self.mypom.current_round, 1)
        self.mypom.advance_round()
        nt.assert_equal(self.mypom.current_round, 2)
        self.mypom.advance_round()
        self.mypom.advance_round()
        nt.assert_equal(self.mypom.current_round, 0)
        
    def test_active_countdown(self):
        nt.assert_true(self.mypom.active_countdown, self.mypom.work_countdown)
        self.mypom.advance_round()
        nt.assert_true(self.mypom.active_countdown, self.mypom.break_countdown)
        
    def test_start_pomodoro(self):
        self.mypom.start_pomodoro()
        nt.assert_true(self.mypom.work_countdown.timer.running)
        with nt.assert_raises(RuntimeError):
            self.mypom.start_pomodoro()
        
    def test_stop_pomodoro(self):
        with nt.assert_raises(RuntimeError):
            self.mypom.stop_pomodoro()
            
    def test_input_times(self):
        self.mypom.input_times((0,0,25,0), (0,0, 5,0))
        nt.assert_equal(self.mypom.work_countdown.countdowntime, 25)
        with nt.assert_raises(TypeError):
            self.mypom.input_times(25, 5)
        
    def test_time_remaining(self):
        nt.assert_equal(self.mypom.time_remaining(), 0)
        self.mypom.input_times((0,0,25,0), (0,0,5,0))
        nt.assert_equal(self.mypom.time_remaining(), 25)
        
        testpom = pom.Pomodoro()
        testpom.work_countdown.timer._now = uf.fake_time
        testpom.work_countdown.countdowntime = (0,0,25,0)
        testpom.start_pomodoro()
        testpom.stop_pomodoro()
        nt.assert_equal(testpom.work_countdown.timer.elapsed(), 1)
        nt.assert_equal(testpom.time_remaining(), 24)
        testpom.start_pomodoro()
        testpom.stop_pomodoro()
        nt.assert_equal(testpom.time_remaining(), 23)
        
        
    def test_reset_pomodoro(self):
        self.mypom.reset_pomodoro()
        nt.assert_equal(self.mypom.current_round, 0)
        nt.assert_equal(self.mypom.active_countdown, self.mypom.work_countdown)
    
   
    
