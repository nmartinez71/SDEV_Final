from breezypythongui import EasyFrame
import tkinter as tk

class Scheduler(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, "Newday")

class MainWindow(Scheduler): 
    def __init__(self):
        Scheduler.__init__(self)

        #GUI Elements
        self.addLabel(text="Welcome to Newday!", row=1, column=0)
        self.week_button = self.addButton("Start Scheduler", row=4, column=0, command=self.open_week_scheduler)
        self.week_label = self.addLabel(text="Select the Week to Schedule in:", row=2, column=0) 
        self.week_list = self.addListbox(row=3, column=0, width=100, height=5) #Creates the Listbox of Weeks
        for num in range(1, 53):
            self.week_list.insert(tk.END, f"Week {num}") #Populates the week & numbers into the listbox

    #Methods
    def open_week_scheduler(self):
        try:
            selected_week = self.week_list.get(self.week_list.curselection()) #Selects the Week and its number
            self.week_scheduler = WeekScheduler(self, selected_week) #Create an instance of WeekScheduler
            self.week_button["state"] = "disabled" #Disable the Week button
            self.week_list["state"] = "disabled" #Disable the Week Selection
        except tk.TclError:
            #If no week is selected, an error will appear
            noWeekSelected = "Please select a week to schedule in."
            self.error_message(noWeekSelected)
        
    def reenable_selections(self):
        self.week_button["state"] = "normal"  #Re-enable the Week button
        self.week_list["state"] = "normal"  #Re-enable the Week Selection

    def error_message(self, error_text):
         self.messageBox(message=error_text, title="Error") #Displays an error message

class WeekScheduler(Scheduler):
    def __init__(self, main_window, selected_week):
        Scheduler.__init__(self)
        self.main_window = main_window
        self.selected_week = selected_week
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
        #GUI Elements
        self.addLabel(text=f"{selected_week}", row=0, column=0)
        self.addLabel(text="Employee Name:", row=2, column=0)
        self.close_button = self.addButton(text="Close", row=0, column=7, command=self.close_schedule)
        self.save_button = self.addButton("Save", row=4, column=0, command=self.save)
        self.employee_name = self.addTextField("Name", row=3, column=0)
        self.schedule_display = self.addTextArea(text="",row=5, column=0, columnspan=7, width=40, height=10)
        self.text_fields = {}
        for index, day in enumerate(days):
            self.addLabel(text=day, row=2, column= index + 1)
            self.text_fields[day] = self.addTextField("Time", row=3, column = index + 1, width=15)
        self.schedule_display["state"] = "disabled"  #Make it read-only

    def add_to_textbox(self, text_item):
        #Text Box displays what Employee you have saved 
        self.schedule_display["state"] = "normal" #Enables editing for the saving
        self.schedule_display.appendText(f"{text_item}")
        self.schedule_display["state"] = "disabled"  #Re-enables read only state after appending
    
    def save(self):
        # Prepare data to save
        data_to_save = f"Employee Name: {self.employee_name.getText()}\n"
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            task = self.text_fields[day].getText()
            if not task:  #Check if the task field is empty
                self.main_window.error_message(f"Please enter a task for {day}.")
                return
            data_to_save += f"{day}\t\t{task}\n"  #Format tasks in a grid layout
        
        #Get employee name
        employee_name = self.employee_name.getText()
        if employee_name:  # Only save if there's a name
            #Write to a file and clear the input boxes
            file_name = f"schedule_{self.selected_week}.txt"
            with open(file_name, "a") as file:  # Use append mode
                file.write(data_to_save)

            # Shows feedback 
            self.add_to_textbox(data_to_save)  
            print("Schedule saved to", file_name)  # Text Box displays feedback that you have saved the schedule

            #Clears text
            self.employee_name.setText("")  #Clear employee name input
            for text in self.text_fields.values():  #Runs through all text fields
                text.setText("")  # Clear day fields
        else:
            self.main_window.error_message("Enter employee name")

    def close_schedule(self):
        self.main_window.week_scheduler.destroy()
        self.main_window.reenable_selections()

# Runners
def main():
    MainWindow().mainloop()

if __name__ == "__main__":
    main()
