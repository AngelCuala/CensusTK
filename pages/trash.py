import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db


def create_trash(parent, teams_page_ref=None):

    frame = tk.Frame(parent, bg="#f0f2f8")

    # ── Header Banner ────────────────────────────────
    banner = tk.Frame(frame, bg="#1a2057", height=100)
    banner.pack(fill="x", padx=24, pady=(24, 0))
    banner.pack_propagate(False)

    banner_inner = tk.Frame(banner, bg="#1a2057")
    banner_inner.pack(fill="both", expand=True, padx=28)

    left_hdr = tk.Frame(banner_inner, bg="#1a2057")
    left_hdr.pack(side="left", fill="both", expand=True)

    tk.Label(
        left_hdr, text="Trash",
        font=("Segoe UI", 22, "bold"),
        bg="#1a2057", fg="#ffffff"
    ).pack(anchor="w", pady=(20, 2))

    tk.Label(
        left_hdr, text="Deleted teams — restore or permanently remove",
        font=("Segoe UI", 11),
        bg="#1a2057", fg="#8b9fd4"
    ).pack(anchor="w")

    right_hdr = tk.Frame(banner_inner, bg="#1a2057")
    right_hdr.pack(side="right", fill="y", pady=28)

    pill = tk.Label(
        right_hdr, text="  🗑️  Recycle Bin  ",
        font=("Segoe UI", 10),
        bg="#2d3b80", fg="#a5b4fc",
        padx=10, pady=6
    )
    pill.pack(side="right")

    # ── Section label ────────────────────────────────
    tk.Label(
        frame, text="DELETED TEAMS",
        font=("Segoe UI", 9, "bold"),
        bg="#f0f2f8", fg="#9ca3af"
    ).pack(anchor="w", padx=24, pady=(16, 4))

    # ── Main container ───────────────────────────────
    table_container = tk.Frame(
        frame, bg="white",
        highlightbackground="#e8eaf0",
        highlightthickness=1
    )
    table_container.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    # ── Toolbar ──────────────────────────────────────
    toolbar = tk.Frame(table_container, bg="white")
    toolbar.pack(fill="x", padx=16, pady=14)

    tk.Label(
        toolbar,
        text="Click 'Select' to pick teams, then Restore or Delete permanently.",
        font=("Segoe UI", 9),
        bg="white", fg="#9ca3af"
    ).pack(side="left", padx=4)

    select_mode = {"active": False}

    button_container = tk.Frame(toolbar, bg="white")
    button_container.pack(side="right")

    def style_btn(btn, bg, hover):
        btn.configure(
            bg=bg, fg="white", relief="flat", bd=0,
            padx=14, pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    select_btn  = tk.Button(button_container, text="Select")
    delete_btn  = tk.Button(button_container, text="🗑  Delete Permanently")
    restore_btn = tk.Button(button_container, text="↩  Restore")

    style_btn(select_btn,  "#374151", "#4b5563")
    style_btn(delete_btn,  "#dc2626", "#b91c1c")
    style_btn(restore_btn, "#16a34a", "#15803d")

    select_btn.pack(side="right", padx=(6, 0))

    # Thin divider
    tk.Frame(table_container, bg="#f0f2f8", height=1).pack(fill="x", padx=16)

    # ── Treeview styling ─────────────────────────────
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Trash.Treeview",
        background="#ffffff",
        foreground="#111827",
        rowheight=42,
        fieldbackground="#ffffff",
        borderwidth=0,
        font=("Segoe UI", 11)
    )
    style.configure(
        "Trash.Treeview.Heading",
        background="#f8fafc",
        foreground="#6b7280",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(10, 10)
    )
    style.map(
        "Trash.Treeview",
        background=[("selected", "#fef2f2")],
        foreground=[("selected", "#991b1b")]
    )
    style.map(
        "Trash.Treeview.Heading",
        background=[("active", "#f1f5f9")]
    )

    columns = ("Select", "Team Name", "Barangay", "Deleted At")
    trash_tree = ttk.Treeview(
        table_container, columns=columns,
        show="headings", style="Trash.Treeview"
    )

    trash_tree.heading("Select",     text="")
    trash_tree.column("Select",      width=50,  anchor="center")
    trash_tree.heading("Team Name",  text="Team Name")
    trash_tree.column("Team Name",   width=220, anchor="w")
    trash_tree.heading("Barangay",   text="Barangay")
    trash_tree.column("Barangay",    width=200, anchor="w")
    trash_tree.heading("Deleted At", text="Deleted At")
    trash_tree.column("Deleted At",  width=180, anchor="w")

    trash_tree["displaycolumns"] = ("Team Name", "Barangay", "Deleted At")

    trash_tree.tag_configure("odd",      background="#ffffff")
    trash_tree.tag_configure("even",     background="#f8fafc")
    trash_tree.tag_configure("checked",  background="#fef2f2")

    trash_tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # ── Warning strip ─────────────────────────────────
    warn_strip = tk.Frame(
        table_container, bg="#fef2f2",
        highlightbackground="#fecaca", highlightthickness=1
    )
    warn_strip.pack(fill="x", padx=16, pady=(0, 14))

    tk.Label(
        warn_strip,
        text="⚠  Permanently deleted teams cannot be recovered.",
        font=("Segoe UI", 9),
        bg="#fef2f2", fg="#b91c1c"
    ).pack(side="left", padx=14, pady=8)

    # ── Load data ─────────────────────────────────────
    def load_trash():
        trash_tree.delete(*trash_tree.get_children())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Trash_ID, Team_ID, Team_Name, Barangay, Deleted_At
            FROM deleted_teams
            ORDER BY Deleted_At DESC
        """)
        for idx, row in enumerate(cursor.fetchall()):
            trash_id, team_id, team_name, barangay, deleted_at = row
            tag = "even" if idx % 2 == 0 else "odd"
            trash_tree.insert(
                "", "end", iid=str(trash_id),
                tags=(tag,),
                values=("☐", team_name, barangay, deleted_at)
            )
        conn.close()

    # ── Toggle select mode ────────────────────────────
    def toggle_select():
        select_mode["active"] = not select_mode["active"]

        if select_mode["active"]:
            select_btn.config(text="✕  Cancel")
            style_btn(select_btn, "#6b7280", "#4b5563")
            restore_btn.pack(side="right", padx=(6, 0))
            delete_btn.pack(side="right", padx=(6, 0))
            trash_tree["displaycolumns"] = ("Select", "Team Name", "Barangay", "Deleted At")
        else:
            select_btn.config(text="Select")
            style_btn(select_btn, "#374151", "#4b5563")
            delete_btn.pack_forget()
            restore_btn.pack_forget()
            trash_tree["displaycolumns"] = ("Team Name", "Barangay", "Deleted At")
            # Clear all checkmarks
            for item in trash_tree.get_children():
                vals = list(trash_tree.item(item, "values"))
                vals[0] = "☐"
                trash_tree.item(item, values=vals)
                idx = trash_tree.index(item)
                trash_tree.item(item, tags=("even" if idx % 2 == 0 else "odd",))

    select_btn.config(command=toggle_select)

    # ── Get checked items ─────────────────────────────
    def get_selected():
        return [
            item for item in trash_tree.get_children()
            if trash_tree.item(item, "values")[0] == "✔"
        ]

    # ── Permanent delete ──────────────────────────────
    def delete_selected():
        selected = get_selected()
        if not selected:
            messagebox.showwarning("No Selection", "Select a team first.")
            return
        if not messagebox.askyesno(
            "Confirm Delete",
            "Permanently delete selected teams? This cannot be undone."
        ):
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            for item in selected:
                cursor.execute("DELETE FROM deleted_teams WHERE Trash_ID = %s", (int(item),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Teams permanently deleted.")
            load_trash()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Restore ───────────────────────────────────────
    def restore_selected():
        selected = get_selected()
        if not selected:
            messagebox.showwarning("No Selection", "Select a team first.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            for item in selected:
                trash_id = int(item)
                cursor.execute("""
                    SELECT Team_ID, Team_Name, Barangay
                    FROM deleted_teams WHERE Trash_ID = %s
                """, (trash_id,))
                result = cursor.fetchone()
                if result:
                    team_id, team_name, barangay = result
                    cursor.execute("""
                        INSERT INTO teams (Team_ID, Team_Name, Barangay)
                        VALUES (%s, %s, %s)
                    """, (team_id, team_name, barangay))
                    cursor.execute("DELETE FROM deleted_teams WHERE Trash_ID = %s", (trash_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Restored", "Team(s) restored successfully.")
            load_trash()
            if teams_page_ref and hasattr(teams_page_ref, "refresh_teams"):
                teams_page_ref.refresh_teams()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    delete_btn.config(command=delete_selected)
    restore_btn.config(command=restore_selected)

    # ── Checkbox click ────────────────────────────────
    def toggle_checkbox(event):
        if not select_mode["active"]:
            return
        item = trash_tree.identify_row(event.y)
        if not item:
            return
        if trash_tree.identify_column(event.x) == "#1":
            vals = list(trash_tree.item(item, "values"))
            idx  = trash_tree.index(item)
            if vals[0] == "☐":
                vals[0] = "✔"
                trash_tree.item(item, values=vals, tags=("checked",))
            else:
                vals[0] = "☐"
                base_tag = "even" if idx % 2 == 0 else "odd"
                trash_tree.item(item, values=vals, tags=(base_tag,))

    trash_tree.bind("<Button-1>", toggle_checkbox)

    load_trash()
    frame.load_trash = load_trash

    return frame