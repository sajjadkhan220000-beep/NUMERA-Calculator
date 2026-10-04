import math
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk


COLOR_BACKGROUND = "#F3F9FE"
COLOR_TEXT = "#243D53"
COLOR_DISPLAY = "#FFFFFF"
COLOR_DISPLAY_TEXT = "#20384F"
COLOR_KEY = "#FFFFFF"
COLOR_KEY_ACTIVE = "#D7EDFB"
COLOR_OPERATOR = "#D8EEFB"
COLOR_FUNCTION = "#EAF6FD"
COLOR_FUNCTION_ACTIVE = "#D1EAF9"
COLOR_CLEAR = "#CBE7F8"
COLOR_PRIMARY = "#A8D8F3"
COLOR_HOME = "#FFFFFF"
COLOR_HOME_GRID = "#E8F2F9"
COLOR_HOME_TEXT = "#243D53"


# These variables keep track of the current calculation.
first_number = None
current_operator = None
start_new_number = True


def press_number(value):
    """Add a digit or decimal point to the display."""
    global start_new_number

    if start_new_number:
        display_var.set("0" if value == "." else value)
        start_new_number = False
        return

    current_text = display_var.get()
    if value == "." and "." in current_text:
        return
    if current_text == "0" and value != ".":
        display_var.set(value)
    else:
        display_var.set(current_text + value)


def choose_operator(operator):
    """Save the first number and the chosen operation."""
    global first_number, current_operator, start_new_number

    try:
        first_number = float(display_var.get())
    except ValueError:
        display_var.set("Error")
        start_new_number = True
        return

    current_operator = operator
    start_new_number = True


def calculate():
    """Perform the saved operation with the displayed number."""
    global first_number, current_operator, start_new_number

    if first_number is None or current_operator is None:
        return

    try:
        second_number = float(display_var.get())
        if current_operator == "+":
            result = first_number + second_number
        elif current_operator == "-":
            result = first_number - second_number
        elif current_operator == "*":
            result = first_number * second_number
        elif current_operator == "/":
            if second_number == 0:
                display_var.set("Cannot divide by zero")
                first_number = None
                current_operator = None
                start_new_number = True
                return
            result = first_number / second_number
        else:
            return

        display_var.set(str(result))
        first_number = result
        current_operator = None
        start_new_number = True
    except ValueError:
        display_var.set("Error")
        first_number = None
        current_operator = None
        start_new_number = True


def clear():
    """Reset the calculator."""
    global first_number, current_operator, start_new_number

    display_var.set("0")
    first_number = None
    current_operator = None
    start_new_number = True


def press_constant(value):
    """Show a scientific constant and start a new number."""
    global start_new_number

    display_var.set(str(value))
    start_new_number = True


def scientific_operation(operation):
    """Apply a scientific function to the displayed number."""
    global first_number, current_operator, start_new_number

    try:
        number = float(display_var.get())
        if operation == "sin":
            result = math.sin(math.radians(number))
        elif operation == "cos":
            result = math.cos(math.radians(number))
        elif operation == "tan":
            result = math.tan(math.radians(number))
        elif operation == "sqrt":
            result = math.sqrt(number)
        elif operation == "square":
            result = number ** 2
        elif operation == "reciprocal":
            result = 1 / number
        elif operation == "log":
            result = math.log10(number)
        elif operation == "ln":
            result = math.log(number)
        else:
            return

        display_var.set(f"{result:.10g}")
        first_number = None
        current_operator = None
        start_new_number = True
    except (ValueError, ZeroDivisionError, OverflowError):
        display_var.set("Error")
        first_number = None
        current_operator = None
        start_new_number = True


