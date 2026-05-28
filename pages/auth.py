import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import connect_db


def create_login(parent, on_login):

    for w in parent.winfo_children():
        w.destroy()

    frame = tk.Frame(parent, bg="#f5f6fa")
    frame.pack(fill="both", expand=True)

    # =================================================
    # BACKGROUND
    # =================================================
    canvas = tk.Canvas(frame, highlightthickness=0, bg="#f5f6fa")
    canvas.pack(fill="both", expand=True)

    def draw_gradient(event=None):
        canvas.delete("grad")
        w = frame.winfo_width()
        h = frame.winfo_height()

        for i in range(h):
            r = int(80 + (30 * i / h))
            g = int(120 + (60 * i / h))
            b = 255
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, w, i, fill=color, tags="grad")

    frame.bind("<Configure>", draw_gradient)

    # =================================================
    # LOGO
    # =================================================
    try:
        logo_img = Image.open("assets/logo.png")
        logo_img = logo_img.resize((90, 90))
        logo = ImageTk.PhotoImage(logo_img)
    except:
        logo = None

    # =================================================
    # CARD
    # =================================================
    card = tk.Frame(frame, bg="white")
    card.place(relx=0.5, rely=0.55, anchor="center", width=360, height=500)

    # =================================================
    # LOGO
    # =================================================
    if logo:
        logo_label = tk.Label(card, image=logo, bg="white")
        logo_label.image = logo
        logo_label.pack(pady=(15, 5))

    # =================================================
    # TITLE
    # =================================================
    title_label = tk.Label(
        card,
        text="🔐 Welcome Back",
        bg="white",
        fg="#2f3640",
        font=("Segoe UI", 16, "bold")
    )
    title_label.pack(pady=(5, 5))

    subtitle_label = tk.Label(
        card,
        text="Login to continue",
        bg="white",
        fg="gray",
        font=("Segoe UI", 10)
    )
    subtitle_label.pack()

    # =================================================
    # VARIABLES
    # =================================================
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    signup_fname = tk.StringVar()
    signup_lname = tk.StringVar()
    signup_user = tk.StringVar()
    signup_pass = tk.StringVar()

    # =================================================
    # ENTRY DESIGN
    # =================================================
    def entry(parent_widget, icon, var, show=None):

        container = tk.Frame(parent_widget, bg="#f1f2f6")
        container.pack(pady=10, padx=25, fill="x")

        tk.Label(
            container,
            text=icon,
            bg="#f1f2f6"
        ).pack(side="left", padx=8)

        e = tk.Entry(
            container,
            textvariable=var,
            bd=0,
            bg="#f1f2f6",
            font=("Segoe UI", 10),
            show=show
        )
        e.pack(side="left", fill="x", expand=True, padx=5, pady=8)

        return e

    # =================================================
    # FORMS CONTAINER
    # =================================================
    forms_container = tk.Frame(card, bg="white")
    forms_container.pack(fill="both", expand=True)

    # =================================================
    # LOGIN PAGE
    # =================================================
    login_page = tk.Frame(forms_container, bg="white")

    entry(login_page, "👤", username_var)
    login_pass = entry(login_page, "🔒", password_var, show="*")

    def login():

        user = username_var.get()
        pwd = password_var.get()

        if not user or not pwd:
            messagebox.showerror("Error", "Fill all fields")
            return

        if user == "admin" and pwd == "admin":
            on_login()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_btn = tk.Label(
        login_page,
        text="Login",
        bg="#273c75",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=8,
        cursor="hand2"
    )
    login_btn.pack(pady=20)

    login_btn.bind("<Button-1>", lambda e: login())

    # SWITCH TO SIGNUP
    signup_switch = tk.Label(
        login_page,
        text="Don't have an account? Sign Up",
        bg="white",
        fg="#273c75",
        cursor="hand2",
        font=("Segoe UI", 9, "underline")
    )
    signup_switch.pack()

    # =================================================
    # SIGNUP PAGE
    # =================================================
    signup_page = tk.Frame(forms_container, bg="white")

    entry(signup_page, "👤", signup_fname)
    entry(signup_page, "👤", signup_lname)
    entry(signup_page, "📧", signup_user)
    entry(signup_page, "🔒", signup_pass, show="*")

    def signup():

        if (
            not signup_fname.get() or
            not signup_lname.get() or
            not signup_user.get() or
            not signup_pass.get()
        ):
            messagebox.showerror("Error", "Fill all fields")
            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO accounts (
                    First_Name,
                    Last_Name,
                    Username,
                    Password,
                    User_type
                )
                VALUES (%s,%s,%s,%s,%s)
            """, (
                signup_fname.get(),
                signup_lname.get(),
                signup_user.get(),
                signup_pass.get(),
                "Admin"
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Account created successfully!"
            )

            show_login()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    signup_btn = tk.Label(
        signup_page,
        text="Create Account",
        bg="#273c75",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=8,
        cursor="hand2"
    )
    signup_btn.pack(pady=20)

    signup_btn.bind("<Button-1>", lambda e: signup())

    # SWITCH TO LOGIN
    login_switch = tk.Label(
        signup_page,
        text="Already have an account? Login",
        bg="white",
        fg="#273c75",
        cursor="hand2",
        font=("Segoe UI", 9, "underline")
    )
    login_switch.pack()

    # =================================================
    # PAGE SWITCHING
    # =================================================
    def show_signup():
        login_page.pack_forget()

        title_label.config(text="📝 Create Account")
        subtitle_label.config(text="Register to continue")

        signup_page.pack(fill="both", expand=True)

    def show_login():
        signup_page.pack_forget()

        title_label.config(text="🔐 Welcome Back")
        subtitle_label.config(text="Login to continue")

        login_page.pack(fill="both", expand=True)

    signup_switch.bind("<Button-1>", lambda e: show_signup())
    login_switch.bind("<Button-1>", lambda e: show_login())

    # DEFAULT PAGE
    show_login()

    return frame