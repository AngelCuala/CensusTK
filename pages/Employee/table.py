import tkinter as tk
from tkinter import ttk, messagebox
from pages.data import resident_data
from db import connect_db


def create_table(parent):

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
        left, text="Residents",
        font=("Segoe UI", 22, "bold"),
        bg="#1a2057", fg="#ffffff"
    ).pack(anchor="w", pady=(20, 2))

    tk.Label(
        left, text="Browse and manage all registered residents",
        font=("Segoe UI", 11),
        bg="#1a2057", fg="#8b9fd4"
    ).pack(anchor="w")

    right = tk.Frame(banner_inner, bg="#1a2057")
    right.pack(side="right", fill="y", pady=28)

    pill = tk.Label(
        right, text="  🏘️  Resident Records  ",
        font=("Segoe UI", 10),
        bg="#2d3b80", fg="#a5b4fc",
        padx=10, pady=6
    )
    pill.pack(side="right")

    # ── Section label ────────────────────────────────
    tk.Label(
        frame, text="RESIDENT LIST",
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

    hint = tk.Label(
        toolbar,
        text="Double-click a row to view full resident details",
        font=("Segoe UI", 9),
        bg="white", fg="#9ca3af"
    )
    hint.pack(side="left", padx=4)

    def style_btn(btn, bg, hover):
        btn.configure(
            bg=bg, fg="white", relief="flat", bd=0,
            padx=16, pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    refresh_btn = tk.Button(toolbar, text="⟳  Refresh")
    delete_btn  = tk.Button(toolbar, text="🗑  Delete")

    style_btn(refresh_btn, "#374151", "#4b5563")
    style_btn(delete_btn,  "#dc2626", "#b91c1c")

    delete_btn.pack(side="right", padx=(6, 0))
    refresh_btn.pack(side="right")

    # Thin divider
    tk.Frame(table_container, bg="#f0f2f8", height=1).pack(fill="x", padx=16)

    # ── Treeview styling ─────────────────────────────
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Residents.Treeview",
        background="#ffffff",
        foreground="#111827",
        rowheight=42,
        fieldbackground="#ffffff",
        borderwidth=0,
        font=("Segoe UI", 11)
    )
    style.configure(
        "Residents.Treeview.Heading",
        background="#f8fafc",
        foreground="#6b7280",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(10, 10)
    )
    style.map(
        "Residents.Treeview",
        background=[("selected", "#eef0fb")],
        foreground=[("selected", "#1a2057")]
    )
    style.map(
        "Residents.Treeview.Heading",
        background=[("active", "#f1f5f9")]
    )

    columns = ("Name", "Age", "Address")
    tree = ttk.Treeview(
        table_container, columns=columns,
        show="headings", style="Residents.Treeview"
    )

    col_widths = {"Name": 280, "Age": 100, "Address": 300}
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=col_widths.get(col, 150), anchor="w")

    tree.tag_configure("odd",  background="#ffffff")
    tree.tag_configure("even", background="#f8fafc")

    tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # ── Load Data ────────────────────────────────────
    def load_data():
        tree.delete(*tree.get_children())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                pi.Personal_Information_ID,
                pi.First_Name,
                pi.Last_Name,
                pi.Age,
                pi.Street_Name
            FROM Personal_Information pi
            LEFT JOIN deleted_responders dr
                ON pi.Respondent_ID = dr.Respondent_ID
            WHERE dr.Respondent_ID IS NULL
        """)
        for idx, row in enumerate(cursor.fetchall()):
            person_id = row[0]
            fullname  = f"{row[1]} {row[2]}"
            tag = "even" if idx % 2 == 0 else "odd"
            tree.insert("", "end", iid=str(person_id), tags=(tag,),
                        values=(fullname, row[3], row[4]))
        conn.close()

    load_data()

    # ── Delete ───────────────────────────────────────
    def delete_resident():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a resident first")
            return
        if not messagebox.askyesno("Confirm Delete", "Move resident to trash?"):
            return
        person_id = selected[0]
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT Respondent_ID FROM Personal_Information
                WHERE Personal_Information_ID = %s
            """, (person_id,))
            result = cursor.fetchone()
            if not result:
                return
            cursor.execute("""
                INSERT INTO deleted_responders (Respondent_ID) VALUES (%s)
            """, (result[0],))
            conn.commit()
            messagebox.showinfo("Deleted", "Resident moved to trash")
            load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    refresh_btn.config(command=load_data)
    delete_btn.config(command=delete_resident)

    # ── Detail popup ─────────────────────────────────
    def show_details(event):
        selected = tree.selection()
        if not selected:
            return
        person_id = selected[0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                pi.First_Name, pi.Middle_Name, pi.Last_Name, pi.Extension_Name,
                pi.Age, pi.Date_Of_Birth, pi.Gender,
                pi.House_Number, pi.Street_Name, pi.Barangay,
                pi.Religion, pi.Contact_Number,
                ei.Employed_or_Unemployed, ei.Job_Type, ei.Emplyoer,
                ei.Emplyoment_Status, ei.Work_Place, ei.Monthly_Income,
                ei.Unemplyoment_Reason,
                edu.Still_in_School, edu.Highest_Education_Level,
                edu.Reason_For_Leaving_School, edu.ALS_Interested,
                ofw.OFW_Status, ofw.Country, ofw.Occupation,
                ofw.Contract_Period, ofw.Planning_to_Return_Abroad,
                yi.Youth_Status, yi.Member_Of_Organization,
                yi.Organization_Name, yi.Organization_Interest, yi.SK_Suggestion,
                t.Civil_Registration, t.Immunization, t.Health,
                r.Date_Of_Interview
            FROM Personal_Information pi
            LEFT JOIN responders r             ON pi.Respondent_ID = r.Respondent_ID
            LEFT JOIN Employment_Information ei ON pi.Respondent_ID = ei.Respondent_ID
            LEFT JOIN Education_Information edu ON pi.Respondent_ID = edu.Respondent_ID
            LEFT JOIN OFW_Information ofw       ON pi.Respondent_ID = ofw.Respondent_ID
            LEFT JOIN Youth_Information yi      ON pi.Respondent_ID = yi.Respondent_ID
            LEFT JOIN Toddlers t               ON pi.Respondent_ID = t.Respondent_ID
            WHERE pi.Personal_Information_ID = %s
        """, (person_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return

        fullname = f"{row[0]} {row[2]}"

        # ── Detail window ─────────────────────────────
        win = tk.Toplevel(frame)
        win.title(fullname)
        win.geometry("680x560")
        win.configure(bg="#f0f2f8")
        win.resizable(True, True)

        # Header
        header = tk.Frame(win, bg="#1a2057", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        hinner = tk.Frame(header, bg="#1a2057")
        hinner.pack(fill="both", expand=True, padx=26)

        # Avatar initials
        initials = row[0][0].upper() if row[0] else "?"
        if row[2]:
            initials += row[2][0].upper()

        av = tk.Canvas(hinner, width=52, height=52, bg="#1a2057", highlightthickness=0)
        av.pack(side="left", pady=18)
        av.create_oval(2, 2, 50, 50, fill="#2d3b80", outline="#4353BD", width=2)
        av.create_text(26, 26, text=initials,
                       font=("Segoe UI", 16, "bold"), fill="white")

        title_col = tk.Frame(hinner, bg="#1a2057")
        title_col.pack(side="left", padx=14, fill="both")

        tk.Label(
            title_col, text=fullname,
            font=("Segoe UI", 17, "bold"),
            bg="#1a2057", fg="white"
        ).pack(anchor="w", pady=(20, 2))

        tk.Label(
            title_col, text="Resident Information",
            font=("Segoe UI", 10),
            bg="#1a2057", fg="#8b9fd4"
        ).pack(anchor="w")

        # Section groups
        SECTIONS = [
            ("👤  Personal", [
                ("First Name", row[0]), ("Middle Name", row[1]),
                ("Last Name", row[2]),  ("Extension Name", row[3]),
                ("Age", row[4]),        ("Birthdate", row[5]),
                ("Gender", row[6]),     ("House Number", row[7]),
                ("Street", row[8]),     ("Barangay", row[9]),
                ("Religion", row[10]),  ("Contact Number", row[11]),
            ]),
            ("💼  Employment", [
                ("Employment Status", row[12]), ("Job Type", row[13]),
                ("Employer", row[14]),          ("Employment Type", row[15]),
                ("Work Place", row[16]),         ("Monthly Income", row[17]),
                ("Unemployment Reason", row[18]),
            ]),
            ("🎓  Education", [
                ("Still In School", row[19]),    ("Highest Education", row[20]),
                ("Reason Left School", row[21]), ("ALS Interested", row[22]),
            ]),
            ("✈️  OFW", [
                ("OFW Status", row[23]),          ("Country", row[24]),
                ("Occupation", row[25]),          ("Contract Period", row[26]),
                ("Planning Return Abroad", row[27]),
            ]),
            ("🌱  Youth", [
                ("Youth Status", row[28]),         ("Organization Member", row[29]),
                ("Organization Name", row[30]),    ("Organization Interest", row[31]),
                ("SK Suggestion", row[32]),
            ]),
            ("🍼  Toddler", [
                ("Civil Registration", row[33]),
                ("Immunization", row[34]),
                ("Health Status", row[35]),
            ]),
            ("📋  Interview", [
                ("Interview Date", row[36]),
            ]),
        ]

        # Scrollable body
        outer = tk.Frame(win, bg="#f0f2f8")
        outer.pack(fill="both", expand=True, padx=20, pady=16)

        canvas = tk.Canvas(outer, bg="#f0f2f8", highlightthickness=0)
        vbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = tk.Frame(canvas, bg="#f0f2f8")
        cw = canvas.create_window((0, 0), window=body, anchor="nw")
        body.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))

        for sec_title, fields in SECTIONS:
            # Section header
            sec_hdr = tk.Frame(body, bg="#f0f2f8")
            sec_hdr.pack(fill="x", pady=(10, 2))
            tk.Label(
                sec_hdr, text=sec_title,
                font=("Segoe UI", 9, "bold"),
                bg="#f0f2f8", fg="#6b7280"
            ).pack(anchor="w", padx=4)

            # Section card
            card = tk.Frame(
                body, bg="white",
                highlightbackground="#e8eaf0", highlightthickness=1
            )
            card.pack(fill="x", pady=(0, 4))
            card.grid_columnconfigure(0, weight=1, uniform="col")
            card.grid_columnconfigure(1, weight=3, uniform="col")

            for i, (label, value) in enumerate(fields):
                bg = "#ffffff" if i % 2 == 0 else "#f8fafc"

                lf = tk.Frame(card, bg=bg)
                lf.grid(row=i, column=0, sticky="nsew")
                tk.Label(
                    lf, text=label,
                    bg=bg, fg="#374151",
                    font=("Segoe UI", 10, "bold"),
                    anchor="w", padx=16, pady=11
                ).pack(fill="both")

                vf = tk.Frame(card, bg=bg,
                              highlightbackground="#f0f2f8", highlightthickness=1)
                vf.grid(row=i, column=1, sticky="nsew")
                tk.Label(
                    vf, text=str(value) if value is not None else "—",
                    bg=bg, fg="#4b5563",
                    font=("Segoe UI", 10),
                    anchor="w", padx=16, pady=11,
                    wraplength=380, justify="left"
                ).pack(fill="both")

                card.grid_rowconfigure(i, weight=1)

        def _scroll(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _scroll)

    tree.bind("<Double-1>", show_details)

    return frame