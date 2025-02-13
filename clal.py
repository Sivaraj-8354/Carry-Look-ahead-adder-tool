import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class CLA4BitAdder:
    def __init__(self):
        # Initialize 4-bit inputs A, B, and carry-in
        self.A = [0] * 4
        self.B = [0] * 4
        self.Cin = 0

        # Initialize 4-bit outputs Sum and carry-out
        self.Sum = [0] * 4
        self.Cout = 0

    def set_inputs(self, binary_A, binary_B, carry_in):
        if len(binary_A) != 4 or len(binary_B) != 4 or not all(bit in '01' for bit in binary_A + binary_B):
            raise ValueError("Inputs must be 4-bit binary strings")

        self.A = [int(bit) for bit in binary_A]
        self.B = [int(bit) for bit in binary_B]
        self.Cin = int(carry_in)

    def perform_addition(self):
        P = [0] * 4
        G = [0] * 4

        for i in range(4):
            P[i] = self.A[i] ^ self.B[i]
            G[i] = self.A[i] & self.B[i]

        P_out = P[3]
        G_out = G[3]
        for i in range(2, -1, -1):
            P_out = P[i] | (G[i] & P_out)
            G_out = G[i] & G_out

        self.Sum = [P[i] ^ self.Cin for i in range(4)]
        self.Cout = G[3] | (G[2] & P[3]) | (G[1] & P[2]) | (G[0] & P[1])

    def get_outputs(self):
        return ''.join(map(str, self.Sum)), str(self.Cout)


def add_4bit_binary(a, b):
    if len(a) != 4 or len(b) != 4 or not all(bit in '01' for bit in a + b):
        raise ValueError("Input must be 4-bit binary strings")

    result = []
    carry = 0

    for i in range(3, -1, -1):
        bit_sum = int(a[i]) ^ int(b[i]) ^ carry
        carry = (int(a[i]) & int(b[i])) | ((int(a[i]) ^ int(b[i])) & carry)
        result.insert(0, str(bit_sum))

    if carry:
        result.insert(0, str(carry))

    return ''.join(result)

def binary_to_decimal(binary):
    decimal = int(binary, 2)
    return decimal

# GUI functions
def calculate_sum():
    binary_a = entry_a.get()
    binary_b = entry_b.get()

    try:
        result = add_4bit_binary(binary_a, binary_b)
        result_label.config(text=f"Result: {result}")
    except ValueError as e:
        result_label.config(text=str(e))

def convert_to_decimal():
    binary_a = entry_a.get()
    try:
        decimal = binary_to_decimal(binary_a)
        result_label.config(text=f"Decimal: {decimal}")
    except ValueError as e:
        result_label.config(text=str(e))

def convert_to_binary():
    decimal = entry_a.get()
    try:
        binary = bin(int(decimal))[2:]
        result_label.config(text=f"Binary: {binary}")
    except ValueError as e:
        result_label.config(text=str(e))

def clear_entries():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    result_label.config(text="Result: ")

def perform_cla_addition():
    binary_a = entry_a.get()
    binary_b = entry_b.get()

    try:
        cla_adder.set_inputs(binary_a, binary_b, "0")
        cla_adder.perform_addition()
        sum_result, carry_out_result = cla_adder.get_outputs()
        result_label.config(text=f"CLA Result: Sum={sum_result}, Carry-out={carry_out_result}")
        show_cla_circuit_diagram()
    except ValueError as e:
        result_label.config(text=str(e))

def show_cla_circuit_diagram():
    # Create a Toplevel window for the circuit diagram
    circuit_window = tk.Toplevel(root)
    circuit_window.title("CLA Circuit Diagram")

    # Enhanced textual representation of the CLA circuit
    cla_circuit_text = """
    CLA Circuit Diagram (4-bit):

    A0 ─── XOR ──── P0 ──────────────────────── Sum[0]
               │     └───────── AND ─── G0 ──│
    A1 ─── XOR ──── P1 ─── XOR ──── P2 ──────── Sum[1]
               │           │           └──── AND ─── G1 ──│
    A2 ─── XOR ──── P3 ─── XOR ──── P4 ─── XOR ──── P5 ─── Sum[2]
               │           │           │           │     └──── AND ─── G2 ──│
    A3 ─── XOR ──── P6 ─── XOR ──── P7 ─── XOR ──── P8 ─── XOR ──── P9 ──── Sum[3]
                           │           │           │           │     └──── AND ─── G3 ──│
                           └─────────── AND ──────── AND ──────── AND ──────────── OR ── Cout
    """

    # Create a label to display the circuit diagram
    label = tk.Label(circuit_window, text=cla_circuit_text, font=("Courier", 12), justify=tk.LEFT)
    label.pack(padx=10, pady=10)

# GUI setup
root = tk.Tk()
root.title("Binary Operations")

# Set the window size to 800x600
root.geometry("400x700")

# Set a custom style for buttons
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)

# Create and place a frame in the center of the window
frame = ttk.Frame(root)
frame.pack(expand=True)

label_a = tk.Label(frame, text="Input:", font=("Helvetica", 16))
label_a.pack(pady=10)

entry_a = tk.Entry(frame, font=("Helvetica", 14))
entry_a.pack(pady=10)

label_b = tk.Label(frame, text="Input (for addition):", font=("Helvetica", 16))
label_b.pack(pady=10)

entry_b = tk.Entry(frame, font=("Helvetica", 14))
entry_b.pack(pady=10)

add_button = ttk.Button(frame, text="Add Binary", command=calculate_sum, style="TButton")
add_button.pack(pady=10)

decimal_button = ttk.Button(frame, text="Convert to Decimal", command=convert_to_decimal, style="TButton")
decimal_button.pack(pady=10)

binary_button = ttk.Button(frame, text="Convert to Binary", command=convert_to_binary, style="TButton")
binary_button.pack(pady=10)

cla_button = ttk.Button(frame, text="CLA Addition", command=perform_cla_addition, style="TButton")
cla_button.pack(pady=10)

clear_button = ttk.Button(frame, text="Clear", command=clear_entries, style="TButton")
clear_button.pack(pady=10)

result_label = tk.Label(frame, text="Result: ", font=("Helvetica", 16))
result_label.pack(pady=10)

# Add a button to show the CLA circuit diagram
cla_diagram_button = ttk.Button(frame, text="Show CLA Circuit Diagram", command=show_cla_circuit_diagram, style="TButton")
cla_diagram_button.pack(pady=10)

# Create an instance of the CLA4BitAdder class
cla_adder = CLA4BitAdder()

root.mainloop()
