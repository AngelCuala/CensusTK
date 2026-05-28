import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db import connect_db


def ensure_deleted_teams_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deleted_teams (
            Trash_ID INT AUTO_INCREMENT PRIMARY KEY,
            Team_ID INT,
            Team_Name VARCHAR(255),
            Barangay VARCHAR(255),
            Deleted_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def get_used_barangays(exclude_team_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    if exclude_team_id:
        cursor.execute("SELECT Barangay FROM teams WHERE Team_ID != %s", (exclude_team_id,))
    else:
        cursor.execute("SELECT Barangay FROM teams")
    used = {row[0] for row in cursor.fetchall()}
    conn.close()
    return used


def get_available_users(exclude_team_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    if exclude_team_id:
        cursor.execute("""
            SELECT User_ID, First_Name, Last_Name FROM accounts
            WHERE User_ID NOT IN (
                SELECT User_ID FROM team_members WHERE Team_ID != %s
            )
        """, (exclude_team_id,))
    else:
        cursor.execute("""
            SELECT User_ID, First_Name, Last_Name FROM accounts
            WHERE User_ID NOT IN (SELECT User_ID FROM team_members)
        """)
    users = cursor.fetchall()
    conn.close()
    return users


BARANGAY_LIST = [
    "Barangay Zone I", "Barangay Zone II", "Barangay Zone III",
    "Barangay Zone IV", "Barangay Zone V", "Barangay Zone VI",
    "Barangay Zone VII", "Barangay Zone VIII",
    "De La Paz", "San Antonio", "San Buenaventura", "San Diego",
    "San Isidro", "San Jose", "San Juan", "San Luis",
    "San Pablo", "San Pedro", "San Rafael", "San Roque",
    "San Salvador", "Santo Domingo", "Santo Tomas"
]


def create_teams_page(parent):

    ensure_deleted_teams_table()

    page = ctk.CTkFrame(parent, fg_color="#f0f2f8")

    # ── Header Banner ────────────────────────────────
    banner = tk.Frame(page, bg="#1a2057", height=100)
    banner.pack(fill="x", padx=24, pady=(24, 0))
    banner.pack_propagate(False)

    banner_inner = tk.Frame(banner, bg="#1a2057")
    banner_inner.pack(fill="both", expand=True, padx=28)

    left_hdr = tk.Frame(banner_inner, bg="#1a2057")
    left_hdr.pack(side="left", fill="both", expand=True)

    tk.Label(
        left_hdr, text="Teams Management",
        font=("Segoe UI", 22, "bold"),
        bg="#1a2057", fg="#ffffff"
    ).pack(anchor="w", pady=(20, 2))

    tk.Label(
        left_hdr, text="Organise survey teams and assign barangays",
        font=("Segoe UI", 11),
        bg="#1a2057", fg="#8b9fd4"
    ).pack(anchor="w")

    right_hdr = tk.Frame(banner_inner, bg="#1a2057")
    right_hdr.pack(side="right", fill="y", pady=26)

    create_banner_btn = tk.Label(
        right_hdr, text="  ＋  Create Team  ",
        font=("Segoe UI", 10, "bold"),
        bg="#4353BD", fg="white",
        cursor="hand2", padx=10, pady=8
    )
    create_banner_btn.pack(side="right")

    # ── Section label ────────────────────────────────
    tk.Label(
        page, text="TEAM LIST",
        font=("Segoe UI", 9, "bold"),
        bg="#f0f2f8", fg="#9ca3af"
    ).pack(anchor="w", padx=24, pady=(16, 4))

    # ── Scrollable team cards ─────────────────────────
    teams_frame = ctk.CTkScrollableFrame(page, fg_color="transparent")
    teams_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    # =========================================================
    # CREATE TEAM WINDOW
    # =========================================================
    def open_create_team():
        window = ctk.CTkToplevel()
        window.title("Create Team")
        window.geometry("860x660")
        window.transient(parent.winfo_toplevel())
        window.grab_set()
        window.focus_force()
        window.resizable(False, False)
        window.after(10, lambda: window.focus())
        window.configure(fg_color="#f0f2f8")

        # Header
        hdr = tk.Frame(window, bg="#1a2057", height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(
            hdr, text="✏️  Create New Team",
            font=("Segoe UI", 15, "bold"),
            bg="#1a2057", fg="white"
        ).pack(side="left", padx=26, pady=20)

        main = tk.Frame(window, bg="#f0f2f8")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ---- LEFT PANEL ----
        left_card = tk.Frame(
            main, bg="white",
            highlightbackground="#e8eaf0", highlightthickness=1
        )
        left_card.pack(side="left", fill="y", padx=(0, 14), ipadx=4)

        tk.Label(
            left_card, text="TEAM DETAILS",
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#9ca3af"
        ).pack(anchor="w", padx=20, pady=(18, 2))
        tk.Frame(left_card, bg="#f0f2f8", height=1).pack(fill="x", padx=20, pady=(0, 10))

        def lbl(parent, text):
            tk.Label(
                parent, text=text, bg="white",
                fg="#374151", font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", padx=20, pady=(10, 2))

        lbl(left_card, "Team Name")
        team_name = ctk.CTkEntry(left_card, width=260, height=38, placeholder_text="e.g. Alpha Team")
        team_name.pack(padx=20)

        lbl(left_card, "Barangay")
        used_brgys = get_used_barangays()
        available_brgys = [b for b in BARANGAY_LIST if b not in used_brgys]
        barangay = ctk.CTkComboBox(
            left_card,
            values=available_brgys if available_brgys else ["No barangays available"],
            width=260, height=38, state="readonly"
        )
        barangay.pack(padx=20)
        barangay.set("Select Barangay")

        lbl(left_card, "Team Leader")
        leader_var = {"id": None}
        leader_combo = ctk.CTkComboBox(
            left_card, values=["Select Leader"],
            width=260, height=38, state="readonly"
        )
        leader_combo.pack(padx=20)
        leader_combo.set("Select Leader")

        tk.Frame(left_card, bg="white").pack(expand=True, fill="both")

        create_btn = tk.Label(
            left_card, text="Create Team",
            bg="#4353BD", fg="white",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2", pady=13, anchor="center"
        )
        create_btn.pack(fill="x", padx=20, pady=20)
        create_btn.bind("<Enter>", lambda e: create_btn.config(bg="#3742fa"))
        create_btn.bind("<Leave>", lambda e: create_btn.config(bg="#4353BD"))

        # ---- RIGHT PANEL ----
        right_card = tk.Frame(
            main, bg="white",
            highlightbackground="#e8eaf0", highlightthickness=1
        )
        right_card.pack(side="left", fill="both", expand=True)

        tk.Label(
            right_card, text="SELECT MEMBERS",
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#9ca3af"
        ).pack(anchor="w", padx=20, pady=(18, 2))
        tk.Frame(right_card, bg="#f0f2f8", height=1).pack(fill="x", padx=20, pady=(0, 8))

        scroll_outer = tk.Frame(right_card, bg="white")
        scroll_outer.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        canvas = tk.Canvas(scroll_outer, bg="white", highlightthickness=0)
        sb = tk.Scrollbar(scroll_outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        users_frame = tk.Frame(canvas, bg="white")
        cw = canvas.create_window((0, 0), window=users_frame, anchor="nw")
        users_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        selected_users = []
        user_id_to_name = {}

        users = get_available_users()
        for user_id, fname, lname in users:
            full = f"{fname} {lname}"
            user_id_to_name[user_id] = full
            var = tk.BooleanVar()

            row_frame = tk.Frame(users_frame, bg="white",
                                 highlightbackground="#f0f2f8", highlightthickness=1)
            row_frame.pack(fill="x", pady=2, padx=4)

            def on_check(uid=user_id, v=var):
                checked = [user_id_to_name[u] for u, vv in selected_users if vv.get()]
                leader_combo.configure(values=checked if checked else ["Select Leader"])
                if leader_combo.get() not in checked:
                    leader_combo.set("Select Leader")
                row_frame.config(bg="#eef0fb" if v.get() else "white")

            cb = ctk.CTkCheckBox(
                row_frame, text=full, variable=var, command=on_check,
                fg_color="#4353BD", hover_color="#3742fa"
            )
            cb.pack(anchor="w", padx=12, pady=8)
            selected_users.append((user_id, var))

        name_to_id = {v: k for k, v in user_id_to_name.items()}

        def create_team():
            name = team_name.get().strip()
            brgy = barangay.get()
            leader_name = leader_combo.get()

            if not name or brgy in ("Select Barangay", "No barangays available"):
                messagebox.showerror("Error", "Please complete all fields.")
                return
            checked = [(uid, var) for uid, var in selected_users if var.get()]
            if not checked:
                messagebox.showerror("Error", "Please select at least one member.")
                return
            if leader_name == "Select Leader":
                messagebox.showerror("Error", "Please select a team leader.")
                return

            leader_id = name_to_id.get(leader_name)
            try:
                conn2 = connect_db()
                cursor2 = conn2.cursor()
# =========================================
# INSERT TEAM WITH LEADER_ID
# =========================================
                cursor2.execute("""
                    INSERT INTO teams
                    (Team_Name, Barangay, Leader_ID, Status)
                    VALUES (%s, %s, %s, %s)
                """, (
                    name,
                    brgy,
                    leader_id,
                    "Active"
                ))

                # GET TEAM ID
                team_id = cursor2.lastrowid

                # =========================================
                # INSERT MEMBERS
                # =========================================
                for user_id, var in selected_users:

                    if var.get():

                        role = "Leader" if user_id == leader_id else "Member"

                        cursor2.execute("""
                            INSERT INTO team_members
                            (Team_ID, User_ID, Role, Status)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            team_id,
                            user_id,
                            role,
                            "Active"
                        ))
                conn2.commit()
                conn2.close()
                messagebox.showinfo("Success", "Team created successfully!")
                parent.after(100, refresh_teams)
                window.after(200, window.withdraw)
                window.after(250, window.destroy)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        create_btn.bind("<Button-1>", lambda e: create_team())

    create_banner_btn.bind("<Button-1>", lambda e: open_create_team())
    create_banner_btn.bind("<Enter>", lambda e: create_banner_btn.config(bg="#3742fa"))
    create_banner_btn.bind("<Leave>", lambda e: create_banner_btn.config(bg="#4353BD"))

    # =========================================================
    # REFRESH / RENDER TEAM CARDS
    # =========================================================
    def refresh_teams():
        for widget in teams_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT Team_ID, Team_Name, Barangay FROM teams ORDER BY Team_ID DESC")
        teams = cursor.fetchall()

        if not teams:
            tk.Label(
                teams_frame, text="No teams yet. Click 'Create Team' to get started.",
                font=("Segoe UI", 12), bg="#f0f2f8", fg="#9ca3af"
            ).pack(pady=40)
            conn.close()
            return

        for team_id, t_name, brgy in teams:
            cursor.execute("SELECT COUNT(*) FROM team_members WHERE Team_ID = %s", (team_id,))
            members = cursor.fetchone()[0]

            cursor.execute("""
                SELECT a.First_Name, a.Last_Name
                FROM team_members tm
                JOIN accounts a ON a.User_ID = tm.User_ID
                WHERE tm.Team_ID = %s AND tm.Role = 'Leader' LIMIT 1
            """, (team_id,))
            leader_row = cursor.fetchone()
            leader_name = f"{leader_row[0]} {leader_row[1]}" if leader_row else "No Leader"

            # Initials avatar colour cycling
            colours = ["#4353BD", "#0ea5e9", "#10b981", "#f59e0b", "#d946ef", "#ef4444"]
            accent = colours[team_id % len(colours)]

            # ---- CARD ────────────────────────────────
            card = tk.Frame(
                teams_frame, bg="white",
                highlightbackground="#e8eaf0", highlightthickness=1
            )
            card.pack(fill="x", pady=8, padx=2)

            # Left accent stripe
            stripe = tk.Frame(card, bg=accent, width=6)
            stripe.pack(side="left", fill="y")

            body = tk.Frame(card, bg="white")
            body.pack(side="left", fill="both", expand=True, padx=18, pady=16)

            # Top row: name + buttons
            top_row = tk.Frame(body, bg="white")
            top_row.pack(fill="x")

            # Team initial bubble
            init_canvas = tk.Canvas(top_row, width=44, height=44, bg="white", highlightthickness=0)
            init_canvas.pack(side="left", padx=(0, 12))
            init_letter = t_name[0].upper() if t_name else "T"
            # Create tinted bg
            r_hex = int(accent[1:3], 16)
            g_hex = int(accent[3:5], 16)
            b_hex = int(accent[5:7], 16)
            tint = f"#{min(r_hex+160,255):02x}{min(g_hex+160,255):02x}{min(b_hex+160,255):02x}"
            init_canvas.create_oval(2, 2, 42, 42, fill=tint, outline="")
            init_canvas.create_text(22, 22, text=init_letter,
                                    font=("Segoe UI", 16, "bold"), fill=accent)

            name_col = tk.Frame(top_row, bg="white")
            name_col.pack(side="left", fill="both", expand=True)

            tk.Label(
                name_col, text=t_name,
                font=("Segoe UI", 15, "bold"),
                bg="white", fg="#111827"
            ).pack(anchor="w")

            tk.Label(
                name_col, text=f"📍 {brgy}",
                font=("Segoe UI", 10),
                bg="white", fg="#6b7280"
            ).pack(anchor="w")

            # Buttons
            btn_frame = tk.Frame(top_row, bg="white")
            btn_frame.pack(side="right")

            def make_edit_btn(btn, tid=team_id, old_name=t_name, old_brgy=brgy):
                btn.bind("<Button-1>", lambda e: edit_team(tid, old_name, old_brgy))
                btn.bind("<Enter>", lambda e: btn.config(bg="#d97706"))
                btn.bind("<Leave>", lambda e: btn.config(bg="#f59e0b"))

            def make_del_btn(btn, tid=team_id, name=t_name, tbrgy=brgy):
                btn.bind("<Button-1>", lambda e: delete_team(tid, name, tbrgy))
                btn.bind("<Enter>", lambda e: btn.config(bg="#b91c1c"))
                btn.bind("<Leave>", lambda e: btn.config(bg="#dc2626"))

            edit_btn = tk.Label(
                btn_frame, text="✏️  Edit",
                bg="#f59e0b", fg="white",
                font=("Segoe UI", 9, "bold"),
                cursor="hand2", padx=12, pady=6
            )
            edit_btn.pack(side="left", padx=(0, 6))
            make_edit_btn(edit_btn)

            del_btn = tk.Label(
                btn_frame, text="🗑  Delete",
                bg="#dc2626", fg="white",
                font=("Segoe UI", 9, "bold"),
                cursor="hand2", padx=12, pady=6
            )
            del_btn.pack(side="left")
            make_del_btn(del_btn)

            # Divider
            tk.Frame(body, bg="#f0f2f8", height=1).pack(fill="x", pady=(12, 10))

            # Footer meta pills
            meta_row = tk.Frame(body, bg="white")
            meta_row.pack(fill="x")

            def meta_pill(parent, icon, text, pill_bg, pill_fg):
                pill = tk.Frame(parent, bg=pill_bg)
                pill.pack(side="left", padx=(0, 8))
                tk.Label(
                    pill, text=f"  {icon}  {text}  ",
                    font=("Segoe UI", 9),
                    bg=pill_bg, fg=pill_fg,
                    pady=4
                ).pack()

            meta_pill(meta_row, "👑", leader_name,   "#fefce8", "#92400e")
            meta_pill(meta_row, "👥", f"{members} Members", "#eff6ff", "#1e40af")

        conn.close()

    # =========================================================
    # DELETE TEAM
    # =========================================================
    def delete_team(tid, name, tbrgy):
        if messagebox.askyesno("Delete", f"Move '{name}' to trash?"):
            try:
                conn2 = connect_db()
                cursor2 = conn2.cursor()
                cursor2.execute(
                    "INSERT INTO deleted_teams (Team_ID, Team_Name, Barangay) VALUES (%s, %s, %s)",
                    (tid, name, tbrgy)
                )
                cursor2.execute("DELETE FROM team_members WHERE Team_ID = %s", (tid,))
                cursor2.execute("DELETE FROM teams WHERE Team_ID = %s", (tid,))
                conn2.commit()
                conn2.close()
                teams_frame.after(100, refresh_teams)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # =========================================================
    # EDIT TEAM WINDOW
    # =========================================================
    def edit_team(tid, old_name, old_brgy):
        edit_window = ctk.CTkToplevel()
        edit_window.title("Edit Team")
        edit_window.geometry("620x620")
        edit_window.transient(parent.winfo_toplevel())
        edit_window.grab_set()
        edit_window.configure(fg_color="#f0f2f8")

        # Header
        hdr = tk.Frame(edit_window, bg="#1a2057", height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(
            hdr, text="✏️  Edit Team",
            font=("Segoe UI", 15, "bold"),
            bg="#1a2057", fg="white"
        ).pack(side="left", padx=26, pady=20)

        form_outer = tk.Frame(edit_window, bg="#f0f2f8")
        form_outer.pack(fill="both", expand=True, padx=20, pady=20)

        form = tk.Frame(
            form_outer, bg="white",
            highlightbackground="#e8eaf0", highlightthickness=1
        )
        form.pack(fill="x", pady=(0, 14))

        tk.Label(
            form, text="TEAM DETAILS",
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#9ca3af"
        ).pack(anchor="w", padx=20, pady=(16, 2))
        tk.Frame(form, bg="#f0f2f8", height=1).pack(fill="x", padx=20, pady=(0, 8))

        def lbl(text):
            tk.Label(
                form, text=text, bg="white",
                fg="#374151", font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", padx=20, pady=(10, 2))

        lbl("Team Name")
        name_entry = ctk.CTkEntry(form, width=560, height=38)
        name_entry.insert(0, old_name)
        name_entry.pack(padx=20)

        lbl("Barangay")
        used_brgys = get_used_barangays(exclude_team_id=tid)
        available_brgys = [b for b in BARANGAY_LIST if b not in used_brgys]
        barangay_combo = ctk.CTkComboBox(
            form,
            values=available_brgys if available_brgys else [old_brgy],
            width=560, state="readonly"
        )
        barangay_combo.pack(padx=20)
        barangay_combo.set(old_brgy)

        lbl("Team Leader")
        edit_leader_combo = ctk.CTkComboBox(
            form, values=["Select Leader"],
            width=560, state="readonly"
        )
        edit_leader_combo.pack(padx=20, pady=(0, 16))

        # Members section
        mem_card = tk.Frame(
            form_outer, bg="white",
            highlightbackground="#e8eaf0", highlightthickness=1
        )
        mem_card.pack(fill="both", expand=True)

        tk.Label(
            mem_card, text="SELECT MEMBERS",
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#9ca3af"
        ).pack(anchor="w", padx=20, pady=(16, 2))
        tk.Frame(mem_card, bg="#f0f2f8", height=1).pack(fill="x", padx=20, pady=(0, 6))

        scroll_outer = ctk.CTkScrollableFrame(mem_card, fg_color="white", height=180)
        scroll_outer.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        user_vars = {}
        edit_uid_to_name = {}
        edit_name_to_id = {}

        conn3 = connect_db()
        cursor3 = conn3.cursor()
        cursor3.execute("""
            SELECT User_ID, First_Name, Last_Name FROM accounts
            WHERE User_ID NOT IN (
                SELECT User_ID FROM team_members WHERE Team_ID != %s
            )
        """, (tid,))
        all_users = cursor3.fetchall()
        cursor3.execute("SELECT User_ID, Role FROM team_members WHERE Team_ID = %s", (tid,))
        existing = {row[0]: row[1] for row in cursor3.fetchall()}
        conn3.close()

        def rebuild_leader_options():
            checked_names = [edit_uid_to_name[uid] for uid, var in user_vars.items() if var.get()]
            edit_leader_combo.configure(values=checked_names if checked_names else ["Select Leader"])
            if edit_leader_combo.get() not in checked_names:
                edit_leader_combo.set("Select Leader")

        for user_id, fname, lname in all_users:
            full = f"{fname} {lname}"
            edit_uid_to_name[user_id] = full
            edit_name_to_id[full] = user_id
            is_checked = user_id in existing
            var = tk.BooleanVar(value=is_checked)

            row_f = tk.Frame(scroll_outer, bg="white",
                             highlightbackground="#f0f2f8", highlightthickness=1)
            row_f.pack(fill="x", pady=2)

            def on_chk(uid=user_id, v=var, rf=row_f):
                rebuild_leader_options()
                rf.config(bg="#eef0fb" if v.get() else "white")

            cb = ctk.CTkCheckBox(
                row_f, text=full, variable=var, command=on_chk,
                fg_color="#4353BD", hover_color="#3742fa"
            )
            cb.pack(anchor="w", padx=12, pady=7)
            if is_checked:
                row_f.config(bg="#eef0fb")
            user_vars[user_id] = var

        # Set initial leader options and pre-select existing leader
        checked_names = [edit_uid_to_name[uid] for uid, var in user_vars.items() if var.get()]
        edit_leader_combo.configure(values=checked_names if checked_names else ["Select Leader"])

        conn4 = connect_db()
        cursor4 = conn4.cursor()
        cursor4.execute("""
            SELECT a.First_Name, a.Last_Name FROM team_members tm
            JOIN accounts a ON a.User_ID = tm.User_ID
            WHERE tm.Team_ID = %s AND tm.Role = 'Leader' LIMIT 1
        """, (tid,))
        lrow = cursor4.fetchone()
        conn4.close()
        edit_leader_combo.set(f"{lrow[0]} {lrow[1]}" if lrow else "Select Leader")

        def save_edit():
            new_name = name_entry.get().strip()
            new_brgy = barangay_combo.get()
            new_leader_name = edit_leader_combo.get()

            if not new_name:
                messagebox.showerror("Error", "Team name required")
                return
            if new_leader_name == "Select Leader":
                messagebox.showerror("Error", "Please select a team leader.")
                return

            new_leader_id = edit_name_to_id.get(new_leader_name)
            try:
                conn3 = connect_db()
                cursor3 = conn3.cursor()
                cursor3.execute("""
                    UPDATE teams
                    SET Team_Name = %s,
                        Barangay = %s,
                        Leader_ID = %s
                    WHERE Team_ID = %s
                """, (
                    new_name,
                    new_brgy,
                    new_leader_id,
                    tid
                ))
                cursor3.execute("DELETE FROM team_members WHERE Team_ID=%s", (tid,))
                for user_id, var in user_vars.items():
                    if var.get():
                        role = "Leader" if user_id == new_leader_id else "Member"
                        cursor3.execute(
                            "INSERT INTO team_members (Team_ID, User_ID, Role) VALUES (%s, %s, %s)",
                            (tid, user_id, role)
                        )
                conn3.commit()
                conn3.close()
                messagebox.showinfo("Success", "Team updated!")
                edit_window.destroy()
                refresh_teams()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn = tk.Label(
            form_outer, text="Save Changes",
            bg="#4353BD", fg="white",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2", pady=13, anchor="center"
        )
        save_btn.pack(fill="x", pady=(12, 0))
        save_btn.bind("<Button-1>", lambda e: save_edit())
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#3742fa"))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg="#4353BD"))

    teams_frame.after(100, refresh_teams)
    page.refresh_teams = refresh_teams

    return page