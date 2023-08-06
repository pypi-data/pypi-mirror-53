#pomodoro gui

import countdown as cd
import stopwatch as sw
import pomodoro as pom
import time
import tkinter as tk
from functools import partial
import utilityfunctions as uf
from pygame import mixer
from sys import exit


#I don't want the countdowns to be able to run at the same time

class Pomapp(object):
    
    def __init__(self, master):
		# list all attributes before building the widget
        self.master = master
        self.pomodoro = pom.Pomodoro()
        
        
        
        #making separate frames for the countdowns
        self.break_frame = tk.Frame(self.master).grid(row=0, column = 1)
        
        self.work_frame = tk.Frame(self.master).grid(row=0, column = 5)
        
        #giving the gui a title
        self.master.title("Pomodoro")
        
        #making buttons to select the countdown you want to set/use
        self.break_button = tk.Button(self.break_frame, text="Break Time", width = 10, command = lambda: self.select_countdown(self.break_button, self.work_button))
        self.break_button.grid(row=0, column=0)
        
        self.work_button = tk.Button(self.work_frame, text="Work Time", width = 10, command = lambda: self.select_countdown(self.work_button, self.break_button))
        self.work_button.grid(row=0, column=5)
        
        #Making the labels for the break countdown, the labels are where the numbers will be printed
        self.break_label_text = tk.StringVar()
        break_text = uf.seconds_to_string(self.pomodoro.break_countdown.countdowntime)
        self.break_label_text.set(break_text[0])
        
        #the small text is where the milliseconds are printed
        self.small_break_label_text = tk.StringVar()
        self.small_break_label_text.set(break_text[1])
        
        
        self.break_label = tk.Label(self.break_frame, textvariable=self.break_label_text, width = 10, font=("Arial",16))
        self.break_label.grid(row=1, column=0)
        
        self.small_break_label = tk.Label(self.break_frame, textvariable=self.small_break_label_text, width=5)
        self.small_break_label.grid(row=1, column=1, sticky="w")
        
        #Making the labels for the work countdown
        self.work_label_text = tk.StringVar()
        work_text = uf.seconds_to_string(self.pomodoro.work_countdown.countdowntime)
        self.work_label_text.set(work_text[0])
        
        self.small_work_label_text = tk.StringVar()
        self.small_work_label_text.set(work_text[1])
        
        self.work_label = tk.Label(self.work_frame, textvariable=self.work_label_text, width=10, font=("Arial",16))
        self.work_label.grid(row=1, column=5)
        
        self.small_work_label = tk.Label(self.work_frame, textvariable=self.small_work_label_text, width=5)
        self.small_work_label.grid(row=1, column=6, sticky="w")
        
        #define a dictionary containing labels to associate with their countdowns
        self.countdown_label = {self.pomodoro.work_countdown : (self.work_label_text, self.small_work_label_text),
                               self.pomodoro.break_countdown : (self.break_label_text, self.small_break_label_text)
                               }
                               
        #define a dictionary containing the countdowns associated with their buttons
        self.button_countdown = {self.work_button : self.pomodoro.work_countdown,
                                  self.break_button : self.pomodoro.break_countdown}
                                  
        
        self.countdown_button = {self.pomodoro.work_countdown : self.work_button,
                                 self.pomodoro.break_countdown : self.break_button}
        
        #the start/reset/quit buttons get a separate frame
        self.button_frame = tk.Frame(self.master).grid(row=3, column=2, columnspan=3)
        
        self.start_button = tk.Button(self.button_frame, text="START", fg="green", width=5, command=self.start)
        self.start_button.grid(row=2, column=2)
        self.reset_button = tk.Button(self.button_frame, text="RESET", fg="orange", width=5, command=self.reset)
        self.reset_button.grid(row=2, column=3)
        self.stop_button = tk.Button(self.button_frame, text="STOP", fg="red", width=5, command=self.manual_stop)
        self.stop_button.grid(row=2, column=4)
        
        #separate frame for the keypad
        self.keypad_frame = tk.Frame(self.master).grid(row=2)
        
        #list of labels for the keypad buttons
        self.keypad_button_list = ['1','2','3',
                                   '4','5','6',
                                   '7','8','9',
                                   '0']
        
        row=4
        column=2
        n=0
        #makes the list [0,1,2,3,4,5,6,7,8,9]
        #list() is there for python3 support. in python 2.7 it is redundant
        #in python3 range returns a range object
        number_button = list(range(len(self.keypad_button_list)))
        
        for label in self.keypad_button_list:
            #this will be where you assign the command for each button
            button_command = partial(self.callback, label)
            number_button[n] = tk.Button(self.keypad_frame, text=label, width=5, command=button_command)
            number_button[n].grid(row=row, column=column)
            n += 1
            column += 1
            if column > 4:
                column = 2
                row += 1
            if n == 9:
                column = 3
             
        #the actual_output is just the active time's countdown time 
        #dictionary containing the countdowns with their associated display outputs
        self.actual_output = {self.pomodoro.work_countdown: ['0','0','0','0','0','0'],
                              self.pomodoro.break_countdown: ['0','0','0','0','0','0']}
                              
        #this dictionary will ensure that each countdown has it's own callback counter
        self.callback_counter = {self.pomodoro.work_countdown: 0,
                                  self.pomodoro.break_countdown: 0}
        
        #ensure each countdown has it's own reset counter
        self.reset_counter = {self.pomodoro.work_countdown: 0,
                              self.pomodoro.break_countdown: 0}
                              
        #have a stop_state so that you can know when the stop button should stop or clear
        #this is for the manual_stop method
        self.stop_state = False
        
        #rounds counter, to count how many rounds of work-break countdowns you have done
        self.rounds_counter = 0
        
        #have a rounds counter between the work and break countdown
        #set its string variable
        self.rounds_label_text = tk.StringVar()
        self.rounds_label_text.set(str(self.rounds_counter) + " rounds")
        
        #make a frame for it
        self.rounds_frame = tk.Frame(self.master).grid(row=0, column=3)
        #then a label
        self.rounds_label = tk.Label(self.rounds_frame, textvariable = self.rounds_label_text, width = 10)
        self.rounds_label.grid(row=0, column =3)
        
    
                
    def select_countdown(self, selected_button, unselected_button):
        """selects the countdown to start with, either break or work 
        countdown"""
        
        if selected_button.cget("relief") == "raised":
            selected_button.config(relief="sunken")
            unselected_button.config(relief="raised")
        else:
            selected_button.config(relief="raised")
            unselected_button.config(relief="sunken")
        
        #make the selected countdown the active countdown
        self.pomodoro.active_countdown = self.button_countdown[selected_button]
        
                
    def play_alert(self):
        """plays the time's up alert sound"""
        
        #mixer.init()
        
        #time_up = mixer.Sound("backupdings.wav")
        #time_up.play()
        notification_root = tk.Tk()
        #notification_root.after(5000, lambda: notification_root.destroy())
        message = tk.Message(notification_root, text="Time's up!")
        message.config(bg="salmon", font=('helvetica', 24), padx=50, pady=50, width=500)
        message.pack()
        uf.flash_color((notification_root, message))
       
        
    def callback(self, label):
        """defines what happens when you press on one of the keys on the
        keypad"""
        
        if self.pomodoro.active_countdown is None:
            raise RuntimeError("A countdown has not been selected")
        
        if self.pomodoro.active_countdown.timer.running:
            raise RuntimeError("Timer is currently running")
            
        if self.stop_state:
            raise RuntimeError("Timer needs to be reset")
                
        if self.callback_counter[self.pomodoro.active_countdown] == 6:
            #print("the program is about to make self.actual output equal to 0")
            self.actual_output[self.pomodoro.active_countdown] = ['0','0','0','0','0','0']
            self.callback_counter[self.pomodoro.active_countdown] = 0
            
        # take off first element in large_output, and add label (keypad number pressed) to the end
        self.actual_output[self.pomodoro.active_countdown].pop(0)
        self.actual_output[self.pomodoro.active_countdown].append(label)
        self.callback_counter[self.pomodoro.active_countdown] += 1
            
        #display on gui
        self.countdown_label[self.pomodoro.active_countdown][0].set(uf.list_to_clockface(self.actual_output[self.pomodoro.active_countdown]))
        
            
            
        
    def print_to_countdown(self):
        """prints how much time is left in the countdown"""
        
        if self.pomodoro.active_countdown.timer.running:
            output = uf.sec_to_clockface(self.pomodoro.time_remaining())
            self.countdown_label[self.pomodoro.active_countdown][0].set(output[0])
            self.countdown_label[self.pomodoro.active_countdown][1].set(output[1])
            
            #when the time is up
            if self.pomodoro.active_countdown.time_remaining() < 0:
                self.play_alert()
                self.manual_stop()
                
                #count a round every time a work_countdown ends, you are
                #counting the number of times someone has done the work portion
                if self.pomodoro.is_work:
                    self.rounds_counter += 1
                    if self.rounds_counter == 1:
                        self.rounds_label_text.set(str(self.rounds_counter) + " round")
                    else:
                        self.rounds_label_text.set(str(self.rounds_counter) + " rounds")
                    
                
                #the following two lines are done so that you don't end up with negative
                #numbers on the number display on the gui
            
                self.countdown_label[self.pomodoro.active_countdown][0].set(uf.sec_to_clockface(self.pomodoro.active_countdown.countdowntime)[0])
                self.countdown_label[self.pomodoro.active_countdown][1].set("000")
                
                self.toggle_countdown()
                
            
            self.master.after(50, self.print_to_countdown)
            
            
    def toggle_countdown(self):
        """this will toggle the countdown, and start it."""
        
        self.countdown_button[self.pomodoro.active_countdown].config(relief="raised") 
        
        self.pomodoro.toggle_countdown()
        
        #the next line ensures that the time_remaining is not less than zero, if it's less than zero the countdown won't start
        self.pomodoro.reset_pomodoro()
        
        #have buttons alternate between being raised and sunken 
        self.countdown_button[self.pomodoro.active_countdown].config(relief="sunken") 
       
            
        self.start()
        
        
    def start(self):
        """starts the countdown (the countdown that is selected)"""
        
        self.stop_state = False
        self.stop_button.config(text = "STOP")
        
        #Set the active countdown's time to the input the user gave with the keypad
        self.pomodoro.active_countdown.countdowntime = uf.list_to_tuple(self.actual_output[self.pomodoro.active_countdown])
        self.actual_output[self.pomodoro.active_countdown] = uf.sec_to_list(self.pomodoro.active_countdown.countdowntime)
        
        self.reset_counter[self.pomodoro.active_countdown] = 0
    
       
        #won't run if there isn't a countdown time
        if self.pomodoro.active_countdown.time_remaining() <= 0:
            raise RuntimeError('Time remaining is zero, input a countdown time')
        
        
        if self.pomodoro.active_countdown.timer.running:
            self.manual_stop()
            self.print_to_countdown()
            self.start_button.config(text = "START")
            
            
        else:  
            self.pomodoro.active_countdown.start_countdown()
            self.print_to_countdown()
            self.start_button.config(text = "PAUSE")  
            
            
    def manual_stop(self):
        """stops both countdown manually when the stop button is pressed"""
            
        if self.pomodoro.active_countdown == None:
            raise RuntimeError("Have not selected a countdown")
        
        if not self.stop_state:
            self.stop_state = True
            #stop the countdown
            self.pomodoro.active_countdown.stop_countdown()
        
            #change button text back to "START" from "PAUSE"
            self.start_button.config(text = "START")
        
            #change stop button text from "STOP" to "CLEAR"
            self.stop_button.config(text = "CLEAR")
            
            
        else:
            self.clear()
        
    def clear(self):
        """resets both countdowns after they are stopped."""
        
        #change stop button text from "CLEAR" to "STOP"
        self.stop_button.config(text = "STOP")
        self.stop_state = False
        
        #reset both countdowns
        self.pomodoro.reset_pomodoro()
        
        #set the countdown times equal to 0, because reset_pomodoro() does not do that
        self.pomodoro.input_times((0,0,0,0), (0,0,0,0))
        
        #change the display back to 0's
        self.countdown_label[self.pomodoro.break_countdown][0].set(uf.sec_to_clockface(self.pomodoro.break_countdown.countdowntime)[0])
        self.countdown_label[self.pomodoro.break_countdown][1].set("000")
        self.countdown_label[self.pomodoro.work_countdown][0].set(uf.sec_to_clockface(self.pomodoro.work_countdown.countdowntime)[0])
        self.countdown_label[self.pomodoro.work_countdown][1].set("000")
        
        #change the self.actual_outputs back to 0
        self.actual_output[self.pomodoro.break_countdown] = uf.sec_to_list(self.pomodoro.break_countdown.countdowntime)
        self.actual_output[self.pomodoro.work_countdown] = uf.sec_to_list(self.pomodoro.work_countdown.countdowntime)
        
        #make sure both break and work time buttons are raised
        self.work_button.config(relief="raised")
        self.break_button.config(relief="raised")
        
        #make neither countdown be the active countdown
        self.pomodoro.active_countdown = None
        
        #have to reset callback counter
        self.callback_counter[self.pomodoro.work_countdown] = 0
        self.callback_counter[self.pomodoro.break_countdown] = 0
        
        #reset the rounds counter
        self.rounds_counter = 0
        
        #reset the rounds counter on the gui
        self.rounds_label_text.set(str(self.rounds_counter) + " rounds")

        
    def reset(self):
        """resets the selected countdown"""
        #print(self.countdown_label[self.pomodoro.active_countdown][0].get())
        #print(uf.sec_to_clockface(self.pomodoro.active_countdown.countdowntime)[0])
        
        #if what's currently displayed on the gui is equal to the countdown time
        #then you reset to zero, so we increment the reset counter by 1
        if self.countdown_label[self.pomodoro.active_countdown][0].get() == uf.sec_to_clockface(self.pomodoro.active_countdown.countdowntime)[0]:
            #print "it worked, increment reset counter"
            self.reset_counter[self.pomodoro.active_countdown] = 1
            
        #if reset has been clicked twice, everything gets fully reset to 0
        if self.reset_counter[self.pomodoro.active_countdown] >= 1:
            self.reset_counter[self.pomodoro.active_countdown] = 0
            self.pomodoro.active_countdown.countdowntime = (0,0,0,0)
        
        #when reset is clicked, timer is no longer in stop mode
        self.stop_state = False
        
        #reset the callback counter
        self.callback_counter[self.pomodoro.active_countdown] = 0
        
        #so that the time_remaining is not < 0
        self.pomodoro.reset_pomodoro()
        
        self.reset_counter[self.pomodoro.active_countdown] += 1
        
        #have the gui display the countdown's countdowntime obtained from the countdown object
        #if reset was hit once, it will be the original countdowntime, if twice, it will be zero
        self.countdown_label[self.pomodoro.active_countdown][0].set(uf.sec_to_clockface(self.pomodoro.active_countdown.countdowntime)[0])
        self.countdown_label[self.pomodoro.active_countdown][1].set("000")
        
        #the gui will display whatever the countdown time has been reset to
        self.actual_output[self.pomodoro.active_countdown] = uf.sec_to_list(self.pomodoro.active_countdown.countdowntime)
        
        #print str(self.reset_counter[self.pomodoro.active_countdown]) + " this is the reset counter at the end of reset method"


def main():
    """run main."""
    #creating the root window of our application with the Tk class
    root = tk.Tk()
    a = Pomapp(root)
    root.mainloop()
        
if __name__ == '__main__':
    main()
        
