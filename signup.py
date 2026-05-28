import tkinter as tk
from tkinter import messagebox


def create_signup(parent):

    frame = tk.Frame(parent, bg="#f5f6fa")

    card = tk.Frame(frame, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card, text="Sign Up", font=("Segoe UI", 20, "bold"), bg="white").pack(pady=20)

    # ---------------- USERNAME ----------------
    tk.Label(card, text="Username", bg="white").pack(anchor="w", padx=20)
    username_var = tk.StringVar()
    tk.Entry(card, textvariable=username_var, width=30).pack(padx=20, pady=5)

    # ---------------- PASSWORD ----------------
    tk.Label(card, text="Password", bg="white").pack(anchor="w", padx=20)
    password_var = tk.StringVar()
    password_entry = tk.Entry(card, textvariable=password_var, width=30, show="*")
    password_entry.pack(padx=20, pady=5)

    # ---------------- CONFIRM PASSWORD ----------------
    tk.Label(card, text="Confirm Password", bg="white").pack(anchor="w", padx=20)
    confirm_var = tk.StringVar()
    confirm_entry = tk.Entry(card, textvariable=confirm_var, width=30, show="*")
    confirm_entry.pack(padx=20, pady=5)

    # ---------------- SHOW/HIDE ----------------
    show = {"state": False}

    def toggle():
        show["state"] = not show["state"]

        if show["state"]:
            password_entry.config(show="")
            confirm_entry.config(show="")
            toggle_btn.config(text="Hide")
        else:
            password_entry.config(show="*")
            confirm_entry.config(show="*")
            toggle_btn.config(text="Show")

    toggle_btn = tk.Button(card, text="Show Password", command=toggle, bg="#dcdde1", relief="flat")
    toggle_btn.pack(pady=5)

    # ---------------- SIGNUP FUNCTION ----------------
    def signup():
        if not username_var.get() or not password_var.get():
            messagebox.showerror("Error", "All fields are required")
            return

        if password_var.get() != confirm_var.get():
            messagebox.showerror("Error", "Passwords do not match")
            return

        messagebox.showinfo("Success", "Account created!")

    tk.Button(card, text="Sign Up", bg="#44bd32", fg="white", width=25, command=signup).pack(pady=15)

    return frame