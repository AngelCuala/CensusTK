import customtkinter as ctk
from db import connect_db

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Shared palette ────────────────────────────────────────────
C = {
    "bg":          "#F0F2F9",
    "white":       "#FFFFFF",
    "navy":        "#1a2057",
    "accent":      "#4353BD",
    "accent_soft": "#EEF0FB",
    "amber":       "#F59E0B",
    "amber_soft":  "#FFFBEB",
    "green":       "#10B981",
    "green_soft":  "#ECFDF5",
    "purple":      "#8B5CF6",
    "purple_soft": "#F5F3FF",
    "border":      "#E5E7EB",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
    "success":     "#16a34a",
}


def create_dashboard_employee(parent, current_user=None):

    dashboard = ctk.CTkScrollableFrame(parent, fg_color=C["bg"])

    # ── DB queries ────────────────────────────────────────────
    conn   = connect_db()
    cursor = conn.cursor(dictionary=True)

    uid = None
    if current_user:
        for key in ("User_ID", "user_id", "id", "ID", "UserID"):
            if key in current_user:
                uid = current_user[key]
                break

    team = None
    members = 0
    leader_name = "N/A"

    if uid:
        cursor.execute("""
            SELECT t.Team_ID, t.Team_Name, t.Barangay, t.Status
            FROM teams t
            JOIN team_members tm ON t.Team_ID = tm.Team_ID
            WHERE tm.User_ID = %s LIMIT 1
        """, (uid,))
        team = cursor.fetchone()

    if team:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM team_members WHERE Team_ID = %s",
            (team["Team_ID"],)
        )
        members = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT a.First_Name, a.Last_Name
            FROM team_members tm
            JOIN accounts a ON tm.User_ID = a.User_ID
            WHERE tm.Team_ID = %s AND tm.Role = 'Leader' LIMIT 1
        """, (team["Team_ID"],))
        lrow = cursor.fetchone()
        if lrow:
            leader_name = f"{lrow['First_Name']} {lrow['Last_Name']}"

    cursor.execute("SELECT COUNT(*) AS total FROM responders")
    total_surveys = cursor.fetchone()["total"]

    # ── Only fetch surveys submitted within the last hour ──
    cursor.execute("""
        SELECT pi.First_Name, pi.Last_Name, pi.Street_Name, r.Date_Of_Interview
        FROM responders r
        JOIN Personal_Information pi ON r.Respondent_ID = pi.Respondent_ID
        WHERE r.Date_Of_Interview >= NOW() - INTERVAL 1 HOUR
        ORDER BY r.Date_Of_Interview DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()
    cursor.close()
    conn.close()

    if team:
        for key in team:
            if team[key] is None:
                team[key] = "N/A"

    # =========================================================
    # HELPER — section card
    # =========================================================
    def make_card(parent_widget, title=None, pady_top=20):
        outer = ctk.CTkFrame(
            parent_widget,
            fg_color=C["white"],
            corner_radius=20
        )
        outer.pack(fill="x", padx=30, pady=(pady_top, 0))

        if title:
            header_row = ctk.CTkFrame(outer, fg_color="transparent")
            header_row.pack(fill="x", padx=24, pady=(20, 0))

            # Accent dot
            ctk.CTkFrame(
                header_row,
                width=6, height=6,
                corner_radius=3,
                fg_color=C["accent"]
            ).pack(side="left", padx=(0, 8))

            ctk.CTkLabel(
                header_row,
                text=title,
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color=C["text_dark"]
            ).pack(side="left")

            # Thin divider
            ctk.CTkFrame(outer, fg_color=C["border"], height=1).pack(
                fill="x", padx=24, pady=(10, 0)
            )

        body = ctk.CTkFrame(outer, fg_color="transparent")
        body.pack(fill="x", padx=24, pady=18)
        return body

    # =========================================================
    # HEADER
    # =========================================================
    hero = ctk.CTkFrame(dashboard, fg_color=C["navy"], corner_radius=0, height=100)
    hero.pack(fill="x")
    hero.pack_propagate(False)

    # Left stripe
    ctk.CTkFrame(hero, fg_color=C["amber"], width=5, corner_radius=0).pack(
        side="left", fill="y"
    )

    hero_inner = ctk.CTkFrame(hero, fg_color="transparent")
    hero_inner.pack(side="left", fill="both", expand=True, padx=28, pady=0)

    fname = (current_user.get("First_Name", "") if current_user else "")
    ctk.CTkLabel(
        hero_inner,
        text=f"Welcome back, {fname} 👋" if fname else "Dashboard",
        font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        text_color=C["white"]
    ).pack(anchor="w", pady=(22, 2))

    ctk.CTkLabel(
        hero_inner,
        text="Survey Monitoring Overview  •  Census Management System",
        font=ctk.CTkFont(family="Segoe UI", size=11),
        text_color="#8b9fd4"
    ).pack(anchor="w")

    # =========================================================
    # STAT CARDS
    # =========================================================
    stats_row = ctk.CTkFrame(dashboard, fg_color="transparent")
    stats_row.pack(fill="x", padx=30, pady=20)
    stats_row.grid_columnconfigure(0, weight=1)
    stats_row.grid_columnconfigure(1, weight=1)
    stats_row.grid_columnconfigure(2, weight=1)

    card_data = [
        ("📋", "Total Surveys",  str(total_surveys), C["accent"],  C["accent_soft"]),
        ("👥", "Team Members",   str(members),       C["green"],   C["green_soft"]),
        ("📍", "Barangay",       team["Barangay"] if team else "No Team",
                                                     C["purple"],  C["purple_soft"]),
    ]

    for col, (icon, title, value, color, soft) in enumerate(card_data):
        card = ctk.CTkFrame(stats_row, fg_color=C["white"], corner_radius=18)
        card.grid(row=0, column=col, padx=8, pady=4, sticky="ew")

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x", padx=20, pady=18)

        # Icon pill
        icon_pill = ctk.CTkFrame(body, fg_color=soft, corner_radius=12, width=48, height=48)
        icon_pill.pack(anchor="w")
        icon_pill.pack_propagate(False)
        ctk.CTkLabel(icon_pill, text=icon, font=ctk.CTkFont(size=20)).place(
            relx=0.5, rely=0.5, anchor="center"
        )

        ctk.CTkLabel(
            body,
            text=value,
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=C["text_dark"],
            wraplength=160, anchor="w", justify="left"
        ).pack(anchor="w", pady=(10, 2))

        ctk.CTkLabel(
            body,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text_muted"],
            anchor="w"
        ).pack(anchor="w")

        # Bottom color bar
        ctk.CTkFrame(card, fg_color=color, height=4, corner_radius=0).pack(
            fill="x", side="bottom"
        )

    # =========================================================
    # TEAM INFORMATION
    # =========================================================
    team_body = make_card(dashboard, "My Team")

    if not team:
        notice = ctk.CTkFrame(team_body, fg_color=C["accent_soft"], corner_radius=12)
        notice.pack(fill="x")
        ctk.CTkLabel(
            notice,
            text="🔔  You have not been assigned to a team yet.\n"
                 "Contact your administrator to get assigned.",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=C["accent"],
            justify="left"
        ).pack(anchor="w", padx=16, pady=14)
    else:
        rows_data = [
            ("🏷️", "Team Name", team["Team_Name"]),
            ("📍", "Barangay",   team["Barangay"]),
            ("👑", "Leader",     leader_name),
            ("📌", "Status",     team.get("Status", "N/A")),
        ]

        grid = ctk.CTkFrame(team_body, fg_color="transparent")
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        for i, (icon, label, value) in enumerate(rows_data):
            r, c = divmod(i, 2)
            cell = ctk.CTkFrame(
                grid, fg_color=C["bg"], corner_radius=12
            )
            cell.grid(row=r, column=c, padx=6, pady=5, sticky="ew")

            inner = ctk.CTkFrame(cell, fg_color="transparent")
            inner.pack(fill="x", padx=14, pady=12)

            ctk.CTkLabel(
                inner,
                text=f"{icon}  {label}",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=C["text_muted"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                inner,
                text=value,
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                text_color=C["text_dark"],
                wraplength=220, anchor="w", justify="left"
            ).pack(anchor="w", pady=(3, 0))

    # =========================================================
    # RECENT ACTIVITY  (last hour only)
    # =========================================================
    activity_body = make_card(dashboard, "Recent Survey Activity  •  Last Hour", pady_top=16)

    # Bottom padding
    ctk.CTkFrame(dashboard, fg_color="transparent", height=30).pack()

    if not recent:
        notice = ctk.CTkFrame(activity_body, fg_color=C["bg"], corner_radius=12)
        notice.pack(fill="x")
        ctk.CTkLabel(
            notice,
            text="No surveys submitted in the last hour.",
            font=ctk.CTkFont(size=13),
            text_color=C["text_muted"]
        ).pack(padx=16, pady=16)
    else:
        for idx, row in enumerate(recent):
            item = ctk.CTkFrame(
                activity_body,
                fg_color=C["bg"],
                corner_radius=14
            )
            item.pack(fill="x", pady=(0, 8))

            left_bar = ctk.CTkFrame(item, fg_color=C["accent"], width=4, corner_radius=2)
            left_bar.pack(side="left", fill="y", padx=(0, 0))

            info = ctk.CTkFrame(item, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=14, pady=12)

            fullname = f"{row['First_Name']} {row['Last_Name']}"

            ctk.CTkLabel(
                info,
                text=fullname,
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                text_color=C["text_dark"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"📍 {row['Street_Name']}",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=C["text_mid"]
            ).pack(anchor="w", pady=(2, 0))

            date_lbl = ctk.CTkLabel(
                item,
                text=f"🗓️ {row['Date_Of_Interview']}",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=C["text_muted"]
            )
            date_lbl.pack(side="right", padx=16)

    return dashboard