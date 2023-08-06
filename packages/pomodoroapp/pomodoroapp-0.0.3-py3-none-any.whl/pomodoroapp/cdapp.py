import countdown as cd
import stopwatch as sw
import time
import tkinter as tk
from functools import partial
import utilityfunctions as uf
import pygame as pg



        
class Cdapp(object):
    #Cdapp class works with tuples for the time
    def __init__(self):
        self.mycountdown = cd.Countdown(sw.real_time)
        self.mytimer = sw.Stopwatch(sw.real_time)
        #convert countdown_time (which is in seconds (this happens automatically when initializing a countdown)) to a tuple
        self.countdown_time = uf.seconds_to_tuple(self.mycountdown.countdowntime)
        self.root = tk.Tk()
        self.root.title("Countdown")
        #self.root.configure(bg="red")
        
        
        self.textvar = tk.StringVar()
        self.output = "{:02d}:{:02d}:{:02d}".format(self.countdown_time[0], self.countdown_time[1], self.countdown_time[2])
        self.textvar.set(self.output)
        self.label = tk.Label(textvariable=self.textvar, font=("Arial",16))
        self.label.grid(row=0, column=0)
        
        self.small_text = tk.StringVar()
        self.small_output = "000"
        self.small_text.set(self.small_output)
        self.small_label = tk.Label(textvariable=self.small_text,width=5, font=("Arial",8))
        self.small_label.grid(row=0, column=0, sticky="e")
        #self.small_label.configure(bg="red")
      
        self.frame = frame = tk.Frame(self.root)
        frame.grid()
        
        self.start_button = tk.Button(frame, text="START", fg="green", width=5, command=self.start)
        self.start_button.grid(row=1, column=0)
        self.reset_button = tk.Button(frame, text="RESET", fg="orange", width=5, command=self.reset)
        self.reset_button.grid(row=1, column=1)
        self.quit_button = tk.Button(frame, text="QUIT", width=5, command = self.root.quit)
        self.quit_button.grid(row=1, column=2)
        
        self.time_left = 0
        
        #lf = tk.LabelFrame(self.root, text="Keypad", bd=3, 
        #                   relief=tk.RIDGE).grid(columnspan=3)
        self.button_list = [
        '1','2','3',
        '4','5','6',
        '7','8','9',
        '0']
        row = 2
        column = 0
        n = 0
        number_button = list(range(len(self.button_list)))
        for label in self.button_list:
            button_command = partial(self.callback, label)
            number_button[n] = tk.Button(self.frame, text=label, width=5, command=button_command)
            number_button[n].grid(row=row, column=column)
            n += 1
            column += 1
            if column > 2:
                column = 0
                row +=1
            if n == 9:
                column = 1
                
        self.click_counter = 0
        self.reset_counter = 0
        
        self.on_state = False
        self.new_output = (00,00,00)
        
        #toggle flag
        self.keep_toggling = False
        
    def play_alert(self):
        """Plays the time's up alert sound"""
        
        pg.mixer.init()
        time_up = pg.mixer.Sound("backupdings.wav")
        
        time_up.play()
        
    def toggle_red(self, root, widget):
        """Makes the background of the labels and root flash red."""
        if not self.keep_toggling:
            uf.return_bg_color(widget)
            return
        else:
         
            for w in widget:
        
                if w.cget("bg") == '#d9d9d9':
                    w.configure(bg="red")
                else:
                    w.configure(bg="#d9d9d9")
        
            root.after(1000, self.toggle_red, root, widget)
                
    def callback(self, label):
        #If timer is running, don't do anything
        if self.mycountdown.timer.running:
            print("timer is currently running")
            return
            
        #print "Click {}".format(self.click_counter)
        
        #this ensures that when reset is clicked after a number is clicked, the original countdown
        # time reappears
        self.reset_counter = 0
        
        # "hh:mm:ss" (what has been inputted by user using keypad) -> [h,h,m,m,s,s] 
        self.new_output = uf.string_to_list(self.output)
        # take off first element in new_output, and add label (keypad number pressed) to the end
        self.new_output.pop(0)
        self.new_output.append(label)
        
        #count up 1, to keep track of how many spaces in hh:mm:ss have been filled
        self.click_counter += 1
        
        #resets after the first h in hh:mm:ss has been filled (or rightmost number has moved all the way to leftmost spot)
        if self.click_counter > 6:
            self.output = self.new_output
            self.reset()
            return
        
        #[h,h,m,m,s,s] -> (hh,mm,ss, ms (always zero)) 
        self.new_output = uf.list_to_tuple(self.new_output)
        
        
        self.output = "{:02d}:{:02d}:{:02d}".format(self.new_output[0], self.new_output[1], self.new_output[2])
        self.textvar.set(self.output)
    
        return self.output
             
        

    def print_elapsed(self):
        # if countdown is running
        if self.on_state:
    
            self.time_left = uf.tuple_to_clockface(uf.seconds_to_tuple(self.mycountdown.time_remaining()))
            
            #separating hh:mm:ss and ms
            self.output = self.time_left[0]
            self.small_output = self.time_left[1]
            
            self.textvar.set(self.output)
            self.small_text.set(self.small_output)
            
            #print "this is the time remaining {}" .format(self.mycountdown.time_remaining())
            
            if self.mycountdown.time_remaining() < 0:
                self.stop()
                
                
                
                #remove start button 
                if self.start_button.winfo_ismapped():
                    self.start_button.grid_forget()
                
                #change toggle flag
                self.keep_toggling = True
                self.toggle_red(self.root, [self.root, self.label, self.small_label])
                #sound toggle??
                ##
                #play sound
                self.play_alert()
                
                
                
            self.root.after(50, self.print_elapsed)
            
        #if it's not running just display the current keypad output    
        else:
            
            self.textvar.set(self.output)
            self.small_text.set(self.small_output)
        
        
        
    def start(self):
        #print("this is the new_output {}".format(self.new_output))
        #change the countdown_time in the countdown instance
        self.mycountdown.countdowntime = self.new_output
        
        #change the countdown_Time for the Cdapp instance
        self.countdown_time = uf.seconds_to_tuple(self.mycountdown.countdowntime)
        
        #setting reset counter back to zero in case start is clicked after reset has been clicked once
        #so that it goes back to the original countdown time (ensures that it resets to zero IFF reset has
        #been clicked two times consecutively)
        self.reset_counter = 0
        
        #print("this is the time remaining{}".format(self.mycountdown.time_remaining()))
        #won't run if there isn't a countdown time
        if self.mycountdown.time_remaining() <= 0:
            raise RuntimeError('Time remaining is zero, input a countdown time')
            
        if not self.on_state:
            self.on_state = True
            self.mycountdown.start_countdown()
            self.print_elapsed()
            self.start_button.config(text = "PAUSE")
            
        else:
            self.on_state = False
            self.mycountdown.stop_countdown()
            self.start_button.config(text = "START")
            
        #print("this is the current countdown time {}".format(self.countdown_time))
            
        
    def stop(self):
        self.mycountdown.stop_countdown()
        self.on_state = False
        
        # I don't know why I had the lines below
        # so that you don'e end up wit h-1:59 after the countdown has elapsed
        
        #self.print_elapsed()
        self.output = "00:00:00"
        self.small_output = "000"
        self.textvar.set(self.output)
        self.small_text.set(self.small_output)
        return
        
        
    def reset(self):
        #print("timer is being reset")
        self.keep_toggling = False
        #uf.return_bg_color([self.root, self.label, self.small_label])
        
        if self.reset_counter >= 1:
            self.reset_counter = 0
            self.mycountdown.countdowntime = (0,0,0,0)
            
        self.reset_counter += 1
        #print("this is how many times reset has been clicked {}".format(self.reset_counter))
        self.start_button.grid(row=1, column=0)

        self.mycountdown.reset_countdown()
        self.countdown_time = uf.seconds_to_tuple(self.mycountdown.countdowntime)
        self.on_state = False
        self.start_button.config(text = "START")
        self.click_counter = 0
        self.output = "{:02d}:{:02d}:{:02d}".format(self.countdown_time[0], self.countdown_time[1], self.countdown_time[2])
        self.small_output = "000"
        self.new_output = uf.string_to_list(self.output)
        self.new_output = uf.list_to_tuple(self.new_output)
        self.print_elapsed()
        #print("here is output after being reset {}".format(self.output))
        #print("this is the current countdown time {}".format(self.countdown_time))
        
   
def main():
    """Run main."""
    
    a = Cdapp()
    a.root.mainloop()

    return 0

if __name__ == '__main__':
    main()
