import tkinter as tk
from tkinter import ttk

LEFT_EDGE = 30.0
RIGHT_EDGE = 300.0
BOTTOM_EDGE = 200.0
TOP_EDGE = 20.0

def validate_numeric_input(action, value_if_allowed):
    if action == '1':  # insert
        if value_if_allowed and value_if_allowed.strip():
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True


def draw_line(start, end, color):
    canvas.create_line(start[0], start[1], end[0], end[1], fill=color)


def get_best(A0, A1, B0, B1, C0, C1, point):
    a = A0 + (A1 - A0) * point
    b = B0 + (B1 - B0) * point
    c = C0 + (C1 - C0) * point

    if a > b and a > c:
        return "A"
    if b > c:
        return "B"
    return "C"

def get_worst(A0, A1, B0, B1, C0, C1, point):
    a = A0 + (A1 - A0) * point
    b = B0 + (B1 - B0) * point
    c = C0 + (C1 - C0) * point

    if a < b and a < c:
        return "A"
    if b < c:
        return "B"
    return "C"

def calculate_y(min_val, max_val, value):
    if min_val == max_val:
        return BOTTOM_EDGE
    t = 1 - float(value - min_val) / float(max_val - min_val)
    return float(TOP_EDGE + (BOTTOM_EDGE - TOP_EDGE) * t)

def intersection(a, b, c, d):
    if c - a == d - b:
        return -1
    return (c - a) / (b - a - d + c)

def draw_axes_with_values(min_val, max_val):
    # Draw X-axis
    canvas.create_line(LEFT_EDGE, BOTTOM_EDGE, RIGHT_EDGE, BOTTOM_EDGE)
    canvas.create_text(RIGHT_EDGE, BOTTOM_EDGE + 5, text=str(1), anchor=tk.N)
    canvas.create_text(LEFT_EDGE, BOTTOM_EDGE + 5, text=str(0), anchor=tk.N)

    # Draw Y-axis
    canvas.create_line(LEFT_EDGE, BOTTOM_EDGE, LEFT_EDGE, TOP_EDGE)
    canvas.create_text(LEFT_EDGE - 5, TOP_EDGE, text=str(max_val), anchor=tk.E)
    canvas.create_text(LEFT_EDGE - 5, BOTTOM_EDGE, text=str(min_val), anchor=tk.E)

    canvas.create_line(RIGHT_EDGE, BOTTOM_EDGE, RIGHT_EDGE, TOP_EDGE)
    canvas.create_text(RIGHT_EDGE - 5, TOP_EDGE, text=str(max_val), anchor=tk.E)
    canvas.create_text(LEFT_EDGE - 5, BOTTOM_EDGE, text=str(min_val), anchor=tk.E)

def update_form():
    # Get values from input fields
    values = [float(entry.get()) for entry in entries]

    # Calculate min and max values
    min_val = 0
    max_val = max(values)

    # Clear previous lines and axes on canvas
    canvas.delete("all")

    # Draw axes with min and max values from input fields
    draw_axes_with_values(min_val, max_val)

    # Draw lines on canvas based on the calculated values
    draw_line((LEFT_EDGE, calculate_y(min_val, max_val, values[0])),
              (RIGHT_EDGE, calculate_y(min_val, max_val, values[1])), "red")
    
    draw_line((LEFT_EDGE, calculate_y(min_val, max_val, values[2])),
              (RIGHT_EDGE, calculate_y(min_val, max_val, values[3])), "green")
    
    draw_line((LEFT_EDGE, calculate_y(min_val, max_val, values[4])),
              (RIGHT_EDGE, calculate_y(min_val, max_val, values[5])), "blue")

    # Convert input values to variables for convenience
    A0, A1, B0, B1, C0, C1 = values[0], values[1], values[2], values[3], values[4], values[5]

    intersections = [
        intersection(A0, A1, B0, B1),
        intersection(C0, C1, B0, B1),
        intersection(A0, A1, C0, C1)
    ]

    intersections = [i for i in intersections if i > 0 and i < 1]
    intersections.extend([0, 1])
    intersections.sort()

    result_label.config(text="")

    for i in range(len(intersections) - 1):
        middle = (intersections[i] + intersections[i + 1]) / 2.0
        best = get_best(A0, A1, B0, B1, C0, C1, middle)
        worst = get_worst(A0, A1, B0, B1, C0, C1, middle)

        result_label.config(text=result_label.cget("text") + f"{intersections[i]:.2f} < P(2) < {intersections[i + 1]:.2f}:\n")
        result_label.config(text=result_label.cget("text") + f"Найкращий варіант: {best}\n")
        result_label.config(text=result_label.cget("text") + f"Найгірший варіант: {worst}\n\n")



# Create the main window
root = tk.Tk()
root.title("Аналіз чутливості")

# Labels and input fields for A, B, C (Loss and Win)
labels = ['A for Win:', 'A for Loss:', 'B for Win:', 'B for Loss:', 'C for Win:', 'C for Loss:']
entries = []

for i, label_text in enumerate(labels):
    bg_color = "red" if 'A' in label_text else "green" if 'B' in label_text else "blue"
    label = tk.Label(root, text=label_text, bg=bg_color)
    label.grid(row=i, column=0, padx=5, pady=5)

    vcmd = root.register(validate_numeric_input)
    entry = ttk.Entry(root, validate="key", validatecommand=(vcmd, '%d', '%P'))
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

    # Set default value for empty fields
    if (i == 0):
        def_value = 4
    elif (i == 1):
        def_value = 10
    elif (i == 2 and i == 3):
        def_value = 6
    elif (i == 4):
        def_value = 10
    else:
        def_value = 1

    entry.insert(tk.END, def_value)

# Button to trigger the calculation
update_button = tk.Button(root, text="Update", command=update_form)
update_button.grid(row=len(labels), columnspan=2, padx=5, pady=10)

# Create a label to display the results
result_label = tk.Label(root, text="", wraplength=300, justify=tk.LEFT)
result_label.grid(row=len(labels) + 3, columnspan=2, padx=5, pady=5)

# Canvas to display lines
canvas = tk.Canvas(root, width=350, height=220, bg="white")
canvas.grid(row=len(labels) + 2, columnspan=2, padx=5, pady=5)

root.mainloop()
