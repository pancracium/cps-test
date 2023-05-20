"""
Simple CPS test application made in Python using the tkinter library. It counts the number of clicks the user makes within a specified duration and calculates the CPS 
(Clicks Per Second) rate.

This application detects how many clicks the user did to the click button, and then divides that number by the time.
I made the program using mostly tkinter, but used other modules such as ttk (from the tkinter package) to create most of the widgets, because in my 
opinion the ttk widgets look better. I also used other packages such as time (to count the duration), pygame (to play the click.wav sound) and json (to save and load awards).


To use the application:

1. Enter the desired duration in seconds.
2. Click the "Start test" button.
3. Click the "Click!" button as fast as possible.
4. Once the test is finished, the result of the CPS test will be displayed.
5. To run a new test, click the "New test" button.

Repeat steps from 1 to 5 to run more tests


The application provides different awards based on the CPS achieved (the awards are saved when the program is closed and load again when the program is opened):

- Normal clicker: 5-6 CPS
- Fast clicker: 7-9 CPS
- Jitter clicker: 10-12 CPS
- Butterfly clicker: 13-16 CPS
- True butterfly clicker: 17-22 CPS
- Drag clicker: 23-30 CPS
- Bolt clicker: 31-40 CPS
- Autoclicker: 41+ CPS


Notes: 

- The application may display a slightly incorrect time when the test is finished (e.g., 5 seconds may be shown as 4.99).

- You can ignore zeros at the start of numbers, even on floats. For example: 01 -> 1; 0.1 -> .1

- The duration must be in seconds, not minutes, not milliseconds, but seconds. The value must be an integer or a float. Use a point (.) and not a comma (,) as floating point.

- If the duration is 0, the test will be infinite, giving no results. This is made on purpose. You will get ZeroDivisionError at line 104, but it won't crash the program.

- If the update delay value is zero or a negative number, the program will likely crash. This is not a bug, it's common sense.

- Even if you use the clicking method of an achivement, you may get different CPS than what the achievement shows. For example even if you drag click you may not get 23-30 CPS.

- If you set the duration to a number less than 1, you will get an incorrectly high amount of cps. This is because the click count is divided by the duration. For example, 
1 (Click count) / 0.1 (duration in seconds) is 10, and so on.


I don't think I have to describe what each widget does, it pretty self-explainative.

Created by pancracium @ GitHub (https://github.com/pancracium/cps-test).
"""

#Import the necessary modules and call pygame.init() to initilize pygame
import json, pygame, time
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from tkinter import ttk
pygame.init()