def make_app_icon(size=96):
    """Draw a square calculator mark based on the supplied NUMERA logo."""
    pixels = [[COLOR_HOME for _ in range(size)] for _ in range(size)]
    left = size * 0.015
    right = size * 0.985
    top = size * 0.015
    bottom = size * 0.985
    corner_radius = size * 0.14

    for y in range(size):
        for x in range(size):
            nearest_x = min(max(x, left + corner_radius), right - corner_radius)
            nearest_y = min(max(y, top + corner_radius), bottom - corner_radius)
            if (x - nearest_x) ** 2 + (y - nearest_y) ** 2 > corner_radius ** 2:
                continue

            horizontal = x / size
            vertical = y / size
            red = int(8 + 26 * horizontal + 6 * vertical)
            green = int(111 + 95 * horizontal + 5 * vertical)
            blue = int(239 - 20 * horizontal - 57 * vertical)
            pixels[y][x] = f"#{red:02x}{green:02x}{blue:02x}"

            if x > size * 0.76 and y > size * 0.68 and y > x * 0.72:
                pixels[y][x] = "#F47D45"

    def draw_curve(points, color, thickness):
        segments = []
        for start, end in zip(points, points[1:]):
            segments.append((start[0] * size, start[1] * size, end[0] * size, end[1] * size))

        for y in range(size):
            for x in range(size):
                for x1, y1, x2, y2 in segments:
                    dx = x2 - x1
                    dy = y2 - y1
                    length_squared = dx * dx + dy * dy
                    if not length_squared:
                        continue
                    fraction = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / length_squared))
                    distance_squared = (x - (x1 + fraction * dx)) ** 2 + (y - (y1 + fraction * dy)) ** 2
                    if distance_squared <= thickness * thickness:
                        if pixels[y][x] != COLOR_HOME:
                            pixels[y][x] = color
                        break

    draw_curve(
        [(0.04, 0.61), (0.12, 0.34), (0.38, 0.08), (0.69, 0.07), (0.96, 0.12)],
        "#73F4E7",
        size * 0.05,
    )
    draw_curve(
        [(0.96, 0.12), (0.94, 0.46), (0.84, 0.72), (0.65, 0.88), (0.27, 0.96)],
        "#27D4DC",
        size * 0.05,
    )

    def paint_if_inside(x, y, condition, color):
        if condition and 0 <= x < size and 0 <= y < size and pixels[y][x] != COLOR_HOME:
            pixels[y][x] = color

    def paint_rounded_rectangle(x1, y1, x2, y2, radius, color):
        for y in range(max(0, int(y1)), min(size, int(y2) + 1)):
            for x in range(max(0, int(x1)), min(size, int(x2) + 1)):
                nearest_x = min(max(x, x1 + radius), x2 - radius)
                nearest_y = min(max(y, y1 + radius), y2 - radius)
                if (x - nearest_x) ** 2 + (y - nearest_y) ** 2 <= radius ** 2:
                    pixels[y][x] = color

    display_left = int(size * 0.17)
    display_top = int(size * 0.39)
    display_right = int(size * 0.72)
    display_bottom = int(size * 0.59)
    paint_rounded_rectangle(display_left, display_top, display_right, display_bottom, size * 0.045, "#F7FAFC")

    glyphs = {
        "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
        "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
        "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
        "=": ("00000", "11111", "00000", "11111", "00000", "00000", "00000"),
    }
    scale = max(1, size // 48)
    glyph_x = int(size * 0.22)
    glyph_y = int(size * 0.425)
    for character in "123=":
        for row_index, row in enumerate(glyphs[character]):
            for column_index, bit in enumerate(row):
                if bit == "1":
                    for offset_y in range(scale):
                        for offset_x in range(scale):
                            x = glyph_x + column_index * scale + offset_x
                            y = glyph_y + row_index * scale + offset_y
                            paint_if_inside(x, y, True, "#1C2A3A")
        glyph_x += 6 * scale

    stroke = max(2, int(size * 0.055))
    plus_x = int(size * 0.77)
    plus_y = int(size * 0.23)
    multiply_x = int(size * 0.82)
    multiply_y = int(size * 0.51)
    divide_x = int(size * 0.29)
    divide_y = int(size * 0.76)
    minus_x = int(size * 0.59)
    minus_y = int(size * 0.76)

    for y in range(size):
        for x in range(size):
            is_plus = abs(x - plus_x) <= stroke and abs(y - plus_y) < size * 0.105 or abs(y - plus_y) <= stroke and abs(x - plus_x) < size * 0.105
            is_multiply = size * 0.70 < x < size * 0.94 and size * 0.41 < y < size * 0.64 and (
                abs((x - multiply_x) - (y - multiply_y)) <= stroke
                or abs((x - multiply_x) + (y - multiply_y)) <= stroke
            )
            is_divide = size * 0.18 < x < size * 0.43 and (
                abs(y - divide_y) <= stroke
                or (x - divide_x) ** 2 + (y - (divide_y - size * 0.10)) ** 2 < (stroke * 1.5) ** 2
                or (x - divide_x) ** 2 + (y - (divide_y + size * 0.10)) ** 2 < (stroke * 1.5) ** 2
            )
            is_minus = size * 0.47 < x < size * 0.70 and abs(y - minus_y) <= stroke
            if is_plus or is_multiply or is_divide or is_minus:
                paint_if_inside(x, y, True, "#FFFFFF")

    image = tk.PhotoImage(width=size, height=size)
    image.put(" ".join("{" + " ".join(row) + "}" for row in pixels))
    return image


def rounded_button(parent, text, command, background, foreground, font, width=76, height=52):
    """Create a consistently sized rounded button using a Canvas."""
    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=parent.cget("bg"),
        highlightthickness=0,
        bd=0,
        cursor="hand2",
        takefocus=True,
    )
    inset = 2
    radius = min(height * 0.32, width * 0.18)
    points = (
        inset + radius, inset, width - inset - radius, inset,
        width - inset, inset + radius, width - inset, height - inset - radius,
        width - inset - radius, height - inset, inset + radius, height - inset,
        inset, height - inset - radius, inset, inset + radius,
    )
    shape = canvas.create_polygon(
        points,
        smooth=True,
        splinesteps=20,
        fill=background,
        outline=background,
    )
    canvas.create_text(width / 2, height / 2, text=text, fill="#000000", font=font)

    def activate(event=None):
        command()

    canvas.bind("<Enter>", lambda event: canvas.itemconfigure(shape, fill=COLOR_KEY_ACTIVE, outline=COLOR_KEY_ACTIVE))
    canvas.bind("<Leave>", lambda event: canvas.itemconfigure(shape, fill=background, outline=background))
    canvas.bind("<Button-1>", activate)
    canvas.bind("<Return>", activate)
    canvas.bind("<space>", activate)
    return canvas


