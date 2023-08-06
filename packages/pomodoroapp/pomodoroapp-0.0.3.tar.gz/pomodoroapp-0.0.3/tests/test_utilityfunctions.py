#utilityfunctions testing module
import nose.tools as nt
import stopwatch.stopwatch as sw
import unittest
import stopwatch.utilityfunctions as uf
import Tkinter as tk
import stopwatch.cdapp as ca

class TestUtilityfunctions(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_seconds_to_tuple(self):
        time_diff = 5410.001 #seconds
        time_diff = uf.seconds_to_tuple(time_diff)
        
        nt.assert_equal(time_diff, (1.0, 30.0, 10.0, 1))
        
        
    def test_tuple_to_seconds(self):
        time_diff = (1.0, 30.0, 10.0, 1)
        time_diff = uf.tuple_to_seconds(time_diff)
        
        nt.assert_equal(time_diff, 5410)
        nt.assert_raises(TypeError, uf.tuple_to_seconds, 15)
        
    def test_tuple_to_clockface(self):
        time_min_sec = (0, 55, 45, 1)
        
        uf.tuple_to_clockface(time_min_sec)
        
        nt.assert_equal(uf.tuple_to_clockface(time_min_sec), ("00:55:45", "001"))
        
    def test_hide_me(self):
        pass
        #root = tk.Tk()
        #w = tk.Label(root, text="hello")
        #w.pack()
        #gnt.assert_equal(w.winfo_ismapped(), 1)
        #uf.hide_me(w)
        #nt.assert_false(w.winfo_ismapped())
        
        """ Can use the following:
        root = tk.Tk()
        w = Label(root, text="hello")
        w.pack()
        w.winfo_ismapped()
        w.pack_forget()
        w.winfo_ismapped() """
        
    def test_string_to_list(self):
        item = "13:52:10"
        item = uf.string_to_list(item)
        nt.assert_equal(item, ['1','3','5','2','1','0'])
        
    def test_list_to_tuple(self):
        item = ['1','3','5','2','1','0']
        item = uf.list_to_tuple(item)
        nt.assert_equal(item, (13, 52, 10, 00))
        
    def test_seconds_to_string(self):
        number_of_seconds = 10
        number_of_seconds = uf.seconds_to_string(number_of_seconds)
        nt.assert_equal(number_of_seconds, ("00:00:10", "000"))
        