class CPS_Test:
    def __init__(self):
        #Create a window with custom title, size and icon
        self.master = tk.Tk()
        self.master.title("CPS Test")
        self.master.geometry("1080x720+420+180")
        self.master.iconbitmap("icon.ico")

        #Save the user's configuration to the config.json file when the window is closed
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.save_config(close=True))

        #Define some fonts
        self.click_font = ("Roboto", 20, "bold")
        self.font = ("Roboto", 11, "bold")

        #Info for the CPS test result
        self.click_count = 0
        self.start_time = None
        self.end_time = None
        self.update_delay = 10

        #Load the click sound
        self.click_sound = "click.wav"

        #Awards and highest score
        self.awards = []
        self.highest_score = 0

        #Call the create_widgets() and update() methods
        self.load_config()
        self.create_widgets()
        self.update()

    def create_widgets(self):
        """Create the widgets."""
        #Label to show the user how many CPS he got
        self.label_instructions = tk.Label(
            text="Enter test duration in seconds:", font=self.font)
        self.label_instructions.place(relx=0.5, rely=0.025, anchor=tk.CENTER)

        #Entry for the duration in seconds of the test and set 10 by default
        self.entry_duration = ttk.Entry(font=self.font)
        self.entry_duration.place(relx=0.5, rely=0.055, anchor=tk.CENTER)
        self.entry_duration.insert(0, "10")

        #Button to start the test
        self.button_start = ttk.Button(text="Start Test",
                                       command=self.start_test)
        self.button_start.place(relx=0.54, rely=0.1, anchor=tk.CENTER)

        #Label to show the user the click count
        self.label_clicks = tk.Label(text="Clicks: 0", font=self.font)
        self.label_clicks.place(relx=0.25, rely=0.05, anchor=tk.CENTER)

        #Label to show the user the current timer
        self.label_timer = tk.Label(text="Time: 0.00", font=self.font)
        self.label_timer.place(relx=0.75, rely=0.05, anchor=tk.CENTER)

        #Button for the user to click and count the current clicks
        self.button_click = tk.Button(text="Click!",
                                      command=self.click,
                                      state=tk.DISABLED,
                                      width=50,
                                      height=15,
                                      relief="flat",
                                      borderwidth=0,
                                      highlightthickness=0,
                                      bg="grey70",
                                      font=self.click_font)
        self.button_click.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #Button to start a new test
        self.button_new_test = ttk.Button(text="New Test",
                                          command=self.new_test,
                                          state=tk.DISABLED)
        self.button_new_test.place(relx=0.46, rely=0.1, anchor=tk.CENTER)

        #Button to end the current test:
        self.button_end = ttk.Button(text="End test",
                                     command=self.end_test,
                                     state=tk.DISABLED)
        self.button_end.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        #Entry for the update delay
        self.entry_delay = ttk.Entry(font=self.font, width=15)
        self.entry_delay.place(relx=0.1, rely=0.95, anchor=tk.CENTER)
        self.entry_delay.insert(0, str(self.update_delay))

        #Button to update the update delay
        self.button_delay = ttk.Button(text="Change update delay",
                                       command=self.change_update_delay)
        self.button_delay.place(relx=0.1, rely=0.91, anchor=tk.CENTER)

        #Button to show the user his awards
        self.button_awards = ttk.Button(text="Show awards",
                                        command=self.show_awards)
        self.button_awards.place(relx=0.9, rely=0.9, anchor=tk.CENTER)

        #Button to change the click sound to a custom one
        self.button_sound = ttk.Button(text="Upload custom click sound", command=self.change_click_sound)
        self.button_sound.place(relx=0.9, rely=0.95, anchor=tk.CENTER)

    def start_test(self):
        """Start the test."""
        #Get the duration the user submitted
        duration = self.entry_duration.get()

        try:
            #Add a keyword to reset all the awards easier
            if duration == "resetawards":
                self.awards = []
                self.highest_score = 0
                msgbox.showinfo(title="Success",
                                message="Successfully reset all awards.")

            else:
                #Convert the duration (string) into a float (number with decimal point)
                self.duration = float(duration)

                #Show the user an error message if the number is negative
                if self.duration < 0:
                    raise ValueError

                #Tell the user the test will be infinite if the duration is zero
                if self.duration == 0:
                    msgbox.showinfo(
                        title="Infinite clicking test",
                        message=
                        "Note that if you insert zero as duration, the test will be infinite, giving no CPS results."
                    )

                #Convert the duration to a number, tell the user the test has started and change some buttons' states and add a click to the click count
                self.label_instructions.config(text="Click as fast as you can!")
                self.entry_duration.config(state=tk.DISABLED)
                self.button_start.config(state=tk.DISABLED)
                self.button_click.config(state=tk.NORMAL)
                self.button_end.config(state=tk.NORMAL)
                self.click_count = 1

        except (ValueError, TypeError):
            #Show the user an error message if the inserted duration is not a valid
            msgbox.showerror(
                title="Error", 
                message="Please insert a positive number (it can also be a float) as duration, i. e.: 10, 5.2, 0.5, 100, 0, ...\n"
            )
            self.entry_duration.delete(0, tk.END)

    def click(self):
        """Detect the click and add it to the click count."""
        #Set a start time if it hasn't been set yet
        if not self.start_time:
            self.start_time = time.time()
        else:
            #Add a click to the click count and update the label
            self.click_count += 1
            self.label_clicks.config(
                text="Clicks: {}".format(self.click_count))
            pygame.mixer.Sound(self.click_sound).play()

    def update(self):
        """Update the program."""
        #If the duration time has elapsed, end the test and show the user how many CPS he got
        if self.start_time and not self.end_time and time.time() - self.start_time >= self.duration:
            self.end_time = time.time()

            #Calculate the CPS
            cps = self.click_count / self.duration

            #If the user got certain amount of CPS, give him an award and tell him so

            #Normal clicker award: 5-6 CPS
            if cps >= 5 and cps <= 6 and not "Normal clicker (get 5-6 CPS in a test)" in self.awards:
                self.awards.append("Normal clicker (get 5-6 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"Normal clicker (get 5-6 CPS in a test)\" award!"
                )

            #Fast clicker award: 7-9 CPS
            elif cps >= 7 and cps <= 9 and not "Fast clicker (get 7-9 CPS in a test)" in self.awards:
                self.awards.append("Fast clicker (get 7-9 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"Fast clicker (get 7-9 CPS in a test)\" award!"
                )

            #Jitter clicker award: 10-12 CPS
            elif cps >= 10 and cps <= 12 and not "Jitter clicker (get 10-12 CPS in a test)" in self.awards:
                self.awards.append("Jitter clicker (get 10-12 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"Jitter clicker (get 10-12 CPS in a test)\" award!"
                )

            #Butterfly clicker award: 13-16 CPS
            elif cps >= 13 and cps <= 16 and not "Butterfly clicker (get 13-16 CPS in a test)" in self.awards:
                self.awards.append(
                    "Butterfly clicker (get 13-16 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"Butterfly clicker (get 13-16 CPS in a test)\" award!"
                )

            #True butterfly clicker award: 17-22 CPS
            elif cps >= 17 and cps <= 22 and not "True butterfly clicker (get 17-22 CPS in a test)" in self.awards:
                self.awards.append(
                    "True butterfly clicker (get 17-22 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"True butterfly clicker (get 17-22 CPS in a test)\" award!"
                )

            #Drag clicker award: 23-30 CPS
            elif cps >= 23 and cps <= 30 and not "Drag clicker (get 23-30 CPS in a test)" in self.awards:
                self.awards.append("Drag clicker (get 23-30 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"Drag clicker (get 23-30 CPS in a test)\" award!"
                )

            #Bolt clicker award: 31-40 CPS
            elif cps >= 31 and cps <= 40 and not "Bolt clicker (get 31-40 CPS in a test)" in self.awards:
                self.awards.append("Bolt clicker (get 31-40 CPS in a test)")
                msgbox.showinfo(
                    title="Gained new award!",
                    message=
                    "You gained the \"Bolt clicker (get 31-40 CPS in a test)\" award!"
                )

            #Autoclicker award: 41+ CPS
            elif cps >= 41 and not "Autoclicker clicker (get 41+ CPS in a test)" in self.awards:
                self.awards.append(
                    "Autoclicker clicker (get 41+ CPS in a test)")
                msgbox.showinfo(
                    title="Congratulations, you cheater!",
                    message=
                    "You gained the \"Autoclicker clicker (get 41+ CPS in a test)\" award!"
                )
            
            #Check if the user has beaten his highest score
            if cps > self.highest_score:
                previous_highest_score = self.highest_score
                self.highest_score = cps
                msgbox.showinfo(
                    title="New highest score!",
                    message=f"You've beaten your previous CPS record of {previous_highest_score} CPS, with {self.highest_score} CPS!"
                )

            #Show the CPS to the user
            self.label_instructions.config(
                text="Your CPS is: {:.2f}".format(cps))
            self.button_click.config(text="{:.2f} CPS".format(cps))

            #Disable the Click button and the end button and enable the new test button again
            self.button_click.config(state=tk.DISABLED)
            self.button_end.config(state=tk.DISABLED)
            self.button_new_test.config(state=tk.NORMAL)
        else:
            #Calculate elapsed time and update the timer label
            if self.start_time and not self.end_time:
                elapsed_time = time.time() - self.start_time
                self.label_timer.config(
                    text="Time: {:.2f}".format(elapsed_time))

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
        self.click_count = 0
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
        """Change the update delay to the desired amount. Note: Don't use zero or a negative number,
        the program will crash. I repeat, it's not a bug, it's common sense."""
        #Try getting the update delay from the entry_delay entry
        try:
            self.update_delay = int(self.entry_delay.get())
        #If any error is raisen, tell the user the input is invalid
        except ValueError:
            msgbox.showerror(
                title="Error",
                message=
                "Please insert a valid poisitve integer (in milliseconds).")
            self.entry_delay.delete(0, tk.END)
        #Else, change the update delay to the desired amount
        else:
            msgbox.showinfo(
                title="Success!",
                message=
                f"Successfully chnaged the update delay to {self.update_delay} milliseconds."
            )

    def show_awards(self):
        """Show the user all the awards he has got."""
        #Create a new toplevel window
        awards_window = tk.Toplevel()
        awards_window.title("Current awards")
        awards_window.iconbitmap("awards.ico")
        awards_window.geometry("400x300+760+390")

        #Create a new string where all the gained awards will be shown
        if not self.awards:
            current_awards = "Not gained any award yet. Start a new test to gain new awards!"
        else:
            current_awards = "\n".join("- " + award for award in self.awards)
        
        #Create a label to show the user's highest score
        highest_score_label = tk.Label(awards_window, text=f"highest score: {self.highest_score} CPS")
        highest_score_label.pack()

        #Create a label to show the string with the awards
        awards_label = tk.Label(awards_window, text=current_awards)
        awards_label.pack()

        #Create a button to close the toplevel window
        ok_button = ttk.Button(awards_window, text="OK", command=awards_window.destroy)
        ok_button.pack()

    def save_config(self, close:bool):
        """Save the user's configuration to the config.json file."""
        #Create a dictionary for better organization
        data = {
            "awards": self.awards,
            "highest_score": self.highest_score,
            "click_sound": self.click_sound,
            "update_delay": self.update_delay
        }

        #Dump all the data to the config.json file
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

        #Close the program if the close parameter is true
        if close:
            self.master.destroy()

    def load_config(self):
        """Load the user's configuration from the config.json file."""
        try:
            #Try to get the data from the config.json
            with open("config.json", "r") as file:
                data = json.load(file)
                self.awards = data.get("awards", [])
                self.highest_score = data.get("highest_score", 0)
                self.click_sound = data.get("click_sound", "click.wav")
                self.update_delay = data.get("update_delay", 10)
        except FileNotFoundError:
            #If the files doesn't exist, set some default values
            self.awards = []
            self.highest_score = 0
            self.click_sound = "click.wav"
            self.update_delay = 10

    def change_click_sound(self):
        """Changes the click sound to a custom one by uploading a WAV or MP3 file."""
        #Prompt the user for a file
        file = filedialog.askopenfilename(
            title="Select custom click sound",
            initialdir="~/Music",
            filetypes=(("WAV files", "*.wav"), 
                       ("MP3 files", "*.mp3"), 
                       ("All files", "*.*")),
        )

        if file:
            #Get only the file name, not the complete directory
            file_name = [x for x in file.split("/")][-1]

            #Change the click sound to the new one if there aren't any errors
            try:
                self.click_sound = file
            except pygame.error as e:
                #Show the user an error message if there's an error
                msgbox.showerror(
                    title="Error", 
                    message=f"Error: {e}"
                )
            else:
                #Else, tell the user everything's fine
                msgbox.showinfo(
                    title="Success", 
                    message=f"Successfully changed the click sound to {file_name}"
                )
            
            self.save_config(close=False)

    def run(self):
        """Run the program"""
        self.master.mainloop()

#Run the program by calling the run() method
CPS_Test().run()