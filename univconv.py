import customtkinter as ctk
from tkinter import messagebox
from fractions import Fraction
import math
import sys
import os

# ---------- RESOURCE PATH FUNCTION ----------


def resource_path(relative_path):
    """ Get absolute path for PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS')
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------- UNITS ----------


units_dict = {
    "Length": {
        "Miles": 1609.344, "Yards": 0.9144, "Feet": 0.3048, "Inches": 0.0254,
        "Kilometers": 1000.0, "Meters": 1.0, "Centimeters": 0.01, "Millimeters": 0.001
    },
    "Mass": {
        "Milligrams": 0.000001, "Grams": 0.001, "Kilograms": 1.0,
        "Tons": 1000.0, "US Tons": 907.18474, "Pounds": 0.45359237, "Ounces": 0.0283495
    },
    "Area": {
        "Square Kilometers": 1e6, "Square Meters": 1.0, "Square Centimeters": 0.0001,
        "Square Millimeters": 0.000001, "Square Miles": 2.58999e6, "Square Yards": 0.836127,
        "Square Feet": 0.092903, "Square Inches": 0.00064516,
        "Acres": 4046.8564224, "Hectares": 10000.0
    },
    "Volume": {
        "Cubic Kilometers": 1e9, "Cubic Meters": 1.0, "Cubic Centimeters": 1e-6,
        "Cubic Millimeters": 1e-9, "Cubic Miles": 4.16818e9, "Cubic Yards": 0.764555,
        "Cubic Feet": 0.0283168, "Cubic Inches": 1.63871e-5,
        "Liters": 0.001, "Milliliters": 1e-6, "Gallons": 0.00378541, "Cups": 0.00024
    },
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Polar": ["Degrees", "Radians", "Gradians"]
}

singular_units = {
    "Miles": "Mile", "Yards": "Yard", "Feet": "Foot", "Inches": "Inch",
    "Kilometers": "Kilometer", "Meters": "Meter", "Centimeters": "Centimeter",
    "Millimeters": "Millimeter",
    "Milligrams": "Milligram", "Grams": "Gram", "Kilograms": "Kilogram",
    "Tons": "Ton", "US Tons": "US Ton", "Pounds": "Pound", "Ounces": "Ounce",
    "Square Kilometers": "Square Kilometer", "Square Meters": "Square Meter",
    "Square Centimeters": "Square Centimeter", "Square Millimeters": "Square Millimeter",
    "Square Miles": "Square Mile", "Square Yards": "Square Yard",
    "Square Feet": "Square Foot", "Square Inches": "Square Inch",
    "Acres": "Acre", "Hectares": "Hectare",
    "Cubic Kilometers": "Cubic Kilometer", "Cubic Meters": "Cubic Meter",
    "Cubic Centimeters": "Cubic Centimeter", "Cubic Millimeters": "Cubic Millimeter",
    "Cubic Miles": "Cubic Mile", "Cubic Yards": "Cubic Yard", "Cubic Feet": "Cubic Foot",
    "Cubic Inches": "Cubic Inch",
    "Liters": "Liter", "Milliliters": "Milliliter", "Gallons": "Gallon", "Cups": "Cup",
    "Celsius": "Celsius", "Fahrenheit": "Fahrenheit", "Kelvin": "Kelvin",
    "Degrees": "Degree", "Radians": "Radian", "Gradians": "Gradian"
}

current_category = "Length"

# ---------- FUNCTIONS ----------


def update_units(*args):
    global current_category
    current_category = category_var.get()
    units = list(units_dict[current_category].keys()) if isinstance(
        units_dict[current_category], dict) else units_dict[current_category]
    unit_from.set(units[0])
    unit_to.set(units[1])
    combo_from.configure(values=units)
    combo_to.configure(values=units)
    result.set("")
    copy_button.pack_forget()


def convert():
    try:
        value = float(entry.get().strip())
        from_unit = unit_from.get()
        to_unit = unit_to.get()

        if current_category in ["Length", "Mass", "Area", "Volume"]:
            factors = units_dict[current_category]
            base = value * factors[from_unit]
            converted = base / factors[to_unit]

            if converted < 0.0001 or converted > 1e6:
                formatted = f"{converted:,.12f}".rstrip('0').rstrip('.')
            else:
                formatted = f"{converted:,.6f}".rstrip('0').rstrip('.')

            unit_name = singular_units[to_unit] if abs(
                converted) == 1 else to_unit
            result.set(f"{formatted} {unit_name}")

        elif current_category == "Temperature":
            converted = value
            if from_unit == "Celsius":
                if to_unit == "Fahrenheit":
                    converted = value * 9/5 + 32
                elif to_unit == "Kelvin":
                    converted = value + 273.15
            elif from_unit == "Fahrenheit":
                if to_unit == "Celsius":
                    converted = (value - 32) * 5/9
                elif to_unit == "Kelvin":
                    converted = (value - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin":
                if to_unit == "Celsius":
                    converted = value - 273.15
                elif to_unit == "Fahrenheit":
                    converted = (value - 273.15) * 9/5 + 32

            if converted < 0.0001 or converted > 1e6:
                formatted = f"{converted:,.12f}".rstrip('0').rstrip('.')
            else:
                formatted = f"{converted:,.6f}".rstrip('0').rstrip('.')

            unit_name = singular_units[to_unit] if abs(
                converted) == 1 else to_unit
            result.set(f"{formatted} {unit_name}")

        elif current_category == "Polar":
            rad_decimal = None
            rad_str = None
            if from_unit == "Degrees":
                if to_unit == "Radians":
                    rad_decimal = value * math.pi / 180
                    try:
                        frac = Fraction(value).limit_denominator(1000) / 180
                        if frac.numerator == 0:
                            rad_str = "0"
                        elif frac.denominator == 1 and frac.numerator == 1:
                            rad_str = "π"
                        elif frac.denominator == 1:
                            rad_str = f"{frac.numerator}π"
                        else:
                            rad_str = f"{frac.numerator}/{frac.denominator}π"
                    except:
                        rad_str = f"{rad_decimal:.6f}π"
                    result.set(f"{rad_str} ({rad_decimal:.6f} rad)")
                elif to_unit == "Gradians":
                    converted = value * 10/9
                    formatted = f"{converted:,.6f}".rstrip('0').rstrip('.')
                    unit_name = "Gradian" if abs(
                        converted) == 1 else "Gradians"
                    result.set(f"{formatted} {unit_name}")
                else:
                    result.set(f"{value} {to_unit}")

            elif from_unit == "Radians":
                if to_unit == "Degrees":
                    converted = value * 180 / math.pi
                    formatted = f"{converted:,.6f}".rstrip('0').rstrip('.')
                    unit_name = singular_units[to_unit] if abs(
                        converted) == 1 else to_unit
                    result.set(f"{formatted} {unit_name}")
                elif to_unit == "Gradians":
                    converted = value * 180 / math.pi * 10/9
                    formatted = f"{converted:,.6f}".rstrip('0').rstrip('.')
                    unit_name = "Gradian" if abs(
                        converted) == 1 else "Gradians"
                    result.set(f"{formatted} {unit_name}")
                else:
                    result.set(f"{value} {to_unit}")

            elif from_unit == "Gradians":
                if to_unit == "Degrees":
                    converted = value * 0.9
                    formatted = f"{converted:,.6f}".rstrip('0').rstrip('.')
                    unit_name = "Degree" if abs(converted) == 1 else "Degrees"
                    result.set(f"{formatted} {unit_name}")
                elif to_unit == "Radians":
                    degrees = value * 0.9
                    rad_decimal = degrees * math.pi / 180
                    try:
                        frac = Fraction(degrees).limit_denominator(1000) / 180
                        if frac.numerator == 0:
                            rad_str = "0"
                        elif frac.denominator == 1 and frac.numerator == 1:
                            rad_str = "π"
                        elif frac.denominator == 1:
                            rad_str = f"{frac.numerator}π"
                        else:
                            rad_str = f"{frac.numerator}/{frac.denominator}π"
                    except:
                        rad_str = f"{rad_decimal:.6f}π"
                    result.set(f"{rad_str} ({rad_decimal:.6f} rad)")
                else:
                    result.set(f"{value} {to_unit}")

        copy_button.pack(pady=5)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")
        copy_button.pack_forget()


def swap_units():
    from_val = unit_from.get()
    to_val = unit_to.get()
    unit_from.set(to_val)
    unit_to.set(from_val)
    convert()


def copy_result(event=None):
    if result.get().strip() == "":
        messagebox.showerror("Error", "There is nothing to copy.")
        return
    root.clipboard_clear()
    root.clipboard_append(result.get())
    messagebox.showinfo("Copied", "Result copied to clipboard!")


def clear_input(event=None):
    entry.delete(0, "end")
    result.set("")
    copy_button.pack_forget()


def show_help(event=None):
    help_win = ctk.CTkToplevel(root)
    help_win.title("Converter Help")
    help_win.geometry("400x300")
    help_win.resizable(False, False)

    ctk.CTkLabel(help_win, text="Converter Help",
                 font=("Arial", 16, "bold")).pack(pady=10)

    help_text = """\
