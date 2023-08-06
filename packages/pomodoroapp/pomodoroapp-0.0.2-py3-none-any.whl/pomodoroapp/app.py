import Tkinter as tk
import stopwatch as sw
import utilityfunctions as uf


class App(object):
    def __init__(self):
        
        self.my_timer = sw.Stopwatch(sw.real_time)
        self.root = tk.Tk()
        self.root.title("Stopwatch")
        
        self.on_state = False
        
        self.textvar = tk.StringVar()
        self.output = "00:00:00"
        self.textvar.set(self.output)
        self.label = tk.Label(textvariable=self.textvar, font=("Arial",16)).grid(row=0, column=0)
        
        self.small_text = tk.StringVar()
        self.small_output = "000"
        self.small_text.set(self.small_output)
        self.small_label = tk.Label(textvariable=self.small_text, width=5, font=("Arial",8)).grid(row=0, column=0, sticky="e")
      
        self.frame = frame = tk.Frame(self.root)
        frame.grid()
        
        self.start_button = tk.Button(frame, text="START", fg="green", command=self.start).grid(row=1, column=0)
        self.stop_button = tk.Button(frame, text="STOP", fg="red", command=self.stop).grid(row=1, column=1)
        self.reset_button = tk.Button(frame, text="RESET", fg="orange", command=self.reset).grid(row=1, column=2)
        
        self.time_elapsed = 0

    def print_elapsed(self):
        if self.on_state == True:
    
            self.time_elapsed = uf.tuple_to_clockface(uf.seconds_to_tuple(self.my_timer.elapsed()))
            self.output = self.time_elapsed[0]
            self.small_output = self.time_elapsed[1]
            self.textvar.set(self.output)
            self.small_text.set(self.small_output)
            
            self.root.after(50, self.print_elapsed)
            
        else:
            
            self.textvar.set(self.output)
            self.small_text.set(self.small_output)
        
    def start(self):
        self.my_timer.start_timer()
        self.on_state = True
        self.print_elapsed()
        
        
    def stop(self):
        self.my_timer.stop_timer()
        self.on_state = False
        self.print_elapsed()
        
        
    def reset(self):
        self.my_timer.reset()
        self.on_state = False
        self.output = "00:00:00"
        self.small_output = "000"
        self.print_elapsed()
        
   
def main():
    """Run main."""
    
    a = App()
    a.root.mainloop()

    return 0

if __name__ == '__main__':
    main()
    
