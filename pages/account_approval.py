import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db
import random
import string
import smtplib
import re
from email.mime.text import MIMEText


SENDER_EMAIL    = "censusportalluisiana@gmail.com"
SENDER_PASSWORD = "lxzk kqug gity whxe"


# =====================================================
# GENERATE PASSWORD
# =====================================================
def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$"
    return ''.join(random.choice(chars) for _ in range(length))


# =====================================================
# VALIDATE EMAIL FORMAT
# =====================================================
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# =====================================================
# SEND EMAIL
# =====================================================
def send_credentials_email(receiver_email, full_name, username, password):
    subject = "Your Census Management System Account"
    body = f"""Hello {full_name},

Your employee account has been created by the administrator.

You can now log in using the credentials below:

----------------------------------------
Username : {username}
Password : {password}
----------------------------------------

Please log in and change your password as soon as possible.

Thank you.
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, ""
    except smtplib.SMTPRecipientsRefused:
        return False, "The email address was rejected by Gmail. It may not exist."
    except Exception as e:
        return False, str(e)


# =====================================================
# MAIN PAGE
# =====================================================
def create_account_approval(parent):

    frame = tk.Frame(parent, bg="#f0f2f8")

    # ── Header Banner ────────────────────────────────
    banner = tk.Frame(frame, bg="#1a2057", height=100)
    banner.pack(fill="x", padx=24, pady=(24, 0))
    banner.pack_propagate(False)

    banner_inner = tk.Frame(banner, bg="#1a2057")
    banner_inner.pack(fill="both", expand=True, padx=28)

    left = tk.Frame(banner_inner, bg="#1a2057")
    left.pack(side="left", fill="both", expand=True)

    tk.Label(
        left, text="Employee Accounts",
        font=("Segoe UI", 22, "bold"),
        bg="#1a2057", fg="#ffffff"
    ).pack(anchor="w", pady=(20, 2))

    tk.Label(
        left, text="Create and manage employee accounts",
        font=("Segoe UI", 11),
        bg="#1a2057", fg="#8b9fd4"
    ).pack(anchor="w")

    right = tk.Frame(banner_inner, bg="#1a2057")
    right.pack(side="right", fill="y", pady=28)

    pill = tk.Label(
        right, text="  👤  Accounts Manager  ",
        font=("Segoe UI", 10),
        bg="#2d3b80", fg="#a5b4fc",
        padx=10, pady=6
    )
    pill.pack(side="right")

    # ── Section label ────────────────────────────────
    tk.Label(
        frame, text="EMPLOYEE LIST",
        font=("Segoe UI", 9, "bold"),
        bg="#f0f2f8", fg="#9ca3af"
    ).pack(anchor="w", padx=24, pady=(16, 4))

    # ── Main container ───────────────────────────────
    container = tk.Frame(
        frame, bg="white",
        highlightbackground="#e8eaf0",
        highlightthickness=1
    )
    container.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    # ── Toolbar ──────────────────────────────────────
    toolbar = tk.Frame(container, bg="white")
    toolbar.pack(fill="x", padx=16, pady=14)

    def style_btn(btn, bg, hover):
        btn.configure(
            bg=bg, fg="white", relief="flat", bd=0,
            padx=16, pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    create_btn  = tk.Button(toolbar, text="＋  Create Account", command=lambda: open_create_window())
    refresh_btn = tk.Button(toolbar, text="⟳  Refresh",        command=lambda: load_data())

    style_btn(create_btn,  "#4353BD", "#3742fa")
    style_btn(refresh_btn, "#374151", "#4b5563")

    create_btn.pack(side="left", padx=(0, 8))
    refresh_btn.pack(side="left")

    tk.Frame(container, bg="#f0f2f8", height=1).pack(fill="x", padx=16)

    # ── Treeview styling ─────────────────────────────
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Accounts.Treeview",
        background="#ffffff",
        foreground="#111827",
        rowheight=40,
        fieldbackground="#ffffff",
        borderwidth=0,
        font=("Segoe UI", 11)
    )
    style.configure(
        "Accounts.Treeview.Heading",
        background="#f8fafc",
        foreground="#6b7280",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(10, 10)
    )
    style.map(
        "Accounts.Treeview",
        background=[("selected", "#eef0fb")],
        foreground=[("selected", "#1a2057")]
    )
    style.map(
        "Accounts.Treeview.Heading",
        background=[("active", "#f1f5f9")]
    )

    columns = ("ID", "Name", "Username", "Email", "Contact", "Barangay")
    tree = ttk.Treeview(
        container, columns=columns,
        show="headings", height=16,
        style="Accounts.Treeview"
    )

    col_widths = {
        "ID": 60, "Name": 190, "Username": 150,
        "Email": 210, "Contact": 130, "Barangay": 160
    }
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=col_widths.get(col, 130), anchor="w")

    tree.tag_configure("odd",  background="#ffffff")
    tree.tag_configure("even", background="#f8fafc")

    tree.pack(fill="both", expand=True, padx=16, pady=(0, 8))

    # ── Bottom action bar ─────────────────────────────
    action_bar = tk.Frame(container, bg="#fef2f2",
                          highlightbackground="#fecaca", highlightthickness=1)
    action_bar.pack(fill="x", padx=16, pady=(0, 14))

    tk.Label(
        action_bar,
        text="⚠  Select a row then click Delete to remove the account.",
        font=("Segoe UI", 9),
        bg="#fef2f2", fg="#b91c1c"
    ).pack(side="left", padx=14, pady=8)

    delete_btn = tk.Button(action_bar, text="🗑  Delete Account")
    style_btn(delete_btn, "#dc2626", "#b91c1c")
    delete_btn.pack(side="right", padx=10, pady=6)

    # =====================================================
    # LOAD DATA
    # =====================================================
    def load_data():
        tree.delete(*tree.get_children())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT User_ID, First_Name, Last_Name, Username,
                   Email, Contact_Number, Barangay
            FROM accounts
            WHERE User_type = 'Employee'
            ORDER BY User_ID DESC
        """)
        for idx, row in enumerate(cursor.fetchall()):
            uid, fname, lname, uname, email, contact, brgy = row
            tag = "even" if idx % 2 == 0 else "odd"
            tree.insert("", "end", iid=str(uid), tags=(tag,), values=(
                uid, f"{fname} {lname}", uname,
                email or "—", contact or "—", brgy or "—"
            ))
        conn.close()

    # =====================================================
    # DELETE ACCOUNT
    # =====================================================
    def delete_account():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an account.")
            return
        uid = selected[0]
        if not messagebox.askyesno("Confirm", "Permanently delete this account?"):
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM accounts WHERE User_ID = %s", (uid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Account deleted.")
            load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    delete_btn.config(command=delete_account)

    # =====================================================
    # CREATE ACCOUNT WINDOW  ──  REDESIGNED
    # =====================================================
    def open_create_window():

        # ── Palette ──────────────────────────────────
        C = {
            "bg":           "#F4F6FB",
            "white":        "#FFFFFF",
            "navy":         "#1a2057",
            "navy_mid":     "#2d3b80",
            "accent":       "#4353BD",
            "accent_hover": "#3742fa",
            "border":       "#DDE1EE",
            "border_focus": "#4353BD",
            "text_dark":    "#111827",
            "text_mid":     "#374151",
            "text_muted":   "#9CA3AF",
            "success":      "#16a34a",
            "success_bg":   "#F0FDF4",
            "error":        "#dc2626",
            "error_bg":     "#FEF2F2",
            "warn_bg":      "#FFFBEB",
            "warn_text":    "#92400e",
            "section_bg":   "#F8FAFC",
            "pill_bg":      "#EEF0FB",
            "pill_fg":      "#4353BD",
        }

        win = tk.Toplevel(frame)
        win.title("Create Employee Account")
        win.geometry("560x740")
        win.config(bg=C["bg"])
        win.resizable(False, False)
        win.grab_set()

        # ── TOP HEADER ───────────────────────────────
        header = tk.Frame(win, bg=C["navy"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Left accent stripe
        tk.Frame(header, bg=C["accent"], width=5).pack(side="left", fill="y")

        h_inner = tk.Frame(header, bg=C["navy"])
        h_inner.pack(side="left", fill="both", expand=True, padx=20)

        tk.Label(
            h_inner, text="Create Employee Account",
            font=("Segoe UI", 15, "bold"),
            bg=C["navy"], fg="#FFFFFF"
        ).pack(anchor="w", pady=(14, 0))

        tk.Label(
            h_inner, text="Fill in all fields — credentials will be emailed automatically",
            font=("Segoe UI", 9),
            bg=C["navy"], fg="#8b9fd4"
        ).pack(anchor="w")

        # Step badge
        badge = tk.Label(
            header, text=" STEP 1 OF 1 ",
            font=("Segoe UI", 8, "bold"),
            bg=C["navy_mid"], fg="#a5b4fc",
            padx=8, pady=4
        )
        badge.pack(side="right", padx=18, pady=26)

        # ── SCROLLABLE CANVAS ────────────────────────
        canvas = tk.Canvas(win, bg=C["bg"], highlightthickness=0)
        vbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        outer = tk.Frame(canvas, bg=C["bg"])
        win_id = canvas.create_window((0, 0), window=outer, anchor="nw", width=556)
        outer.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # ── HELPER: section card ─────────────────────
        def make_card(parent, title, subtitle=None):
            """Returns the inner frame of a titled card."""
            card = tk.Frame(
                parent, bg=C["white"],
                highlightbackground=C["border"],
                highlightthickness=1
            )
            card.pack(fill="x", padx=18, pady=(14, 0))

            # Card header row
            card_header = tk.Frame(card, bg=C["section_bg"],
                                   highlightbackground=C["border"],
                                   highlightthickness=0)
            card_header.pack(fill="x")
            tk.Frame(card_header, bg=C["accent"], width=3).pack(side="left", fill="y")
            ch_text = tk.Frame(card_header, bg=C["section_bg"])
            ch_text.pack(side="left", padx=14, pady=10)
            tk.Label(
                ch_text, text=title.upper(),
                font=("Segoe UI", 8, "bold"),
                bg=C["section_bg"], fg=C["text_muted"]
            ).pack(anchor="w")
            if subtitle:
                tk.Label(
                    ch_text, text=subtitle,
                    font=("Segoe UI", 9),
                    bg=C["section_bg"], fg=C["text_mid"]
                ).pack(anchor="w")

            # Thin divider
            tk.Frame(card, bg=C["border"], height=1).pack(fill="x")

            body = tk.Frame(card, bg=C["white"])
            body.pack(fill="x", padx=20, pady=14)
            return body

        # ── HELPER: single labelled entry ────────────
        fields = {}
        active_entries = {}   # track focus colors

        def make_entry(parent, label, key, hint=None, show=None, row=None, col=None, colspan=1):
            """
            Renders a label + styled entry. If row/col given, uses grid, else pack.
            Returns the Entry widget.
            """
            container = tk.Frame(parent, bg=C["white"])
            if row is not None:
                container.grid(row=row, column=col, columnspan=colspan,
                               sticky="ew", padx=(0, 12 if col == 0 else 0), pady=(0, 14))
            else:
                container.pack(fill="x", pady=(0, 14))

            tk.Label(
                container, text=label,
                font=("Segoe UI", 10, "bold"),
                bg=C["white"], fg=C["text_mid"]
            ).pack(anchor="w")

            if hint:
                tk.Label(
                    container, text=hint,
                    font=("Segoe UI", 8),
                    bg=C["white"], fg=C["text_muted"]
                ).pack(anchor="w", pady=(1, 3))

            entry_frame = tk.Frame(
                container, bg=C["white"],
                highlightbackground=C["border"],
                highlightthickness=1
            )
            entry_frame.pack(fill="x", pady=(3, 0))

            e = tk.Entry(
                entry_frame,
                font=("Segoe UI", 11),
                relief="flat", bd=0,
                bg=C["white"],
                fg=C["text_dark"],
                insertbackground=C["accent"]
            )
            if show:
                e.config(show=show)
            e.pack(fill="x", padx=10, ipady=9)

            # Focus ring
            def on_focus_in(_):
                entry_frame.config(highlightbackground=C["border_focus"], highlightthickness=2)
            def on_focus_out(_):
                entry_frame.config(highlightbackground=C["border"], highlightthickness=1)
            e.bind("<FocusIn>",  on_focus_in)
            e.bind("<FocusOut>", on_focus_out)

            fields[key] = e
            active_entries[key] = entry_frame
            return e, container

        # ── HELPER: combobox ──────────────────────────
        def make_combo(parent, label, key, values, hint=None):
            container = tk.Frame(parent, bg=C["white"])
            container.pack(fill="x", pady=(0, 14))

            tk.Label(
                container, text=label,
                font=("Segoe UI", 10, "bold"),
                bg=C["white"], fg=C["text_mid"]
            ).pack(anchor="w")
            if hint:
                tk.Label(
                    container, text=hint,
                    font=("Segoe UI", 8),
                    bg=C["white"], fg=C["text_muted"]
                ).pack(anchor="w", pady=(1, 3))

            combo_frame = tk.Frame(
                container, bg=C["white"],
                highlightbackground=C["border"],
                highlightthickness=1
            )
            combo_frame.pack(fill="x", pady=(3, 0))

            style = ttk.Style()
            style.configure("Create.TCombobox",
                            fieldbackground=C["white"],
                            background=C["white"],
                            foreground=C["text_dark"],
                            arrowcolor=C["accent"],
                            padding=(8, 8))

            var = tk.StringVar(value=f"Select {label}")
            cb = ttk.Combobox(
                combo_frame, textvariable=var,
                values=values, state="readonly",
                font=("Segoe UI", 11),
                style="Create.TCombobox"
            )
            cb.pack(fill="x", ipady=5)

            fields[key] = var
            return cb

        # ══════════════════════════════════════════════
        # CARD 1 — Personal Info
        # ══════════════════════════════════════════════
        body1 = make_card(outer, "Personal Information", "Employee's full name")

        name_grid = tk.Frame(body1, bg=C["white"])
        name_grid.pack(fill="x")
        name_grid.columnconfigure(0, weight=1)
        name_grid.columnconfigure(1, weight=1)

        make_entry(name_grid, "First Name", "first_name", row=0, col=0)
        make_entry(name_grid, "Last Name",  "last_name",  row=0, col=1)

        # ══════════════════════════════════════════════
        # CARD 2 — Login Credentials
        # ══════════════════════════════════════════════
        body2 = make_card(outer, "Login Credentials",
                          "Username is set by you; password is auto-generated")

        make_entry(body2, "Username", "username",
                   hint="Must be unique — this is what the employee types to log in")

        # Email row + live validator
        email_entry, email_container = make_entry(
            body2, "Email Address", "email",
            hint="A real inbox — login credentials will be delivered here"
        )

        email_status = tk.Label(
            email_container, text="", bg=C["white"], font=("Segoe UI", 9)
        )
        email_status.pack(anchor="w", pady=(3, 0))

        def on_email_change(*_):
            val = fields["email"].get().strip()
            if not val:
                email_status.config(text="", fg=C["text_muted"])
                active_entries["email"].config(highlightbackground=C["border"])
            elif is_valid_email(val):
                email_status.config(text="✔  Valid email format", fg=C["success"])
                active_entries["email"].config(highlightbackground=C["success"])
            else:
                email_status.config(text="✘  Invalid email format", fg=C["error"])
                active_entries["email"].config(highlightbackground=C["error"])

        fields["email"].bind("<KeyRelease>", on_email_change)

        # Password preview (auto-generated notice)
        pw_notice = tk.Frame(body2, bg=C["warn_bg"],
                             highlightbackground="#FDE68A", highlightthickness=1)
        pw_notice.pack(fill="x", pady=(4, 6))
        tk.Label(
            pw_notice,
            text="🔐  A secure password will be auto-generated and sent to the employee's email.",
            font=("Segoe UI", 9),
            bg=C["warn_bg"], fg=C["warn_text"],
            wraplength=470, justify="left"
        ).pack(anchor="w", padx=12, pady=8)

        # ══════════════════════════════════════════════
        # CARD 3 — Contact & Location
        # ══════════════════════════════════════════════
        body3 = make_card(outer, "Contact & Location", "Where to reach the employee")

        make_entry(body3, "Contact Number", "contact",
                   hint="e.g. 09XX-XXX-XXXX")
        make_entry(body3, "Street / Address", "street")

        barangay_list = [
            "Barangay Zone I", "Barangay Zone II", "Barangay Zone III",
            "Barangay Zone IV", "Barangay Zone V", "Barangay Zone VI",
            "Barangay Zone VII", "Barangay Zone VIII",
            "De La Paz", "San Antonio", "San Buenaventura", "San Diego",
            "San Isidro", "San Jose", "San Juan", "San Luis",
            "San Pablo", "San Pedro", "San Rafael", "San Roque",
            "San Salvador", "Santo Domingo", "Santo Tomas"
        ]
        make_combo(body3, "Barangay", "barangay", barangay_list)

        # ══════════════════════════════════════════════
        # SUBMIT BUTTON
        # ══════════════════════════════════════════════
        btn_frame = tk.Frame(outer, bg=C["bg"])
        btn_frame.pack(fill="x", padx=18, pady=(18, 28))

        # Cancel
        cancel_btn = tk.Label(
            btn_frame, text="Cancel",
            font=("Segoe UI", 10),
            bg=C["bg"], fg=C["text_mid"],
            cursor="hand2", padx=16, pady=11
        )
        cancel_btn.pack(side="left")
        cancel_btn.bind("<Button-1>", lambda e: win.destroy())
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(fg=C["error"]))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(fg=C["text_mid"]))

        # Submit
        submit_btn = tk.Label(
            btn_frame,
            text="  ✓   Create Account & Send Credentials  ",
            font=("Segoe UI", 11, "bold"),
            bg=C["accent"], fg="#FFFFFF",
            cursor="hand2", pady=12,
            anchor="center"
        )
        submit_btn.pack(side="right", fill="x", expand=True)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=C["accent_hover"]))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=C["accent"]))

        # ── Submit logic ──────────────────────────────
        def submit(_=None):
            first    = fields["first_name"].get().strip()
            last     = fields["last_name"].get().strip()
            username = fields["username"].get().strip()
            email    = fields["email"].get().strip()
            contact  = fields["contact"].get().strip()
            street   = fields["street"].get().strip()
            barangay = fields["barangay"].get()

            # Highlight empty fields
            required = {
                "first_name": first, "last_name": last,
                "username": username, "email": email,
                "contact": contact, "street": street,
            }
            any_empty = False
            for k, v in required.items():
                if not v:
                    active_entries[k].config(highlightbackground=C["error"], highlightthickness=2)
                    any_empty = True
                else:
                    active_entries[k].config(highlightbackground=C["border"], highlightthickness=1)

            if any_empty or "Select" in barangay:
                messagebox.showerror("Incomplete Form", "Please fill in all highlighted fields.")
                return

            if not is_valid_email(email):
                messagebox.showerror(
                    "Invalid Email",
                    f'"{email}" is not a valid email address.\n\nPlease enter a real email.'
                )
                return

            if not messagebox.askyesno(
                "Confirm Account Creation",
                f"Create account for {first} {last}?\n\n"
                f"Username : {username}\n"
                f"Email    : {email}\n\n"
                f"A temporary password will be generated and emailed to the address above."
            ):
                return

            password = generate_password()

            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("SELECT 1 FROM accounts WHERE Username = %s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Username Taken", "That username is already in use. Please choose another.")
                    conn.close()
                    return

                cursor.execute("SELECT 1 FROM accounts WHERE Email = %s", (email,))
                if cursor.fetchone():
                    messagebox.showerror("Email Exists", "An account with this email already exists.")
                    conn.close()
                    return

                cursor.execute("""
                    INSERT INTO accounts (
                        First_Name, Last_Name, Username, Password,
                        Email, Contact_Number, Street_Name, Barangay, User_type
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (first, last, username, password,
                      email, contact, street, barangay, "Employee"))

                conn.commit()
                conn.close()

            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                return

            full_name = f"{first} {last}"
            sent, err = send_credentials_email(email, full_name, username, password)

            if sent:
                messagebox.showinfo(
                    "Account Created ✓",
                    f"Account created successfully!\n\n"
                    f"Login credentials have been sent to:\n{email}"
                )
            else:
                messagebox.showwarning(
                    "Account Created — Email Failed",
                    f"Account was created but the email could not be delivered.\n\n"
                    f"Reason: {err}\n\n"
                    f"Please share the username manually:\n"
                    f"Username : {username}\n\n"
                    f"The employee can use 'Forgot Password' to recover access."
                )

            win.destroy()
            load_data()

        submit_btn.bind("<Button-1>", submit)

    load_data()

    return frame