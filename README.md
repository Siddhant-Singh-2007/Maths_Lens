# Math Lens Clone - Backend

This is a Python-based backend application that can recognize math equations from an image and solve them automatically. It uses **Pix2Text** for OCR (Optical Character Recognition) and **SymPy** for solving equations. The interface is built with **Tkinter**.

---

## Features

- Open an image containing a math equation.
- Automatically detect the equation using OCR.
- Solve linear, quadratic, and simple algebraic equations.
- Display the detected equation and its solutions in a simple GUI window.

---

## Screenshots

![Screenshot](screenshot.png)  
*(Replace with your actual screenshot)*

---

## Requirements

- Python 3.10 or higher
- pip

Dependencies are listed in `requirements.txt`:

pip install -r requirements.txt


```txt
pix2text==1.1.0
Pillow==10.0.0
sympy==1.12
onnxruntime==1.23.2
rapidocr>=3.0
