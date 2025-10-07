import tkinter as tk
from math import *

# Convert degrees-based trig functions
def sin_deg(x): return sin(radians(x))
def cos_deg(x): return cos(radians(x))
def tan_deg(x): return tan(radians(x))

# Function to evaluate expressions safely
def evaluate_expression(expression):
    try:
        # Replace special symbols with valid Python math expressions
        expression = expression.replace('√', 'sqrt(')
        expression = expression.replace('^', '**')
        expression = expression.replace('×', '*')
        expression = expression.replace('÷', '/')

        # Convert trig to degree-based
        expression = expression.replace('sin', 'sin_deg')
        expression = expression.replace('cos', 'cos_deg')
        expression = expression.replace('tan', 'tan_deg')

        # Auto-insert missing parentheses after trig and sqrt/log if needed
        funcs = ['sin_deg', 'cos_deg', 'tan_deg', 'sqrt', 'log']
        for func in funcs:
            i = 0
            while i < len(expression):
                i = expression.find(func, i)
                if i == -1:
                    break
                end = i + len(func)
                # If next char is a digit or letter (like sin30), insert '('
                if end < len(expression) and expression[end] not in ['(', ')', '*', '/', '+', '-', '**']:
                    # Find where the number ends
                    j = end
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    expression = expression[:end] + '(' + expression[end:j] + ')' + expression[j:]
                    i = j + 2
                else:
                    i = end + 1

        # Balance parentheses if needed
        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count > close_count:
            expression += ')' * (open_count - close_count)

        # Evaluate and return result
        result = eval(expression)
        return str(result)
    except Exception as e:
        return "Error"

# Button click function
def on_click(symbol):
    if symbol == "=":
        expr = entry.get()
        result = evaluate_expression(expr)
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    elif symbol == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, symbol)

BG_MAIN = "#181818"
BG_ENTRY = "#23272e"
FG_ENTRY = "#f8f8f2"
BG_BTN_NUM = "#282a36"
BG_BTN_OP = "#ffb86c"
FG_BTN_OP = "#282a36"
BG_BTN_FUNC = "#8be9fd"
FG_BTN_FUNC = "#282a36"
BG_BTN_EQ = "#50fa7b"
FG_BTN_EQ = "#282a36"
BG_BTN_CLR = "#ff5555"
FG_BTN_CLR = "#f8f8f2"

# GUI setup
root = tk.Tk()
root.title("Smart Calculator")
root.geometry("360x500")
root.config(bg=BG_MAIN)

entry = tk.Entry(root, font=("Arial", 24), justify="right",
                 bg=BG_ENTRY, fg=FG_ENTRY, bd=0, relief=tk.FLAT)
entry.pack(fill=tk.BOTH, ipadx=8, ipady=15, pady=10, padx=10)


# Buttons layout
buttons = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["√", "(", ")", "="],
    ["sin", "cos", "tan", "log"],
    ["C"]
]

def get_btn_colors(btn):
    if btn in ["+", "-", "×", "÷", "^"]:
        return BG_BTN_OP, FG_BTN_OP
    elif btn in ["sin", "cos", "tan", "log", "√"]:
        return BG_BTN_FUNC, FG_BTN_FUNC
    elif btn == "=":
        return BG_BTN_EQ, FG_BTN_EQ
    elif btn == "C":
        return BG_BTN_CLR, FG_BTN_CLR
    else:
        return BG_BTN_NUM, "white"

# Create buttons
for row in buttons:
    frame = tk.Frame(root, bg=BG_MAIN)
    frame.pack(expand=True, fill="both")
    for btn in row:
        bg, fg = get_btn_colors(btn)
        b = tk.Button(
            frame,
            text=btn,
            font=("Arial", 18),
            relief=tk.GROOVE,
            bd=0,
            fg=fg,
            bg=bg,
            activebackground="#44475a",
            activeforeground=fg,
            command=lambda x=btn: on_click(x)
        )
        b.pack(side="left", expand=True, fill="both", padx=3, pady=3)

root.mainloop()
