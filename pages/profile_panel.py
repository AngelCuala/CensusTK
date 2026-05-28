import tkinter as tk
from tkinter import messagebox
from db import connect_db


class ProfilePanel:

    def __init__(self, parent, user_data, navbar_height=0):
        self.parent = parent
        self.user_data = user_data
        self.navbar_height = navbar_height

        self.width = 520
        self.is_open = False

        self.panel = tk.Frame(
            parent, bg="#ffffff", width=self.width, bd=0
        )
        self.panel.config(highlightbackground="#dfe6e9", highlightthickness=1)
        self.panel.pack_propagate(False)  # prevent content from resizing the panel
        # Start hidden off the left edge
        self.panel.place(x=-self.width, y=0)

        self.container = tk.Frame(self.panel, bg="#ffffff")
        self.container.place(relx=0, rely=0, relwidth=1, relheight=1)  # fill panel completely

        self.parent.after(10, self.update_height)
        self.parent.bind("<Configure>", lambda e: self.update_height())

        self._show_profile_view()

    # =================================================
    # HEIGHT — full screen top to bottom
    # =================================================
    def update_height(self):
        height = self.parent.winfo_height()
        self.panel.config(height=height)
        if self.is_open:
            self.panel.place(x=0, y=0)

    def _clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # =================================================
    # PROFILE VIEW
    # =================================================
    def _show_profile_view(self):
        self._clear()

        # ── Header ───────────────────────────────────
        top = tk.Frame(self.container, bg="#4353BD", height=280)
        top.pack(fill="x")
        top.pack_propagate(False)

        # Close X top-right
        close_x = tk.Label(
            top, text="✕", bg="#4353BD", fg="#a5b4fc",
            font=("Segoe UI", 14), cursor="hand2", padx=18, pady=14
        )
        close_x.pack(anchor="ne")
        close_x.bind("<Button-1>", lambda e: self.toggle())
        close_x.bind("<Enter>", lambda e: close_x.config(fg="white"))
        close_x.bind("<Leave>", lambda e: close_x.config(fg="#a5b4fc"))

        # Avatar with initials
        first = self.user_data.get("First_Name", "") or "?"
        last  = self.user_data.get("Last_Name", "")
        initials = first[0].upper()
        if last:
            initials += last[0].upper()

        av = tk.Canvas(top, width=110, height=110, bg="#4353BD", highlightthickness=0)
        av.pack(pady=(0, 14))
        av.create_oval(5, 5, 105, 105, fill="#eef2ff", outline="#818cf8", width=2)
        av.create_text(55, 55, text=initials, font=("Segoe UI", 30, "bold"), fill="#4353BD")

        full_name = f"{first} {last}".strip() or "Unknown User"
        user_type = self.user_data.get("User_type", "User")

        tk.Label(top, text=full_name, bg="#4353BD", fg="white",
                 font=("Segoe UI", 20, "bold")).pack()
        tk.Label(top, text=user_type, bg="#4353BD", fg="#a5b4fc",
                 font=("Segoe UI", 13)).pack(pady=(4, 0))

        # ── Body ─────────────────────────────────────
        body = tk.Frame(self.container, bg="#ffffff")
        body.pack(fill="both", expand=True, padx=32, pady=28)

        tk.Label(body, text="Account Details", bg="#ffffff", fg="#94a3b8",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Frame(body, bg="#e5e7eb", height=1).pack(fill="x", pady=(6, 16))

        def info_row(icon, label, value):
            row = tk.Frame(body, bg="#f8fafc",
                           highlightbackground="#e5e7eb", highlightthickness=1)
            row.pack(fill="x", pady=5)

            icon_box = tk.Frame(row, bg="#eef2ff", width=44, height=44)
            icon_box.pack(side="left", padx=(14, 0), pady=12)
            icon_box.pack_propagate(False)
            tk.Label(icon_box, text=icon, bg="#eef2ff",
                     font=("Segoe UI", 16)).place(relx=0.5, rely=0.5, anchor="center")

            text_box = tk.Frame(row, bg="#f8fafc")
            text_box.pack(side="left", padx=14, pady=10)

            tk.Label(text_box, text=label, bg="#f8fafc", fg="#94a3b8",
                     font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(text_box, text=str(value), bg="#f8fafc", fg="#111827",
                     font=("Segoe UI Semibold", 13)).pack(anchor="w")

        uid = (self.user_data.get("User_ID")
               or self.user_data.get("user_id")
               or self.user_data.get("id", "N/A"))

        info_row("🪪", "User ID",   uid)
        info_row("👤", "Full Name", full_name)
        info_row("🔑", "Role",      user_type)

        email = self.user_data.get("Email") or self.user_data.get("email", "")
        if email:
            info_row("✉️", "Email", email)

        username = self.user_data.get("Username", "")
        if username:
            info_row("🏷️", "Username", username)

        # ── Settings ─────────────────────────────────
        tk.Frame(body, bg="#ffffff").pack(expand=True, fill="both")

        tk.Label(body, text="Settings", bg="#ffffff", fg="#94a3b8",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))

        def settings_btn(text, command):
            btn = tk.Label(
                body, text=text, bg="#f1f5f9", fg="#111827",
                font=("Segoe UI", 12), cursor="hand2",
                anchor="w", padx=16, pady=12,
                highlightbackground="#e2e8f0", highlightthickness=1
            )
            btn.pack(fill="x", pady=4)
            btn.bind("<Button-1>", lambda e: command())
            btn.bind("<Enter>", lambda e: btn.config(bg="#e2e8f0"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#f1f5f9"))

        settings_btn("✏️   Edit Profile",    self._show_edit_profile)
        settings_btn("🔒   Change Password", self._show_change_password)

        close_btn = tk.Label(
            body, text="← Close Panel", bg="#ffffff", fg="#4353BD",
            font=("Segoe UI Semibold", 13), cursor="hand2", pady=22
        )
        close_btn.pack()
        close_btn.bind("<Button-1>", lambda e: self.toggle())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg="#5b6ee1"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg="#4353BD"))

        tk.Label(body, text="Census Management System", bg="#ffffff", fg="#cbd5e1",
                 font=("Segoe UI", 9)).pack(pady=(0, 6))

    # =================================================
    # EDIT PROFILE VIEW
    # =================================================
    def _show_edit_profile(self):
        self._clear()

        # Outer frame fills the full container height
        outer = tk.Frame(self.container, bg="#ffffff")
        outer.place(relx=0, rely=0, relwidth=1, relheight=1)

        top = tk.Frame(outer, bg="#4353BD", height=70)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="✏️  Edit Profile", bg="#4353BD", fg="white",
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=24, pady=18)

        # Body fills remaining space
        body = tk.Frame(outer, bg="#ffffff")
        body.pack(fill="both", expand=True, padx=32, pady=28)

        def labeled_entry(label, default=""):
            tk.Label(body, text=label, bg="#ffffff", fg="#374151",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(14, 2))
            e = tk.Entry(body, font=("Segoe UI", 12), bg="#f8fafc",
                         relief="flat",
                         highlightbackground="#e5e7eb", highlightthickness=1)
            e.insert(0, default)
            e.pack(fill="x", ipady=10)
            return e

        fname_entry = labeled_entry("First Name",  self.user_data.get("First_Name", ""))
        lname_entry = labeled_entry("Last Name",   self.user_data.get("Last_Name", ""))
        uname_entry = labeled_entry("Username",    self.user_data.get("Username", ""))

        tk.Label(body, text="⚠️ Role and status cannot be changed.",
                 bg="#ffffff", fg="#f59e0b",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(14, 0))

        error_lbl = tk.Label(body, text="", bg="#ffffff", fg="#ef4444",
                             font=("Segoe UI", 10))
        error_lbl.pack(anchor="w", pady=(4, 0))

        def save():
            new_fname = fname_entry.get().strip()
            new_lname = lname_entry.get().strip()
            new_uname = uname_entry.get().strip()

            if not new_fname or not new_lname or not new_uname:
                error_lbl.config(text="All fields are required.")
                return

            uid = (self.user_data.get("User_ID")
                   or self.user_data.get("user_id")
                   or self.user_data.get("id"))
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT User_ID FROM accounts
                    WHERE Username = %s AND User_ID != %s
                """, (new_uname, uid))
                if cursor.fetchone():
                    error_lbl.config(text="Username already taken.")
                    conn.close()
                    return

                cursor.execute("""
                    UPDATE accounts
                    SET First_Name = %s, Last_Name = %s, Username = %s
                    WHERE User_ID = %s
                """, (new_fname, new_lname, new_uname, uid))
                conn.commit()
                conn.close()

                self.user_data["First_Name"] = new_fname
                self.user_data["Last_Name"]  = new_lname
                self.user_data["Username"]   = new_uname

                messagebox.showinfo("Saved", "Profile updated successfully.")
                self._show_profile_view()

            except Exception as e:
                error_lbl.config(text=f"Error: {e}")

        # Spacer pushes buttons to the bottom
        tk.Frame(body, bg="#ffffff").pack(expand=True, fill="both")

        save_btn = tk.Label(
            body, text="Save Changes", bg="#4353BD", fg="white",
            font=("Segoe UI", 11, "bold"), cursor="hand2", pady=13
        )
        save_btn.pack(fill="x", pady=(0, 8))
        save_btn.bind("<Button-1>", lambda e: save())
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#3243a8"))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg="#4353BD"))

        back_btn = tk.Label(
            body, text="← Back", bg="#f1f5f9", fg="#374151",
            font=("Segoe UI", 11), cursor="hand2", pady=11
        )
        back_btn.pack(fill="x")
        back_btn.bind("<Button-1>", lambda e: self._show_profile_view())
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#e2e8f0"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#f1f5f9"))

    # =================================================
    # CHANGE PASSWORD VIEW
    # =================================================
    def _show_change_password(self):
        self._clear()

        # Outer frame fills the full container height
        outer = tk.Frame(self.container, bg="#ffffff")
        outer.place(relx=0, rely=0, relwidth=1, relheight=1)

        top = tk.Frame(outer, bg="#4353BD", height=70)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="🔒  Change Password", bg="#4353BD", fg="white",
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=24, pady=18)

        # Body fills remaining space
        body = tk.Frame(outer, bg="#ffffff")
        body.pack(fill="both", expand=True, padx=32, pady=28)

        def pw_entry(label):
            tk.Label(body, text=label, bg="#ffffff", fg="#374151",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(14, 2))
            e = tk.Entry(body, font=("Segoe UI", 12), bg="#f8fafc",
                         show="•", relief="flat",
                         highlightbackground="#e5e7eb", highlightthickness=1)
            e.pack(fill="x", ipady=10)
            return e

        current_entry = pw_entry("Current Password")
        new_entry     = pw_entry("New Password")
        confirm_entry = pw_entry("Confirm New Password")

        tk.Label(body, text="Password must be at least 8 characters.",
                 bg="#ffffff", fg="#94a3b8",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 0))

        error_lbl = tk.Label(body, text="", bg="#ffffff", fg="#ef4444",
                             font=("Segoe UI", 10))
        error_lbl.pack(anchor="w", pady=(4, 0))

        def save():
            current = current_entry.get()
            new_pw  = new_entry.get()
            confirm = confirm_entry.get()

            if not current or not new_pw or not confirm:
                error_lbl.config(text="All fields are required.")
                return
            if len(new_pw) < 8:
                error_lbl.config(text="Password must be at least 8 characters.")
                return
            if new_pw != confirm:
                error_lbl.config(text="New passwords do not match.")
                return

            uid = (self.user_data.get("User_ID")
                   or self.user_data.get("user_id")
                   or self.user_data.get("id"))
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT User_ID FROM accounts
                    WHERE User_ID = %s AND Password = %s
                """, (uid, current))
                if not cursor.fetchone():
                    error_lbl.config(text="Current password is incorrect.")
                    conn.close()
                    return

                cursor.execute("""
                    UPDATE accounts SET Password = %s WHERE User_ID = %s
                """, (new_pw, uid))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Password changed successfully.")
                self._show_profile_view()

            except Exception as e:
                error_lbl.config(text=f"Error: {e}")

        # Spacer pushes buttons to the bottom
        tk.Frame(body, bg="#ffffff").pack(expand=True, fill="both")

        change_btn = tk.Label(
            body, text="Change Password", bg="#4353BD", fg="white",
            font=("Segoe UI", 11, "bold"), cursor="hand2", pady=13
        )
        change_btn.pack(fill="x", pady=(0, 8))
        change_btn.bind("<Button-1>", lambda e: save())
        change_btn.bind("<Enter>", lambda e: change_btn.config(bg="#3243a8"))
        change_btn.bind("<Leave>", lambda e: change_btn.config(bg="#4353BD"))

        back_btn = tk.Label(
            body, text="← Back", bg="#f1f5f9", fg="#374151",
            font=("Segoe UI", 11), cursor="hand2", pady=11
        )
        back_btn.pack(fill="x")
        back_btn.bind("<Button-1>", lambda e: self._show_profile_view())
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#e2e8f0"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#f1f5f9"))

    # =================================================
    # ANIMATION — slides in/out from LEFT, full height
    # =================================================
    def open(self):
        self.is_open = True
        self.panel.lift()
        self.update_height()
        self._animate(-self.width, 0, step=35)

    def close(self):
        self.is_open = False
        self._animate(0, -self.width, step=-35)

    def _animate(self, x, target, step):
        self.panel.place(x=x, y=0)
        if (step > 0 and x < target) or (step < 0 and x > target):
            next_x = min(x + step, target) if step > 0 else max(x + step, target)
            self.parent.after(6, lambda: self._animate(next_x, target, step))

    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()