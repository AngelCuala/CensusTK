import customtkinter as ctk
from db import connect_db

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def create_dashboard(parent):

    # =========================================================
    # SCROLLABLE DASHBOARD
    # =========================================================
    dashboard = ctk.CTkScrollableFrame(
        parent,
        fg_color="#f0f2f8"
    )

    # =========================================================
    # FETCH DASHBOARD DATA
    # =========================================================
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Personal_Information")
    total_residents = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Gender = 'Male'")
    total_male = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Gender = 'Female'")
    total_female = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM responders")
    total_surveyed = cursor.fetchone()[0]

    # =========================================================
    # HEADER BANNER — gradient-style two-tone block
    # =========================================================
    banner = ctk.CTkFrame(
        dashboard,
        fg_color="#1a2057",
        corner_radius=20,
        height=110
    )
    banner.pack(fill="x", padx=24, pady=(24, 0))
    banner.pack_propagate(False)

    banner_inner = ctk.CTkFrame(banner, fg_color="transparent")
    banner_inner.pack(fill="both", expand=True, padx=28, pady=0)

    left_col = ctk.CTkFrame(banner_inner, fg_color="transparent")
    left_col.pack(side="left", fill="both", expand=True)

    ctk.CTkLabel(
        left_col,
        text="Census Dashboard",
        font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
        text_color="#ffffff"
    ).pack(anchor="w", pady=(22, 2))

    ctk.CTkLabel(
        left_col,
        text="Population records · Analytics overview · Live data",
        font=ctk.CTkFont(family="Segoe UI", size=12),
        text_color="#8b9fd4"
    ).pack(anchor="w")

    # Right side — decorative pill badges
    right_col = ctk.CTkFrame(banner_inner, fg_color="transparent")
    right_col.pack(side="right", fill="y", pady=22)

    badge = ctk.CTkFrame(right_col, fg_color="#2d3b80", corner_radius=20, height=36)
    badge.pack(side="right", padx=(0, 0))
    badge.pack_propagate(False)
    ctk.CTkLabel(
        badge,
        text="  📋  Barangay Records  ",
        font=ctk.CTkFont(family="Segoe UI", size=11),
        text_color="#a5b4fc"
    ).pack(expand=True)

    # =========================================================
    # STAT CARDS ROW
    # =========================================================
    cards_label_frame = ctk.CTkFrame(dashboard, fg_color="transparent")
    cards_label_frame.pack(fill="x", padx=24, pady=(18, 4))

    ctk.CTkLabel(
        cards_label_frame,
        text="OVERVIEW",
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        text_color="#9ca3af"
    ).pack(anchor="w")

    card_frame = ctk.CTkFrame(dashboard, fg_color="transparent")
    card_frame.pack(fill="x", padx=24, pady=(0, 20))

    for i in range(4):
        card_frame.grid_columnconfigure(i, weight=1)

    # =========================================================
    # COUNTER ANIMATION
    # =========================================================
    def animate_counter(label, target):
        current = 0
        def update():
            nonlocal current
            step = max(1, target // 30)
            if current < target:
                current += step
                label.configure(text=f"{min(current, target):,}")
                label.after(15, update)
            else:
                label.configure(text=f"{target:,}")
        update()

    # =========================================================
    # STAT CARD BUILDER
    # =========================================================
    CARD_META = [
        ("Total Residents", total_residents, "#4353BD", "#eef0fb", "👥"),
        ("Male",            total_male,      "#0ea5e9", "#e0f2fe", "♂"),
        ("Female",          total_female,    "#d946ef", "#fdf4ff", "♀"),
        ("Surveyed",        total_surveyed,  "#f59e0b", "#fffbeb", "📝"),
    ]

    def create_card(parent, title, value, accent, tint, icon, col):
        outer = ctk.CTkFrame(
            parent,
            corner_radius=18,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e8eaf0"
        )
        outer.grid(row=0, column=col, padx=7, pady=4, sticky="nsew")
        outer.grid_propagate(False)
        outer.configure(height=170)

        # Left accent stripe
        stripe = ctk.CTkFrame(outer, width=5, fg_color=accent, corner_radius=4)
        stripe.pack(side="left", fill="y", padx=(10, 0), pady=18)

        body = ctk.CTkFrame(outer, fg_color="transparent")
        body.pack(side="left", fill="both", expand=True, padx=16, pady=16)

        # Icon bubble
        icon_bubble = ctk.CTkFrame(
            body,
            width=42, height=42,
            corner_radius=12,
            fg_color=tint
        )
        icon_bubble.pack(anchor="w")
        icon_bubble.pack_propagate(False)
        ctk.CTkLabel(
            icon_bubble,
            text=icon,
            font=ctk.CTkFont(size=18),
            text_color=accent
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            body,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9ca3af"
        ).pack(anchor="w", pady=(10, 0))

        val_lbl = ctk.CTkLabel(
            body,
            text="0",
            font=ctk.CTkFont(family="Segoe UI", size=34, weight="bold"),
            text_color="#111827"
        )
        val_lbl.pack(anchor="w")
        animate_counter(val_lbl, int(value))

        # Hover
        def on_enter(e): outer.configure(fg_color="#f9faff")
        def on_leave(e): outer.configure(fg_color="#ffffff")
        outer.bind("<Enter>", on_enter)
        outer.bind("<Leave>", on_leave)

    for col, (title, value, accent, tint, icon) in enumerate(CARD_META):
        create_card(card_frame, title, value, accent, tint, icon, col)

    # =========================================================
    # AGE GROUP SECTION
    # =========================================================
    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Age BETWEEN 0 AND 3")
    toddlers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Age BETWEEN 4 AND 14")
    children = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Age BETWEEN 15 AND 19")
    teens = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Age BETWEEN 20 AND 25")
    young_adults = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Age BETWEEN 26 AND 59")
    adults = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Personal_Information WHERE Age >= 60")
    seniors = cursor.fetchone()[0]

    age_groups = [
        ("0–3",  "Toddler",     toddlers,    "#06b6d4", "#ecfeff"),
        ("4–14", "Child",       children,    "#10b981", "#ecfdf5"),
        ("15–19","Teen",        teens,       "#8b5cf6", "#f5f3ff"),
        ("20–25","Young Adult", young_adults,"#f59e0b", "#fffbeb"),
        ("26–59","Adult",       adults,      "#4353BD", "#eef0fb"),
        ("60+",  "Senior",      seniors,     "#ef4444", "#fef2f2"),
    ]

    # Section header row
    age_header = ctk.CTkFrame(dashboard, fg_color="transparent")
    age_header.pack(fill="x", padx=24, pady=(0, 6))

    ctk.CTkLabel(
        age_header,
        text="POPULATION BY AGE GROUP",
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        text_color="#9ca3af"
    ).pack(anchor="w")

    # Section card container
    section = ctk.CTkFrame(
        dashboard,
        corner_radius=20,
        fg_color="#ffffff",
        border_width=1,
        border_color="#e8eaf0"
    )
    section.pack(fill="x", padx=24, pady=(0, 28))

    section_inner = ctk.CTkFrame(section, fg_color="transparent")
    section_inner.pack(fill="x", padx=18, pady=18)

    age_grid = ctk.CTkFrame(section_inner, fg_color="transparent")
    age_grid.pack(fill="x")

    for i in range(3):
        age_grid.grid_columnconfigure(i, weight=1)

    # =========================================================
    # AGE CARD BUILDER
    # =========================================================
    def create_age_card(parent, range_txt, label, value, accent, tint, row, col):
        card = ctk.CTkFrame(
            parent,
            height=115,
            corner_radius=16,
            fg_color=tint,
            border_width=1,
            border_color="#e8eaf0"
        )
        card.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
        card.grid_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        # Range pill
        pill = ctk.CTkFrame(inner, fg_color=accent, corner_radius=8, height=22)
        pill.pack(anchor="w")
        pill.pack_propagate(False)
        ctk.CTkLabel(
            pill,
            text=f"  Age {range_txt}  ",
            font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
            text_color="#ffffff"
        ).pack(expand=True)

        ctk.CTkLabel(
            inner,
            text=label,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#6b7280"
        ).pack(anchor="w", pady=(6, 0))

        val_lbl = ctk.CTkLabel(
            inner,
            text="0",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#111827"
        )
        val_lbl.pack(anchor="w")
        animate_counter(val_lbl, value)

        # Hover
        def on_enter(e): card.configure(border_color=accent)
        def on_leave(e): card.configure(border_color="#e8eaf0")
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    for i, (range_txt, label, value, accent, tint) in enumerate(age_groups):
        create_age_card(age_grid, range_txt, label, value, accent, tint, i // 3, i % 3)

    conn.close()
    return dashboard