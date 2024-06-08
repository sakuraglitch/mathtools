import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import unittest

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def matrix_mult(A, B, mod):
    return [[(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod],
            [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod]]

def matrix_pow(M, power, mod):
    result = [[1, 0], [0, 1]]
    base = M
    while power:
        if power % 2:
            result = matrix_mult(result, base, mod)
        base = matrix_mult(base, base, mod)
        power //= 2
    return result

def fibonacci_mod(n, mod):
    if n == 0:
        return 0
    F = [[1, 1], [1, 0]]
    result = matrix_pow(F, n - 1, mod)
    return result[0][0]

def calculate_pisano_period(n):
    if n <= 1:
        return n
    previous, current = 0, 1
    for i in range(0, n * n):
        previous, current = current, (previous + current) % n
        if previous == 0 and current == 1:
            return i + 1

class PisanoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pisano Period Calculator")
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        
        self.open_button = tk.Button(self.frame, text="Open CSV", command=self.open_csv)
        self.open_button.pack(pady=5)
        
        self.save_button = tk.Button(self.frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.frame, text="Stop Calculation", command=self.stop_calculation, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(self.frame, orient='horizontal', mode='determinate', length=400)
        self.progress_bar.pack(pady=5)
        
        self.results_text = tk.Text(self.frame, height=20, width=50)
        self.results_text.pack(pady=10)
        
        self.primes = []
        self.results = []
        self.stop_flag = False

    def open_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                chunk_size = 1000
                self.primes = []
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    primes = chunk.iloc[:, 0].tolist()
                    invalid_primes = [num for num in primes if not is_prime(num)]
                    if invalid_primes:
                        messagebox.showerror("Error", f"Invalid prime numbers found: {invalid_primes}")
                        return
                    self.primes.extend(primes)
                self.calculate_pisano_periods()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file: {e}")

    def calculate_pisano_periods(self):
        self.stop_flag = False
        self.stop_button.config(state=tk.NORMAL)
        total = len(self.primes)
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = total
        
        self.results = []
        for index, prime in enumerate(self.primes):
            if self.stop_flag:
                messagebox.showinfo("Info", "Calculation stopped by user.")
                break
            self.results.append((prime, calculate_pisano_period(prime)))
            self.progress_bar['value'] += 1
            self.root.update_idletasks()
        
        self.stop_button.config(state=tk.DISABLED)
        self.display_results()

    def display_results(self):
        self.results_text.delete(1.0, tk.END)
        for prime, period in self.results:
            self.results_text.insert(tk.END, f"Prime: {prime}, Pisano Period: {period}\n")

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.DataFrame(self.results, columns=["Prime", "Pisano Period"])
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Results saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save CSV file: {e}")

    def stop_calculation(self):
        self.stop_flag = True

if __name__ == "__main__":
    root = tk.Tk()
    app = PisanoGUI(root)
    root.mainloop()
    
    # Unit Tests
    class TestPisanoPeriod(unittest.TestCase):
        def test_pisano_period(self):
            self.assertEqual(calculate_pisano_period(2), 3)
            self.assertEqual(calculate_pisano_period(3), 8)
            self.assertEqual(calculate_pisano_period(5), 20)
            self.assertEqual(calculate_pisano_period(7), 16)
            self.assertEqual(calculate_pisano_period(11), 10)
            self.assertEqual(calculate_pisano_period(13), 28)
            self.assertEqual(calculate_pisano_period(17), 36)
            self.assertEqual(calculate_pisano_period(19), 18)
            self.assertEqual(calculate_pisano_period(23), 48)
        
        def test_is_prime(self):
            self.assertTrue(is_prime(2))
            self.assertTrue(is_prime(3))
            self.assertTrue(is_prime(5))
            self.assertTrue(is_prime(7))
            self.assertTrue(is_prime(11))
            self.assertTrue(is_prime(13))
            self.assertFalse(is_prime(4))
            self.assertFalse(is_prime(9))
            self.assertFalse(is_prime(15))
            self.assertFalse(is_prime(21))
        
        def test_large_primes(self):
            self.assertEqual(calculate_pisano_period(97), 96)
            self.assertEqual(calculate_pisano_period(101), 50)
            self.assertEqual(calculate_pisano_period(103), 102)
            self.assertEqual(calculate_pisano_period(107), 53)
            self.assertEqual(calculate_pisano_period(109), 54)
    
    unittest.main(argv=[''], exit=False)
