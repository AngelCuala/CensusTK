import tkinter as tk
from tkinter import ttk
from db import connect_db


def open_registered_accounts(parent):

    accounts_win = tk.Toplevel(parent)
    accounts_win.title("Registered Accounts")
    accounts_win.geometry("900x520")
    accounts_win.config(bg="#f5f6fa")

    # ================= MODERN HEADER =================
    header = tk.Frame(accounts_win, bg="#4353BD", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Registered Accounts",
        font=("Segoe UI Semibold", 20),
        bg="#4353BD",
        fg="white"
    ).pack(anchor="w", padx=25, pady=(18, 0))

    tk.Label(
        header,
        text="Manage system users and access roles",
        font=("Segoe UI", 10),
        bg="#4353BD",
        fg="#dcdde1"
    ).pack(anchor="w", padx=25)

    # ================= MAIN CONTAINER =================
    container = tk.Frame(
        accounts_win,
        bg="white",
        highlightbackground="#dcdde1",
        highlightthickness=1
    )

    container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    # ================= TREEVIEW STYLE =================
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview",
        background="white",
        foreground="#2f3640",
        rowheight=32,
        fieldbackground="white",
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI Semibold", 10),
        background="#f1f2f6",
        foreground="#2f3640"
    )

    style.map(
        "Treeview",
        background=[("selected", "#4353BD")],
        foreground=[("selected", "white")]
    )

    # ================= SCROLLBAR =================
    scroll_y = ttk.Scrollbar(container, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    # ================= TREEVIEW =================
    columns = ("ID", "Name", "Username", "Email", "User Type")

    tree = ttk.Treeview(
        container,
        columns=columns,
        show="headings",
        height=18,
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=tree.yview)

    # column setup (cleaner spacing)
    widths = [60, 180, 140, 220, 120]

    for col, w in zip(columns, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ================= LOAD DATA =================
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            User_ID,
            First_Name,
            Last_Name,
            Username,
            Email,
            User_type
        FROM accounts
        ORDER BY User_ID DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        fullname = f"{row[1]} {row[2]}"

        tree.insert(
            "",
            "end",
            values=(
                row[0],
                fullname,
                row[3],
                row[4],
                row[5]
            )
        )

    conn.close()