import tkinter as tk
import random
import winsound

BG = "#121212"
FG = "#E0E0E0"
BTN = "#1E1E1E"
ACCENT = "#F0D4FC"
ERROR = "#ff5555"

root = tk.Tk()
root.title("super kalkulator")
root.configure(bg=BG)
root.resizable(False, False)

def click_sound():
    winsound.Beep(600, 50)

def on_enter(e):
    e.widget.config(bg=ACCENT, fg="black")

def on_leave(e):
    e.widget.config(bg=BTN, fg=FG)

tk.Label(
    root,
    text="witam w super kalkulatorze",
    bg=BG,
    fg=FG,
    font=("Comic Sans MS", 14, "bold")
).grid(row=0, column=0, columnspan=4, pady=10)

entry_style = {
    "bg": "#1A1A1A",
    "fg": FG,
    "insertbackground": FG,
    "justify": "right",
    "font": ("Comic Sans MS", 14),
    "relief": "flat",
}

entry_a = tk.Entry(root, **entry_style)
entry_a.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
entry_a.insert(0, "")

op_label = tk.Label(root, text="Możesz wpisywać liczby ręcznie lub klikać przyciski", bg=BG, fg=FG,
                    font=("Comic Sans MS", 10))
op_label.grid(row=2, column=0, columnspan=4)

result = tk.Label(root, text="Wynik:", bg=BG, fg=FG, font=("Comic Sans MS", 13, "bold"))
result.grid(row=4, column=0, columnspan=4, pady=10)

def animate_result(text):
    result.config(text="", fg=random.choice(["#00ffcc", "#ffaa00", "#ff77ff"]))
    for i in range(len(text)):
        root.after(i * 40, lambda x=text[:i+1]: result.config(text=x))

def calc():
    click_sound()
    expr = entry_a.get().replace("×", "*").replace("÷", "/")
    try:
        r = eval(expr)
        r = int(r) if isinstance(r, float) and r.is_integer() else r
        animate_result(f"Wynik: {r}")
        start_confetti(5)
    except ZeroDivisionError:
        result.config(text="Dzielenie przez 0", fg=ERROR)
    except:
        result.config(text="Błąd danych", fg=ERROR)

def clear():
    click_sound()
    entry_a.delete(0, tk.END)
    result.config(text="Wynik:", fg=FG)

def add_to_entry(char):
    click_sound()
    entry_a.insert(tk.END, char)

buttons_layout = [
    ['7', '8', '9', '÷'],
    ['4', '5', '6', '×'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

for r, row in enumerate(buttons_layout, start=5):
    for c, char in enumerate(row):
        if char == '=':
            btn = tk.Button(root, text=char, width=5, height=2,
                            bg=ACCENT, fg="black", relief="flat",
                            font=("Comic Sans MS", 12, "bold"), command=calc)
        else:
            btn = tk.Button(root, text=char, width=5, height=2,
                            bg=BTN, fg=FG, relief="flat",
                            font=("Comic Sans MS", 12, "bold"),
                            command=lambda ch=char: add_to_entry(ch))
        btn.grid(row=r, column=c, padx=3, pady=3)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

btn_c = tk.Button(root, text="C", width=5, bg=BTN, fg=FG, relief="flat",
                  font=("Comic Sans MS", 12, "bold"), command=clear)
btn_c.grid(row=9, column=0, columnspan=4, sticky="we", padx=3, pady=3)
btn_c.bind("<Enter>", on_enter)
btn_c.bind("<Leave>", on_leave)

root.bind("<Return>", lambda e: calc())
root.bind("<Escape>", lambda e: clear())

confetti_pieces = []

def start_confetti(duration_seconds=5):
    canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height(), bg="", highlightthickness=0)
    canvas.place(x=0, y=0)
    confetti_pieces.clear()
    for _ in range(50):
        x = random.randint(0, root.winfo_width())
        y = random.randint(-50, 0)
        color = random.choice(["#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff"])
        size = random.randint(5, 10)
        piece = canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
        confetti_pieces.append((piece, size, random.randint(2,5)))
    root.after(duration_seconds*1000, lambda: canvas.destroy())
    animate_confetti(canvas)

def animate_confetti(canvas):
    for piece, size, speed in confetti_pieces:
        canvas.move(piece, 0, speed)
        pos = canvas.coords(piece)
        if pos[1] > root.winfo_height():
            x = random.randint(0, root.winfo_width())
            canvas.coords(piece, x, -size, x+size, 0)
    canvas.after(50, lambda: animate_confetti(canvas))

root.mainloop()
