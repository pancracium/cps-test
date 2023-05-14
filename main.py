"""
Simple CPS test application made in python using the tkinter library.
I used the ttk module from the tkinter library because the buttons look way cleaner.
I also impremented some simple error handling, so overall, there should not be any errors, 
expect for the ZeroDivision an error on line 104 if the duration is 0 (infinite). (Doesn't crash the program though).
Works by counting how many clicks the user did on the click button, and divide it by the duration.
Note that the duration should be in seconds, and if the duration is zero, the test will be infinite (this is on purpose).
To end and infinite test, simply click the "End test" button on the bottom center of the window.
It also has labels to show the user the current click count and the elapsed time.
Also note than sometimes, the time label may show a slightly incorrect number when the test finished (i. e.: 5 seconds may be shown as 4.99).
I am also thinking of adding the posibility of inserting a float as duration, instead of only integers.

Intructions:
    1. Insert the desired duration in seconds into the input.
    2. Click the "Start test" button.
    3. Click the "Click!" button as fast as you can.
    4. Once the test has finished, the user will be shown the result of the CPS test.
    5. If you want to run a new test, simply click the "New test" button and repeat steps 1 - 5.

Made by pancracium @ github (https://github.com/pancracium).
"""

import time
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk

class CPS_Test:
    def __init__(self):
        #Create a window with custom title, size and icon
        self.master = tk.Tk()
        self.master.title("CPS Test")
        self.master.geometry("1080x720+420+180")
        self.master.iconbitmap("icon.ico")

        #Define some fonts
        self.click_font = ("Roboto", 20, "bold")
        self.font = ("Roboto", 11, "bold")

        #Declare some necessary variables
        self.clicks = 0
        self.start_time = None
        self.end_time = None
        self.update_delay = 10

        #Call the create_widgets() and update() methods
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        """Create the widgets."""
        #Label to show the user how many CPS he got
        self.label_instructions = tk.Label(text="Enter test duration in seconds:", font=self.font)
        self.label_instructions.place(relx=0.5, rely=0.025, anchor=tk.CENTER)
        
        #Entry for the duration in seconds of the test
        self.entry_duration = ttk.Entry(font=self.font)
        self.entry_duration.place(relx=0.5, rely=0.055, anchor=tk.CENTER)
        
        #Button to start the test
        self.button_start = ttk.Button(text="Start Test", command=self.start_test)
        self.button_start.place(relx=0.54, rely=0.1, anchor=tk.CENTER)
        
        #Label to show the user the click count
        self.label_clicks = tk.Label(text="Clicks: 0", font=self.font)
        self.label_clicks.place(relx=0.25, rely=0.05, anchor=tk.CENTER)
        
        #Label to show the user the current timer
        self.label_timer = tk.Label(text="Time: 0.00", font=self.font)
        self.label_timer.place(relx=0.75, rely=0.05, anchor=tk.CENTER)
        
        #Button for the user to click and count the current clicks
        self.button_click = tk.Button(text="Click!", command=self.click, state=tk.DISABLED, width=50, 
                                      height=15, relief="flat", borderwidth=0, highlightthickness=0, 
                                      bg="grey70", font=self.click_font)
        self.button_click.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        #Button to start a new test
        self.button_new_test = ttk.Button(text="New Test", command=self.new_test, state=tk.DISABLED)
        self.button_new_test.place(relx=0.46, rely=0.1, anchor=tk.CENTER)

        #Button to end the current test:
        self.button_end = ttk.Button(text="End test", command=self.end_test, state=tk.DISABLED)
        self.button_end.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        #Entry for the update delay
        self.entry_delay = ttk.Entry(font=self.font, width=15)
        self.entry_delay.place(relx=0.1, rely=0.95, anchor=tk.CENTER)
        self.entry_delay.insert(0, "10")

        #Button to update the update delay
        self.button_delay = ttk.Button(text="Change update delay", command=self.change_update_delay)
        self.button_delay.place(relx=0.1, rely=0.91, anchor=tk.CENTER)
        
    def start_test(self):
        """Start the test."""
        #Get the duration the user submitted
        duration = self.entry_duration.get()

        #Check if it's a digit
        if duration.isdigit():
            #Check if it's zero. If so, the test will be infinite
            if duration == "0":
                msgbox.showinfo(title="Infinite clicking test", message="Note that if you insert zero as duration, the test will be infinite, giving no CPS results.")
            #Start the test
            self.duration = int(duration)
            self.label_instructions.config(text="Click as fast as you can!")
            self.entry_duration.config(state=tk.DISABLED)
            self.button_start.config(state=tk.DISABLED)
            self.button_click.config(state=tk.NORMAL)
            self.button_end.config(state=tk.NORMAL)
        else:
            #Else, show the user an error message
            msgbox.showerror(title="Error", message="Please insert a valid integer.")
            self.entry_duration.delete(0, tk.END)
        
    def click(self):
        """Detect the click and add it to the click count."""
        #Set a start time if it hasn't been set yet
        if not self.start_time:
            self.start_time = time.time()
        else:
            #Add a click to the click count and update the label
            self.clicks += 1
            self.label_clicks.config(text="Clicks: {}".format(self.clicks))
        
    def update(self):
        """Update the program."""
        #If the duration time has elapsed, end the test and show the user how many CPS he got
        if self.start_time and not self.end_time and time.time() - self.start_time >= self.duration:
            self.end_time = time.time()
            #Calculate the CPS
            cps = self.clicks / self.duration
            #Show the CPS to the user
            self.label_instructions.config(text="Your CPS is: {:.2f}".format(cps))
            self.button_click.config(text="{:.2f} CPS".format(cps))
            #Disable the Click button and enable the new test button again
            self.button_click.config(state=tk.DISABLED)
            self.button_new_test.config(state=tk.NORMAL)
        else:
            #Calculate elapsed time and update the timer label
            if self.start_time and not self.end_time:
                elapsed_time = time.time() - self.start_time
                self.label_timer.config(text="Time: {:.2f}".format(elapsed_time))

        #Keep updating every 10 milliseconds
        self.master.after(self.update_delay, self.update)

    def new_test(self):
        """Start a new CPS test."""
        #Reset all widgets to their default state
        self.entry_duration.delete(0, tk.END)
        self.entry_duration.config(state=tk.NORMAL)
        self.button_start.config(state=tk.NORMAL)
        self.button_click.config(state=tk.DISABLED)
        self.button_click.config(text="Click!")
        self.button_new_test.config(state=tk.DISABLED)
        self.button_end.config(state=tk.DISABLED)
        self.label_instructions.config(text="Enter test duration in seconds:")
        self.label_clicks.config(text="Clicks: 0")
        self.label_timer.config(text="Time: 0.00")
        
        #Reset all variables
        self.clicks = 0
        self.start_time = None
        self.end_time = None
    
    def end_test(self):
        """Abort the test."""
        #Stop the test
        self.end_time = time.time()
        self.label_instructions.config(text="Test aborted.")

        #Enable the new test button
        self.button_new_test.config(state=tk.NORMAL)

        #Disable the click and end test buttons
        self.button_click.config(state=tk.DISABLED)
        self.button_end.config(state=tk.DISABLED)

        #Reset the duration entry and the click and time labels
        self.entry_duration.config(state=tk.NORMAL)
        self.entry_duration.delete(0, tk.END)
        self.entry_duration.config(state=tk.DISABLED)
        self.label_clicks.config(text="Clicks: 0")
        self.label_timer.config(text="Time: 0.00")
    
    def change_update_delay(self):
        try:
            self.update_delay = int(self.entry_delay.get())
        except ValueError:
            msgbox.showerror(title="Error", message="Please insert a valid poisitve integer (in milliseconds).")
            self.entry_delay.delete(0, tk.END)
        else:
            msgbox.showinfo(title="Success!", message=f"Successfully chnaged the update delay to {self.update_delay} milliseconds.")
        
    def run(self):
        """Run the program"""
        self.master.mainloop()

#Run the program by calling the run() method
CPS_Test().run()