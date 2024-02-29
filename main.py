import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PseudoRandom import PseudoRandom  # Replace 'your_module' with the actual name of the module where your PseudoRandom class is defined
import pandas as pd

class App:
    def __init__(self, master):
        self.master = master
        master.title("Random Number Generator")

        self.label = tk.Label(master, text="Select a function:")
        self.label.pack()

        self.function_var = tk.StringVar()
        self.function_var.set("Middle Square")  # Set the default function
        self.function_menu = tk.OptionMenu(master, self.function_var, "Middle Square", "Linear Congruential", "Quadratic Congruential")
        self.function_menu.pack()

        self.quantity_label = tk.Label(master, text="Enter quantity:")
        self.quantity_label.pack()

        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.pack()

        self.seed_label = tk.Label(master, text="Enter seed:")
        self.seed_label.pack()

        self.seed_entry = tk.Entry(master)
        self.seed_entry.pack()

        # Additional input fields for Linear Congruential and Quadratic Congruential
        self.a_label = tk.Label(master, text="Enter 'a':")
        self.a_entry = tk.Entry(master)

        self.b_label = tk.Label(master, text="Enter 'b':")
        self.b_entry = tk.Entry(master)

        self.c_label = tk.Label(master, text="Enter 'c':")
        self.c_entry = tk.Entry(master)

        self.m_label = tk.Label(master, text="Enter 'm':")
        self.m_entry = tk.Entry(master)

        self.show_additional_fields()

        self.generate_button = tk.Button(master, text="Generate", command=self.generate)
        self.generate_button.pack()

        # Create a Treeview widget once
        self.tree = ttk.Treeview(master)
        self.tree["show"] = "headings"  # Hide the default empty column

    def list_to_dataframe(self, data):
        df = pd.DataFrame(data)
        return df
    
    def generate(self):
        try:
            quantity = int(self.quantity_entry.get())
            seed = int(self.seed_entry.get())
            function_name = self.function_var.get()

            # Additional parameters for Linear Congruential and Quadratic Congruential
            a = int(self.a_entry.get()) if hasattr(self, 'a_entry') and self.a_entry.get() else None
            b = int(self.b_entry.get()) if hasattr(self, 'b_entry') and self.b_entry.get() else None
            c = int(self.c_entry.get()) if hasattr(self, 'c_entry') and self.c_entry.get() else None
            m = int(self.m_entry.get()) if hasattr(self, 'm_entry') and self.m_entry.get() else None

            # Validate input values
            if function_name in ["Linear Congruential", "Quadratic Congruential"]:
                if any(value is None for value in [a, b, c, m]):
                    messagebox.showerror("Error", "Please enter values for 'a', 'b', 'c', and 'm'")
                    return

            # Create an instance of PseudoRandom with a seed (you may want to allow the user to input a seed as well)
            prng = PseudoRandom(seed)

            # Call the selected function based on the user's choice
            if function_name == "Middle Square":
                result = prng.middle_square(quantity)
            elif function_name == "Linear Congruential":
                result = prng.linear_congruential(quantity, a, c, m)
            elif function_name == "Quadratic Congruential":
                result = prng.quadratic_congruential(quantity, a, b, c, m)
            else:
                result = []

            dataframe = self.list_to_dataframe(result)

            # Call the refresh method to update the Treeview with new data
            self.refresh_treeview(dataframe)

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def refresh_treeview(self, dataframe):
        # Clear existing data from the Treeview
        self.tree.delete(*self.tree.get_children())

        # Insert new data into the Treeview
        self.tree["columns"] = list(dataframe.columns)
        for column in dataframe.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)  # Set column width

        for index, row in dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Pack or grid the Treeview as needed
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

    def show_additional_fields(self):
        # Show additional input fields for Linear Congruential and Quadratic Congruential
        if self.function_var.get() in ["Linear Congruential", "Quadratic Congruential"]:
            for widget in [self.a_label, self.a_entry, self.b_label, self.b_entry, self.c_label, self.c_entry, self.m_label, self.m_entry]:
                widget.pack()
        else:
            # Hide the additional input fields if another option is selected
            for widget in [self.a_label, self.a_entry, self.b_label, self.b_entry, self.c_label, self.c_entry, self.m_label, self.m_entry]:
                widget.pack_forget()

# Create the main application window
root = tk.Tk()

# Create an instance of the App class
app = App(root)

# Set up a trace on the function_var to show/hide additional fields based on the selected option
app.function_var.trace_add("write", lambda *args: app.show_additional_fields())

# Start the Tkinter event loop
root.mainloop()
