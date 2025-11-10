from pix2text import Pix2Text
from PIL import Image
from sympy import symbols, Eq, solve
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to process image and solve equation
def process_image(image_path):
    # Initialize Pix2Text
    p2t = Pix2Text.from_config()

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Detect equation
    detected = p2t.recognize_text_formula(image, return_text=True)
    if isinstance(detected, list):
        detected_eq = "".join(item.get("text", "") for item in detected)
    else:
        detected_eq = str(detected).strip()

    if not detected_eq:
        return None, "No equation detected"

    # Clean up LaTeX
    detected_eq = detected_eq.strip()
    if detected_eq.startswith("$$") and detected_eq.endswith("$$"):
        detected_eq = detected_eq[2:-2]

    # Convert LaTeX-like syntax to Python
    detected_eq = detected_eq.replace(" ", "")
    detected_eq = re.sub(r"\^\\?\{(\d+)\}", r"**\1", detected_eq)  # x^{2} -> x**2
    detected_eq = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', detected_eq)  # 2x -> 2*x
    detected_eq = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', detected_eq)  # x2 -> x*2
    detected_eq = detected_eq.replace("{", "").replace("}", "")

    # Split at '=' if present
    if "=" in detected_eq:
        lhs, rhs = detected_eq.split("=")
    else:
        lhs, rhs = detected_eq, "0"

    # Solve equation safely using sympy
    try:
        x = symbols("x")
        eq = Eq(eval(lhs), eval(rhs))
        solutions = solve(eq, x)
        return detected_eq, solutions
    except Exception as e:
        return detected_eq, f"Could not solve: {str(e)}"

# Tkinter GUI
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
        return

    equation, solutions = process_image(file_path)
    if equation is None:
        messagebox.showerror("Error", solutions)
    else:
        messagebox.showinfo(
            "Result",
            f"Detected Equation:\n{equation}\n\nSolutions:\n{solutions}"
        )

# Main window
root = tk.Tk()
root.title("Math Lens Clone")
root.geometry("500x250")
root.configure(bg="#f0f4f7")

# Header
header = tk.Label(
    root, text="Math Lens Clone", font=("Helvetica", 20, "bold"),
    bg="#f0f4f7", fg="#333"
)
header.pack(pady=10)

# Instruction
instr = tk.Label(
    root, text="Select an image containing a math equation",
    font=("Arial", 12), bg="#f0f4f7"
)
instr.pack(pady=10)

# Button
button = tk.Button(
    root, text="Open Image", command=open_file,
    font=("Arial", 12), bg="#007bff", fg="white", padx=10, pady=5
)
button.pack(pady=20)

root.mainloop()
