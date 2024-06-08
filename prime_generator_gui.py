import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from sympy import primerange
import csv

def generate_primes(n):
    primes = list(primerange(1, 15485863))[:n]  # 15485863 is approximately the 1,000,000th prime
    return primes

def display_primes():
    try:
        n = int(entry_n.get())
        if n <= 0 or n > 1000000:
            raise ValueError("Please enter a positive integer up to 1,000,000.")
        
        global primes  # Make primes accessible for export
        primes = generate_primes(n)
        
        result_text.delete(1.0, tk.END)  # Clear previous results
        for prime in primes:
            result_text.insert(tk.END, f"{prime}\n")
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))

def export_to_csv():
    if not primes:
        messagebox.showerror("No primes generated", "Please generate primes before exporting.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return  # User cancelled the file dialog
    
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Prime Numbers"])
            for prime in primes:
                writer.writerow([prime])
        messagebox.showinfo("Export Successful", f"Primes exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Prime Number Generator")

# Create and place the input fields and labels
label_n = tk.Label(root, text="Enter the number of primes (up to 1,000,000):")
label_n.pack(pady=5)
entry_n = tk.Entry(root)
entry_n.pack(pady=5)

# Create and place the generate button
button_generate = tk.Button(root, text="Generate Primes", command=display_primes)
button_generate.pack(pady=10)

# Create and place the export button
button_export = tk.Button(root, text="Export to CSV", command=export_to_csv)
button_export.pack(pady=10)

# Create and place the result display
result_text = scrolledtext.ScrolledText(root, width=60, height=20)
result_text.pack(pady=10)

# Start the main event loop
root.mainloop()