def show_menu():
    """Display the calculator mode choices."""
    for widget in window.winfo_children():
        widget.destroy()

    window.title("NUMERA Calculator")
    window.configure(padx=30, pady=24, bg=COLOR_HOME)
    window.geometry("440x500")

    tk.Label(window, image=home_logo, bg=COLOR_HOME, bd=0).pack(pady=(0, 6))

    tk.Label(
        window,
        text="Choose a calculator",
        font=("Segoe UI", 15, "bold"),
        bg=COLOR_HOME,
        fg=COLOR_HOME_TEXT,
    ).pack(pady=(0, 10))

    rounded_button(
        window,
        "Scientific Calculator",
        lambda: show_calculator("scientific"),
        COLOR_PRIMARY,
        COLOR_HOME_TEXT,
        ("Segoe UI", 14, "bold"),
        width=360,
        height=60,
    ).pack(fill="x", pady=6)
    rounded_button(
        window,
        "Simple Calculator",
        lambda: show_calculator("simple"),
        COLOR_KEY,
        COLOR_HOME_TEXT,
        ("Segoe UI", 14, "bold"),
        width=360,
        height=60,
    ).pack(fill="x", pady=6)


def show_calculator(mode):
    """Build the selected calculator's display and buttons."""
    global first_number, current_operator, start_new_number, display_var

    first_number = None
    current_operator = None
    start_new_number = True

    for widget in window.winfo_children():
        widget.destroy()

    is_scientific = mode == "scientific"
    column_count = 4
    window.title("Scientific Calculator" if is_scientific else "Simple Calculator")
    window.configure(padx=12, pady=12, bg=COLOR_BACKGROUND)
    window.geometry("440x680" if is_scientific else "410x500")

    rounded_button(
        window,
        "Back",
        show_menu,
        COLOR_KEY,
        COLOR_TEXT,
        ("Segoe UI", 10, "bold"),
        width=84,
        height=38,
    ).grid(row=0, column=0, sticky="w", padx=4, pady=(0, 8))

    display_var = tk.StringVar(value="0")
    display = tk.Entry(
        window,
        textvariable=display_var,
        font=("Segoe UI", 24),
        justify="right",
        state="readonly",
        readonlybackground=COLOR_DISPLAY,
        fg=COLOR_DISPLAY_TEXT,
        width=16,
        bd=0,
    )
    display.grid(row=1, column=0, columnspan=column_count, padx=4, pady=(0, 8), ipady=10)

    for column in range(column_count):
        window.grid_columnconfigure(column, weight=1, uniform="calculator-key")

    if is_scientific:
        buttons = [
            ("sin", 2, 0), ("cos", 2, 1), ("tan", 2, 2), ("sqrt", 2, 3),
            ("x²", 3, 0), ("1/x", 3, 1), ("log", 3, 2), ("ln", 3, 3),
            ("π", 4, 0), ("e", 4, 1), ("C", 4, 2), ("/", 4, 3),
            ("7", 5, 0), ("8", 5, 1), ("9", 5, 2), ("*", 5, 3),
            ("4", 6, 0), ("5", 6, 1), ("6", 6, 2), ("-", 6, 3),
            ("1", 7, 0), ("2", 7, 1), ("3", 7, 2), ("+", 7, 3),
            ("0", 8, 0), (".", 8, 1),
        ]
        equals_row = 9
    else:
        buttons = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
            ("C", 5, 0), ("0", 5, 1), (".", 5, 2), ("+", 5, 3),
        ]
        equals_row = 6

    for label, row, column in buttons:
        if label == "C":
            command = clear
            color = COLOR_CLEAR
            text_color = COLOR_TEXT
        elif label in "+-*/":
            command = lambda operation=label: choose_operator(operation)
            color = COLOR_OPERATOR
            text_color = COLOR_BACKGROUND
        elif label in {"sin", "cos", "tan", "sqrt", "x²", "1/x", "log", "ln"}:
            operation = {"x²": "square", "1/x": "reciprocal", "sqrt": "sqrt"}.get(label, label)
            command = lambda function=operation: scientific_operation(function)
            color = COLOR_FUNCTION
            text_color = COLOR_TEXT
        elif label in {"π", "e"}:
            value = math.pi if label == "π" else math.e
            command = lambda constant=value: press_constant(constant)
            color = COLOR_FUNCTION
            text_color = COLOR_TEXT
        else:
            command = lambda digit=label: press_number(digit)
            color = COLOR_KEY
            text_color = COLOR_TEXT

        rounded_button(
            window,
            label,
            command,
            color,
            text_color,
            ("Segoe UI", 13 if is_scientific else 16, "bold"),
            width=76,
            height=52,
        ).grid(row=row, column=column, padx=4, pady=4, sticky="nsew")

    rounded_button(
        window,
        "=",
        calculate,
        COLOR_PRIMARY,
        COLOR_DISPLAY_TEXT,
        ("Segoe UI", 16, "bold"),
        width=100,
        height=52,
    ).grid(row=equals_row, column=0, columnspan=column_count, padx=4, pady=(4, 0), sticky="nsew")


window = tk.Tk()
window.resizable(False, False)
logo_path = Path(__file__).resolve().with_name("images (2).jpg")
with Image.open(logo_path) as logo_file:
    logo_source = logo_file.convert("RGB")
app_icon = ImageTk.PhotoImage(logo_source.resize((96, 96), Image.Resampling.LANCZOS))
home_logo = ImageTk.PhotoImage(logo_source.resize((220, 220), Image.Resampling.LANCZOS))
window.iconphoto(True, app_icon)
show_menu()
window.mainloop()
