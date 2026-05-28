import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

# =================================================
# IMPORT PAGES
# =================================================
from pages.login import create_login
from pages.profile_panel import ProfilePanel

# ADMIN
from pages.dashboard import create_dashboard
from pages.account_approval import create_account_approval
from pages.trash import create_trash
from pages.teams import create_teams_page

# EMPLOYEE
from pages.Employee.dashboard_employee import create_dashboard_employee
from pages.Employee.team_employee import create_team_employee
from pages.Employee.form_employee import create_form_employee
from pages.Employee.table import create_table

# =================================================
# MAIN WINDOW
# =================================================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Census Management System")

root.after(0, lambda: root.state("zoomed"))
root.minsize(1200, 700)

root.configure(fg_color="#f5f6fa")

# =================================================
# SAFE PAGE CREATOR
# =================================================
def safe_page(create_func, parent):
    try:
        page = create_func(parent)

        if page is None:
            frame = ctk.CTkFrame(parent, fg_color="red")
            ctk.CTkLabel(
                frame,
                text=f"{create_func.__name__} returned None",
                text_color="white"
            ).pack(pady=20)
            return frame

        return page

    except Exception as e:
        print(f"Error loading {create_func.__name__}: {e}")

        frame = ctk.CTkFrame(parent)
        ctk.CTkLabel(
            frame,
            text=f"Error loading page:\n{e}",
            text_color="red"
        ).pack(pady=20)

        return frame


