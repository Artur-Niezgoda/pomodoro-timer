from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def end_of_period():
    """
    Make a sound and move the window up in front every time it is called
    """
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
    window.bell()


def reset_timer():
    """
    Stop the timer and reset all the variables to initial values
    """

    window.after_cancel(timer)
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    for widget in sticker_frame.winfo_children():
        widget.destroy()
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    """Start the timer depending on which phase the counter is currently in"""

    global reps
    reps += 1
    if reps == 6:
        count_down(LONG_BREAK_MIN*60)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 1:
        count_down(WORK_MIN*60)
        title_label.config(text="Work", fg=GREEN)
    else:
        count_down(SHORT_BREAK_MIN*60)
        title_label.config(text="Break", fg=PINK)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    """Count down mechanism. Count down until reaches zero, then switch to a new phase and start counting down again.
    If the last phase was long break, reset the timer to initial status"""

    mins = int(count // 60)
    sec = int(count % 60)
    canvas.itemconfig(timer_text, text=f"{mins:02}:{sec:02}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        if reps % 6 != 0:
            end_of_period()
            start_timer()
            if reps % 2 == 0:
                Label(sticker_frame, image=tick, bg=YELLOW, highlightthickness=0).grid(column=(reps//2-1), row=0)
        else:
            end_of_period()
            reset_timer()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=200, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_png = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_png)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

Button(text="Start", font=(FONT_NAME, 16, "bold"), relief=RAISED, command=start_timer).grid(column=0, row=2)
Button(text="Reset", font=(FONT_NAME, 16, "bold"), relief=RAISED, command=reset_timer).grid(column=2, row=2)

tick = PhotoImage(file="tomato_mini.png")
sticker_frame = Frame(window)
sticker_frame.grid(column=1, row=3)

window.mainloop()
