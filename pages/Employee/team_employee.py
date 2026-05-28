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
    "amber_border":"#FDE68A",
    "green":       "#10B981",
    "border":      "#E5E7EB",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
}


def create_team_employee(parent, current_user=None):

    page = ctk.CTkFrame(parent, fg_color=C["bg"])

    # ── Hero banner ───────────────────────────────────────────
    hero = ctk.CTkFrame(page, fg_color=C["navy"], corner_radius=0, height=100)
    hero.pack(fill="x")
    hero.pack_propagate(False)

    ctk.CTkFrame(hero, fg_color=C["amber"], width=5, corner_radius=0).pack(
        side="left", fill="y"
    )
    hero_inner = ctk.CTkFrame(hero, fg_color="transparent")
    hero_inner.pack(side="left", padx=28, pady=0)

    ctk.CTkLabel(
        hero_inner,
        text="Teams",
        font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        text_color=C["white"]
    ).pack(anchor="w", pady=(22, 2))

    ctk.CTkLabel(
        hero_inner,
        text="View your team and all active census survey teams",
        font=ctk.CTkFont(family="Segoe UI", size=11),
        text_color="#8b9fd4"
    ).pack(anchor="w")

    # ── Scroll area ───────────────────────────────────────────
    scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=30, pady=20)

    # =========================================================
    # TEAM DETAIL POPUP
    # =========================================================
    def show_team_detail(team_id, team_name, barangay):
        win = ctk.CTkToplevel()
        win.title(team_name)
        win.geometry("500x580")
        win.resizable(False, False)
        win.grab_set()
        win.focus_force()
        win.configure(fg_color=C["bg"])

        header = ctk.CTkFrame(win, fg_color=C["navy"], corner_radius=0)
        header.pack(fill="x")
        ctk.CTkFrame(header, fg_color=C["amber"], width=5, corner_radius=0).pack(
            side="left", fill="y"
        )
        h_inner = ctk.CTkFrame(header, fg_color="transparent")
        h_inner.pack(side="left", padx=20, pady=18)
        ctk.CTkLabel(
            h_inner, text=team_name,
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=C["white"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            h_inner, text=f"📍  {barangay}",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#c7d2fe"
        ).pack(anchor="w", pady=(4, 0))

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.First_Name, a.Last_Name, tm.Role
            FROM team_members tm
            JOIN accounts a ON tm.User_ID = a.User_ID
            WHERE tm.Team_ID = %s
            ORDER BY FIELD(tm.Role, 'Leader', 'Member')
        """, (team_id,))
        members = cursor.fetchall()
        conn.close()

        ctk.CTkLabel(
            header,
            text=f"  {len(members)} members  ",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=C["accent"], text_color=C["white"], corner_radius=8
        ).pack(side="right", padx=20, pady=20)

        scroll_area = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll_area.pack(fill="both", expand=True, padx=20, pady=15)

        if not members:
            ctk.CTkLabel(
                scroll_area, text="No members yet.",
                font=ctk.CTkFont(size=14), text_color=C["text_muted"]
            ).pack(pady=30)
        else:
            for m in members:
                fullname  = f"{m['First_Name']} {m['Last_Name']}"
                is_leader = m["Role"] == "Leader"

                row = ctk.CTkFrame(
                    scroll_area,
                    fg_color=C["amber_soft"] if is_leader else C["white"],
                    corner_radius=14, border_width=1,
                    border_color=C["amber_border"] if is_leader else C["border"]
                )
                row.pack(fill="x", pady=5)

                avatar = ctk.CTkFrame(
                    row, width=42, height=42, corner_radius=21,
                    fg_color=C["amber"] if is_leader else C["accent_soft"]
                )
                avatar.pack(side="left", padx=14, pady=14)
                avatar.pack_propagate(False)
                ctk.CTkLabel(
                    avatar, text="👑" if is_leader else "👤",
                    font=ctk.CTkFont(size=18)
                ).place(relx=0.5, rely=0.5, anchor="center")

                info = ctk.CTkFrame(row, fg_color="transparent")
                info.pack(side="left", fill="both", expand=True, pady=14)
                ctk.CTkLabel(
                    info, text=fullname,
                    font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                    text_color=C["text_dark"]
                ).pack(anchor="w")
                ctk.CTkLabel(
                    info,
                    text="Team Leader" if is_leader else "Member",
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    text_color=C["amber"] if is_leader else C["text_muted"]
                ).pack(anchor="w", pady=(2, 0))

        ctk.CTkButton(
            win, text="Close",
            fg_color=C["accent"], hover_color=C["navy"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=10, height=40, command=win.destroy
        ).pack(pady=(0, 18), padx=20, fill="x")

    # =========================================================
    # BUILD A TEAM CARD
    # =========================================================
    def build_card(parent_frame, team, is_my_team, leader_name, member_count):
        card = ctk.CTkFrame(
            parent_frame, corner_radius=18,
            fg_color=C["amber_soft"] if is_my_team else C["white"],
            border_width=2 if is_my_team else 1,
            border_color=C["amber"] if is_my_team else C["border"],
            cursor="hand2"
        )
        card.pack(fill="x", pady=6)

        ctk.CTkFrame(
            card, fg_color=C["amber"] if is_my_team else C["accent"],
            width=5, corner_radius=0
        ).pack(side="left", fill="y")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(side="left", fill="both", expand=True, padx=16, pady=16)

        title_row = ctk.CTkFrame(inner, fg_color="transparent")
        title_row.pack(anchor="w")

        ctk.CTkLabel(
            title_row, text=team["Team_Name"],
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=C["text_dark"]
        ).pack(side="left")

        if is_my_team:
            ctk.CTkLabel(
                title_row, text="  ★ Your Team",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=C["amber"]
            ).pack(side="left", padx=(8, 0))

        ctk.CTkLabel(
            inner, text=f"📍  {team['Barangay']}",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text_muted"]
        ).pack(anchor="w", pady=(4, 0))

        meta_row = ctk.CTkFrame(inner, fg_color="transparent")
        meta_row.pack(anchor="w", pady=(6, 0))

        ctk.CTkLabel(
            meta_row, text=f"👑  {leader_name}",
            fg_color=C["amber_soft"] if is_my_team else C["accent_soft"],
            text_color=C["amber"] if is_my_team else C["accent"],
            font=ctk.CTkFont(family="Segoe UI", size=11),
            corner_radius=6, padx=8, pady=3
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            meta_row, text=f"👥  {member_count} members",
            fg_color=C["bg"], text_color=C["text_mid"],
            font=ctk.CTkFont(family="Segoe UI", size=11),
            corner_radius=6, padx=8, pady=3
        ).pack(side="left")

        ctk.CTkLabel(
            card, text=" › ", font=ctk.CTkFont(size=24),
            text_color=C["text_muted"]
        ).pack(side="right", padx=16)

        def on_click(e, t=team["Team_ID"], tn=team["Team_Name"], br=team["Barangay"]):
            show_team_detail(t, tn, br)

        for widget in [card, inner, title_row, meta_row]:
            widget.bind("<Button-1>", on_click)

    # =========================================================
    # LOAD TEAMS
    # =========================================================
    def load_teams():

        for w in scroll.winfo_children():
            w.destroy()

        # =====================================================
        # GET USER ID
        # =====================================================

        uid = None


        print("CURRENT USER:", current_user)
        print("UID:", uid)

        # =====================================================
        # DATABASE
        # =====================================================

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        # =====================================================
        # GET USER TEAM IDS
        # =====================================================

        my_team_ids = []

        if uid:

            cursor.execute("""
                SELECT Team_ID
                FROM team_members
                WHERE User_ID = %s
            """, (uid,))

            rows = cursor.fetchall()

            my_team_ids = [r["Team_ID"] for r in rows]

        print("MY TEAM IDS:", my_team_ids)

        # =====================================================
        # GET ALL TEAMS
        # =====================================================

        cursor.execute("""
            SELECT
                t.Team_ID,
                t.Team_Name,
                t.Barangay,
                t.Status,

                COALESCE(
                    CONCAT(a.First_Name, ' ', a.Last_Name),
                    'No Leader'
                ) AS Leader_Name

            FROM teams t

            LEFT JOIN accounts a
                ON t.Leader_ID = a.User_ID

            ORDER BY t.Team_ID ASC
        """)

        all_teams = cursor.fetchall()

        # =====================================================
        # GET MEMBER COUNTS
        # =====================================================

        cursor.execute("""
            SELECT
                Team_ID,
                COUNT(*) AS cnt
            FROM team_members
            GROUP BY Team_ID
        """)

        counts = {
            r["Team_ID"]: r["cnt"]
            for r in cursor.fetchall()
        }

        conn.close()

        # =====================================================
        # SPLIT TEAMS
        # =====================================================

        my_teams = []
        other_teams = []

        for t in all_teams:

            if t["Team_ID"] in my_team_ids:
                my_teams.append(t)
            else:
                other_teams.append(t)

        # =====================================================
        # MY TEAMS
        # =====================================================

        if my_teams:

            section_label(
                scroll,
                "🏅  My Team",
                C["accent"]
            )

            for t in my_teams:

                build_card(
                    scroll,
                    t,
                    is_my_team=True,
                    leader_name=t["Leader_Name"],
                    member_count=counts.get(t["Team_ID"], 0)
                )

        else:

            no_team = ctk.CTkFrame(
                scroll,
                fg_color=C["white"],
                corner_radius=14,
                border_width=1,
                border_color=C["border"]
            )

            no_team.pack(fill="x", pady=6)

            ctk.CTkLabel(
                no_team,
                text="🔔  You have not been assigned to a team yet.",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13
                ),
                text_color=C["text_muted"]
            ).pack(padx=20, pady=20)

        # =====================================================
        # ALL TEAMS
        # =====================================================

        if other_teams:

            section_label(
                scroll,
                "All Teams",
                C["text_mid"]
            )

            for t in other_teams:

                build_card(
                    scroll,
                    t,
                    is_my_team=False,
                    leader_name=t["Leader_Name"],
                    member_count=counts.get(t["Team_ID"], 0)
                )

    def section_label(parent_w, text, color):
        ctk.CTkLabel(
            parent_w, text=text,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=color
        ).pack(anchor="w", pady=(14, 4))

    load_teams()
    return page