# =================================================
# BUILD MAIN APP
# =================================================
def build_main_app(current_user):

    # Clear old widgets
    for widget in root.winfo_children():
        widget.destroy()

    # =================================================
    # MAIN FRAME
    # =================================================
    main = ctk.CTkFrame(root, fg_color="#f5f6fa")
    main.pack(fill="both", expand=True)

    # =================================================
    # NAVBAR
    # =================================================
    navbar = ctk.CTkFrame(
        main,
        fg_color="#1e2566",
        height=67,
        corner_radius=14
    )

    navbar.pack(
        side="top",
        fill="x",
        padx=12,
        pady=(10, 0)
    )

    navbar.pack_propagate(False)

    # =================================================
    # LEFT NAV
    # =================================================
    left_nav = ctk.CTkFrame(navbar, fg_color="transparent")
    left_nav.pack(side="left", padx=16, fill="y")

    # Logo
    try:
        logo_img = Image.open("assets/logo.png")

        logo = ctk.CTkImage(
            light_image=logo_img,
            dark_image=logo_img,
            size=(36, 36)
        )

        logo_label = ctk.CTkLabel(
            left_nav,
            image=logo,
            text=""
        )

        logo_label.pack(side="left", padx=(0, 10), pady=14)

    except Exception as e:
        print("Logo error:", e)

    # Brand text
    brand_stack = ctk.CTkFrame(left_nav, fg_color="transparent")
    brand_stack.pack(side="left", pady=14)

    ctk.CTkLabel(
        brand_stack,
        text="Census MS",
        text_color="white",
        font=("Poppins", 13, "bold")
    ).pack(anchor="w")

    ctk.CTkLabel(
        brand_stack,
        text=f"Welcome, {current_user.get('First_Name', 'User')}",
        text_color="#8899cc",
        font=("Segoe UI", 11)
    ).pack(anchor="w")

    # =================================================
    # DIVIDER
    # =================================================
    def make_divider(parent):
        ctk.CTkFrame(
            parent,
            fg_color="#3b437d",
            width=1,
            height=28
        ).pack(side="left", padx=12, pady=18)

    make_divider(navbar)

    # =================================================
    # CENTER NAV
    # =================================================
    center_nav = ctk.CTkFrame(navbar, fg_color="transparent")
    center_nav.pack(side="left", fill="both", expand=True)

    # =================================================
    # RIGHT NAV
    # =================================================
    right_nav = ctk.CTkFrame(navbar, fg_color="transparent")
    right_nav.pack(side="right", padx=16, fill="y")

    # Avatar
    first = current_user.get("First_Name", "?")
    last = current_user.get("Last_Name", "?")

    initials = (
        (first[0] + last[0]).upper()
        if first and last
        else "U"
    )

    avatar = ctk.CTkLabel(
        right_nav,
        text=initials,
        text_color="white",
        fg_color="#5b6ee1",
        font=("Poppins", 12, "bold"),
        width=36,
        height=36,
        corner_radius=18,
        cursor="hand2"
    )

    avatar.pack(side="left", padx=(0, 8), pady=14)

    make_divider(right_nav)

    # =================================================
    # LOGOUT
    # =================================================
    def logout():

        confirm = messagebox.askyesno(
            "Logout Confirmation",
            "Are you sure you want to logout?"
        )

        if confirm:

            for widget in root.winfo_children():
                widget.destroy()

            create_login(root, build_main_app)

    logout_btn = ctk.CTkLabel(
        right_nav,
        text="⏻ Logout",
        text_color="#ff8080",
        font=("Segoe UI Semibold", 12),
        padx=12,
        cursor="hand2"
    )

    logout_btn.pack(side="left", pady=14)

    logout_btn.bind(
        "<Button-1>",
        lambda e: logout()
    )

    # =================================================
    # PROFILE PANEL
    # =================================================
    profile = ProfilePanel(
        main,
        current_user,
        navbar_height=64
    )

    avatar.bind(
        "<Button-1>",
        lambda e: profile.toggle()
    )

    # =================================================
    # CONTENT AREA
    # =================================================
    content = ctk.CTkFrame(main, fg_color="#f5f6fa")

    content.pack(
        fill="both",
        expand=True,
        pady=(8, 0)
    )

    # =================================================
    # USER TYPE
    # =================================================
    user_type = current_user.get("User_type", "Employee")

    # =================================================
    # PAGES
    # =================================================
    if user_type == "Admin":

        teams_page = safe_page(create_teams_page, content)

        pages = {
            "dashboard": safe_page(create_dashboard, content),
            "approval": safe_page(create_account_approval, content),
            "trash": create_trash(
                content,
                teams_page_ref=teams_page
            ),
            "teams": teams_page,
        }

    else:

        pages = {
            "dashboard": safe_page(create_dashboard_employee, content),
            "teams": safe_page(create_team_employee, content),
            "table": safe_page(create_table, content),
            "form": safe_page(create_form_employee, content),
        }

    buttons = {}
    active_page = ["dashboard"]

    # =================================================
    # NAV BUTTON
    # =================================================
    def create_btn(text, key):

        btn = ctk.CTkLabel(
            center_nav,
            text=text,
            text_color="#99aadd",
            fg_color="transparent",
            font=("Segoe UI Semibold", 13),
            padx=16,
            pady=8,
            cursor="hand2",
            corner_radius=8
        )

        btn.pack(side="left", padx=3, pady=18)

        btn.bind(
            "<Button-1>",
            lambda e: show_page(key)
        )

        buttons[key] = btn

        # Hover
        def on_enter(e):
            if key != active_page[0]:
                btn.configure(
                    fg_color="#2d356b",
                    text_color="white"
                )

        def on_leave(e):
            if key != active_page[0]:
                btn.configure(
                    fg_color="transparent",
                    text_color="#99aadd"
                )

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # =================================================
    # ACTIVE BUTTON
    # =================================================
    def set_active(name):

        active_page[0] = name

        for k, btn in buttons.items():

            if k == name:
                btn.configure(
                    fg_color="#3b437d",
                    text_color="white"
                )

            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#99aadd"
                )

    # =================================================
    # SHOW PAGE
    # =================================================
    def show_page(name):

        for p in pages.values():
            p.pack_forget()

        pages[name].pack(
            fill="both",
            expand=True
        )

        set_active(name)

        # Refresh trash
        if (
            name == "trash"
            and hasattr(pages["trash"], "load_trash")
        ):
            pages["trash"].load_trash()

    # =================================================
    # NAVIGATION
    # =================================================
    if user_type == "Admin":

        create_btn("Dashboard", "dashboard")
        create_btn("Approvals", "approval")
        create_btn("Trash", "trash")
        create_btn("Teams", "teams")

    else:

        create_btn("Dashboard", "dashboard")
        create_btn("Teams", "teams")
        create_btn("Residents", "table")
        create_btn("Add Resident", "form")

    # =================================================
    # DEFAULT PAGE
    # =================================================
    show_page("dashboard")


# =================================================
# START APP
# =================================================
create_login(root, build_main_app)

root.mainloop()