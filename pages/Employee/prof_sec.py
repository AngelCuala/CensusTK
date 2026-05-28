import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db import connect_db


class ProfilePanel:

    def __init__(self, parent, user_data, navbar_height=0):
        self.parent = parent
        self.user_data = user_data
        self.navbar_height = navbar_height

        self.width = 380
        self.is_open = False

        self.panel = ctk.CTkFrame(
            parent,
            fg_color="white",
            width=self.width,
            corner_radius=0,
            border_width=1,
            border_color="#e5e7eb"
        )
        self.panel.place(x=9999, y=self.navbar_height)

        self.build_ui()
        self.parent.after(10, self.update_height)
        self.parent.bind("<Configure>", lambda e: self.update_height())

    # =================================================
    # UPDATE HEIGHT + POSITION
    # =================================================
    def update_height(self):
        height = self.parent.winfo_height() - self.navbar_height
        self.panel.configure(height=height)
        if self.is_open:
            self.panel.place(x=self._right_edge(), y=self.navbar_height)

    def _right_edge(self):
        return self.parent.winfo_width() - self.width

    # =================================================
    # BUILD UI
    # =================================================
    def build_ui(self):

        self.container = ctk.CTkFrame(self.panel, fg_color="white")
        self.container.pack(fill="both", expand=True)

        self._show_profile_view()

    # =================================================
    # PROFILE VIEW (main panel)
    # =================================================
    def _show_profile_view(self):

        for w in self.container.winfo_children():
            w.destroy()

        # ── Header ───────────────────────────────────
        header = ctk.CTkFrame(self.container, fg_color="#4353BD", height=260, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        close_x = ctk.CTkLabel(
            header, text="✕",
            font=ctk.CTkFont(size=16),
            text_color="#a5b4fc", cursor="hand2"
        )
        close_x.pack(anchor="ne", padx=16, pady=(12, 0))
        close_x.bind("<Button-1>", lambda e: self.toggle())

        first = self.user_data.get("First_Name", "") or self.user_data.get("name", "?")
        last  = self.user_data.get("Last_Name", "")
        initials = (first[0] if first else "?").upper()
        if last:
            initials += last[0].upper()

        av_frame = ctk.CTkFrame(header, width=96, height=96,
                                fg_color="#eef2ff", corner_radius=48)
        av_frame.pack(pady=(8, 12))
        av_frame.pack_propagate(False)

        ctk.CTkLabel(
            av_frame, text=initials,
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#4353BD"
        ).place(relx=0.5, rely=0.5, anchor="center")

        full_name = f"{first} {last}".strip() or "Unknown User"
        self._full_name = full_name

        ctk.CTkLabel(
            header, text=full_name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack()

        user_type = self.user_data.get("User_type", "Employee")
        ctk.CTkLabel(
            header, text=user_type,
            font=ctk.CTkFont(size=12),
            text_color="#a5b4fc"
        ).pack(pady=(4, 0))

        # ── Body ─────────────────────────────────────
        body = ctk.CTkFrame(self.container, fg_color="white")
        body.pack(fill="both", expand=True, padx=22, pady=22)

        ctk.CTkLabel(
            body, text="Account Details",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#94a3b8"
        ).pack(anchor="w")

        ctk.CTkFrame(body, fg_color="#e5e7eb", height=1).pack(fill="x", pady=(8, 14))

        def info_row(icon, label, value):
            row = ctk.CTkFrame(body, fg_color="#f8fafc", corner_radius=12,
                               border_width=1, border_color="#e5e7eb")
            row.pack(fill="x", pady=5)

            icon_box = ctk.CTkFrame(row, width=42, height=42,
                                    fg_color="#eef2ff", corner_radius=10)
            icon_box.pack(side="left", padx=(14, 0), pady=12)
            icon_box.pack_propagate(False)
            ctk.CTkLabel(icon_box, text=icon,
                         font=ctk.CTkFont(size=18)).place(relx=0.5, rely=0.5, anchor="center")

            text_box = ctk.CTkFrame(row, fg_color="transparent")
            text_box.pack(side="left", padx=12, pady=10)

            ctk.CTkLabel(text_box, text=label,
                         font=ctk.CTkFont(size=10),
                         text_color="#94a3b8").pack(anchor="w")

            ctk.CTkLabel(text_box, text=str(value),
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#111827").pack(anchor="w")

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

        # ── Settings buttons ─────────────────────────
        ctk.CTkFrame(body, fg_color="white").pack(expand=True, fill="both")

        ctk.CTkLabel(
            body, text="Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#94a3b8"
        ).pack(anchor="w", pady=(0, 8))

        ctk.CTkButton(
            body, text="✏️  Edit Profile",
            fg_color="#f1f5f9", hover_color="#e2e8f0",
            text_color="#111827",
            height=40, corner_radius=10,
            font=ctk.CTkFont(size=12),
            anchor="w",
            command=self._show_edit_profile
        ).pack(fill="x", pady=(0, 6))

        ctk.CTkButton(
            body, text="🔒  Change Password",
            fg_color="#f1f5f9", hover_color="#e2e8f0",
            text_color="#111827",
            height=40, corner_radius=10,
            font=ctk.CTkFont(size=12),
            anchor="w",
            command=self._show_change_password
        ).pack(fill="x", pady=(0, 12))

        ctk.CTkButton(
            body, text="← Close Panel",
            fg_color="#4353BD", hover_color="#3243a8",
            height=44,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle
        ).pack(fill="x")

        ctk.CTkLabel(
            body, text="Census Management System",
            font=ctk.CTkFont(size=9),
            text_color="#cbd5e1"
        ).pack(pady=(10, 0))

    # =================================================
    # EDIT PROFILE VIEW
    # =================================================
    def _show_edit_profile(self):

        for w in self.container.winfo_children():
            w.destroy()

        # Header
        header = ctk.CTkFrame(self.container, fg_color="#4353BD", height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="✏️  Edit Profile",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=18)

        body = ctk.CTkFrame(self.container, fg_color="white")
        body.pack(fill="both", expand=True, padx=24, pady=24)

        def labeled_entry(label, default=""):
            ctk.CTkLabel(body, text=label,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="#374151").pack(anchor="w", pady=(12, 2))
            e = ctk.CTkEntry(body, height=40, font=ctk.CTkFont(size=13))
            e.insert(0, default)
            e.pack(fill="x")
            return e

        fname_entry = labeled_entry("First Name",
                                    self.user_data.get("First_Name", ""))
        lname_entry = labeled_entry("Last Name",
                                    self.user_data.get("Last_Name", ""))
        uname_entry = labeled_entry("Username",
                                    self.user_data.get("Username", ""))

        # Status note
        ctk.CTkLabel(
            body,
            text="⚠️ Role and status cannot be changed.",
            font=ctk.CTkFont(size=10),
            text_color="#f59e0b"
        ).pack(anchor="w", pady=(14, 0))

        error_lbl = ctk.CTkLabel(body, text="", text_color="#ef4444",
                                 font=ctk.CTkFont(size=11))
        error_lbl.pack(anchor="w", pady=(4, 0))

        # ── Save ─────────────────────────────────────
        def save():
            new_fname = fname_entry.get().strip()
            new_lname = lname_entry.get().strip()
            new_uname = uname_entry.get().strip()

            if not new_fname or not new_lname or not new_uname:
                error_lbl.configure(text="All fields are required.")
                return

            uid = (self.user_data.get("User_ID")
                   or self.user_data.get("user_id")
                   or self.user_data.get("id"))

            try:
                conn = connect_db()
                cursor = conn.cursor()

                # Check username not taken by someone else
                cursor.execute("""
                    SELECT User_ID FROM accounts
                    WHERE Username = %s AND User_ID != %s
                """, (new_uname, uid))
                if cursor.fetchone():
                    error_lbl.configure(text="Username already taken.")
                    conn.close()
                    return

                cursor.execute("""
                    UPDATE accounts
                    SET First_Name = %s, Last_Name = %s, Username = %s
                    WHERE User_ID = %s
                """, (new_fname, new_lname, new_uname, uid))

                conn.commit()
                conn.close()

                # Update local user_data so panel reflects changes immediately
                self.user_data["First_Name"] = new_fname
                self.user_data["Last_Name"]  = new_lname
                self.user_data["Username"]   = new_uname

                messagebox.showinfo("Saved", "Profile updated successfully.")
                self._show_profile_view()

            except Exception as e:
                error_lbl.configure(text=f"Error: {e}")

        ctk.CTkFrame(body, fg_color="white").pack(expand=True, fill="both")

        ctk.CTkButton(
            body, text="Save Changes",
            fg_color="#4353BD", hover_color="#3243a8",
            height=44, font=ctk.CTkFont(size=12, weight="bold"),
            command=save
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            body, text="← Back",
            fg_color="#f1f5f9", hover_color="#e2e8f0",
            text_color="#374151",
            height=40, font=ctk.CTkFont(size=12),
            command=self._show_profile_view
        ).pack(fill="x")

    # =================================================
    # CHANGE PASSWORD VIEW
    # =================================================
    def _show_change_password(self):

        for w in self.container.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.container, fg_color="#4353BD", height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="🔒  Change Password",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=18)

        body = ctk.CTkFrame(self.container, fg_color="white")
        body.pack(fill="both", expand=True, padx=24, pady=24)

        def pw_entry(label):
            ctk.CTkLabel(body, text=label,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="#374151").pack(anchor="w", pady=(12, 2))
            e = ctk.CTkEntry(body, height=40, show="•",
                             font=ctk.CTkFont(size=13))
            e.pack(fill="x")
            return e

        current_entry = pw_entry("Current Password")
        new_entry     = pw_entry("New Password")
        confirm_entry = pw_entry("Confirm New Password")

        ctk.CTkLabel(
            body,
            text="Password must be at least 8 characters.",
            font=ctk.CTkFont(size=10),
            text_color="#94a3b8"
        ).pack(anchor="w", pady=(6, 0))

        error_lbl = ctk.CTkLabel(body, text="", text_color="#ef4444",
                                 font=ctk.CTkFont(size=11))
        error_lbl.pack(anchor="w", pady=(4, 0))

        # ── Save ─────────────────────────────────────
        def save():
            current = current_entry.get()
            new_pw  = new_entry.get()
            confirm = confirm_entry.get()

            if not current or not new_pw or not confirm:
                error_lbl.configure(text="All fields are required.")
                return

            if len(new_pw) < 8:
                error_lbl.configure(text="Password must be at least 8 characters.")
                return

            if new_pw != confirm:
                error_lbl.configure(text="New passwords do not match.")
                return

            uid = (self.user_data.get("User_ID")
                   or self.user_data.get("user_id")
                   or self.user_data.get("id"))

            try:
                conn = connect_db()
                cursor = conn.cursor()

                # Verify current password
                cursor.execute("""
                    SELECT User_ID FROM accounts
                    WHERE User_ID = %s AND Password = %s
                """, (uid, current))

                if not cursor.fetchone():
                    error_lbl.configure(text="Current password is incorrect.")
                    conn.close()
                    return

                # Update to new password
                cursor.execute("""
                    UPDATE accounts SET Password = %s WHERE User_ID = %s
                """, (new_pw, uid))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Password changed successfully.")
                self._show_profile_view()

            except Exception as e:
                error_lbl.configure(text=f"Error: {e}")

        ctk.CTkFrame(body, fg_color="white").pack(expand=True, fill="both")

        ctk.CTkButton(
            body, text="Change Password",
            fg_color="#4353BD", hover_color="#3243a8",
            height=44, font=ctk.CTkFont(size=12, weight="bold"),
            command=save
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            body, text="← Back",
            fg_color="#f1f5f9", hover_color="#e2e8f0",
            text_color="#374151",
            height=40, font=ctk.CTkFont(size=12),
            command=self._show_profile_view
        ).pack(fill="x")

    # =================================================
    # ANIMATION — slides in/out from RIGHT
    # =================================================
    def open(self):
        self.is_open = True
        self.panel.lift()
        start = self.parent.winfo_width()
        self._animate(start, self._right_edge(), step=-28)

    def close(self):
        self.is_open = False
        self._animate(self._right_edge(), self.parent.winfo_width(), step=28)

    def _animate(self, x, target, step):
        self.panel.place(x=x, y=self.navbar_height)
        if (step < 0 and x > target) or (step > 0 and x < target):
            next_x = max(x + step, target) if step < 0 else min(x + step, target)
            self.parent.after(8, lambda: self._animate(next_x, target, step))

    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()