1. Enter a value and select the units to convert from and to.
2. Press Convert to see the result.
3. Use Swap Units to quickly switch between units.
4. Use Copy Result to copy the conversion result.

Keyboard Shortcuts:
    - Enter: Convert
    - Ctrl+C: Copy result
    - Ctrl+S: Swap units
    - Ctrl+L: Clear input
    - F1: Open help
"""
    textbox = ctk.CTkTextbox(
        help_win,
        width=380,
        height=200,
        font=("Arial", 12),
        state="normal",
        wrap="word"
    )
    textbox.pack(pady=10, padx=10)
    textbox.insert("1.0", help_text)
    textbox.configure(state="disabled")

# ---------- GUI SETUP ----------


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Universal Converter")
root.geometry("520x380")
root.resizable(False, False)

# Icon
root.iconbitmap(resource_path("conv.ico"))

# Top frame
top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.pack(fill="x", pady=10, padx=10)

category_var = ctk.StringVar(value="Length")
category_menu = ctk.CTkOptionMenu(
    top_frame,
    values=list(units_dict.keys()),
    variable=category_var,
    command=update_units,
    fg_color="#2b2b2b",
    button_color="#2b2b2b",
    dropdown_fg_color="#333333"
)
category_menu.pack(side="right")

# Input
entry = ctk.CTkEntry(root, font=("Arial", 16),
                     justify="center", width=250, corner_radius=12)
entry.pack(pady=15)
entry.focus()

# Unit selectors
unit_from = ctk.StringVar()
unit_to = ctk.StringVar()
combo_from = ctk.CTkComboBox(root, values=list(units_dict["Length"].keys()),
                             width=220, corner_radius=12, variable=unit_from)
combo_from.set("Meters")
combo_from.pack(pady=5)
combo_to = ctk.CTkComboBox(root, values=list(units_dict["Length"].keys()),
                           width=220, corner_radius=12, variable=unit_to)
combo_to.set("Kilometers")
combo_to.pack(pady=5)

# Buttons
buttons_frame = ctk.CTkFrame(root, fg_color="transparent")
buttons_frame.pack(pady=15)
convert_button = ctk.CTkButton(buttons_frame, text="Convert", command=convert,
                               width=120, corner_radius=15, border_width=2, border_color="#4CAF50")
convert_button.grid(row=0, column=0, padx=10)
swap_button = ctk.CTkButton(buttons_frame, text="Swap Units", command=swap_units,
                            width=120, corner_radius=15, border_width=2, border_color="#4CAF50")
swap_button.grid(row=0, column=1, padx=10)

# Result
result = ctk.StringVar()
label = ctk.CTkLabel(root, textvariable=result, font=("Arial", 18, "bold"))
label.pack(pady=10)

copy_button = ctk.CTkButton(root, text="Copy Result", command=copy_result,
                            width=150, corner_radius=12, font=("Arial", 12),
                            border_width=2, border_color="#4CAF50")

# Bindings
root.bind('<Return>', lambda event: convert())
root.bind('<Control-l>', clear_input)
root.bind('<Control-c>', copy_result)
root.bind('<Control-s>', lambda event: swap_units())
root.bind('<F1>', show_help)

# Initialize
update_units()

root.mainloop()
