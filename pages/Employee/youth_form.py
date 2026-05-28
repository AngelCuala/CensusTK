import customtkinter as ctk
import tkinter as tk

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
    "border":      "#E5E7EB",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
}


def create_youth(parent):

    # ── Main container ────────────────────────────────────────
    youth_frame = ctk.CTkFrame(
        parent,
        fg_color=C["white"],
        corner_radius=12,
        border_width=1,
        border_color=C["green"]
    )

    # ── Header banner ─────────────────────────────────────────
    banner = ctk.CTkFrame(
        youth_frame,
        fg_color=C["green_soft"],
        corner_radius=0,
        height=50
    )
    banner.pack(fill="x")
    banner.pack_propagate(False)

    ctk.CTkFrame(
        banner,
        fg_color=C["green"],
        width=3,
        corner_radius=0
    ).pack(side="left", fill="y")

    b_inner = ctk.CTkFrame(
        banner,
        fg_color="transparent"
    )
    b_inner.pack(side="left", padx=12, pady=5)

    ctk.CTkLabel(
        b_inner,
        text="Youth-Specific Information",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=13,
            weight="bold"
        ),
        text_color=C["navy"]
    ).pack(anchor="w")

    ctk.CTkLabel(
        b_inner,
        text="Applicable for respondents aged 15–30 years old",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=9
        ),
        text_color=C["text_muted"]
    ).pack(anchor="w")

    # ── Helper: sub-section ───────────────────────────────────
    def sub_section(text, parent_w=youth_frame):

        section = ctk.CTkFrame(
            parent_w,
            fg_color=C["bg"],
            corner_radius=10
        )
        section.pack(fill="x", padx=14, pady=(10, 0))

        row = ctk.CTkFrame(
            section,
            fg_color="transparent",
            height=34
        )
        row.pack(fill="x", padx=12, pady=(8, 4))
        row.pack_propagate(False)

        ctk.CTkFrame(
            row,
            fg_color=C["accent"],
            width=3,
            corner_radius=2,
            height=18
        ).pack(side="left", padx=(0, 8), pady=6)

        ctk.CTkLabel(
            row,
            text=text,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=C["text_dark"]
        ).pack(side="left")

        return section

    # =========================================================
    # LAST GRADE COMPLETED
    # =========================================================
    grade_section = sub_section("Last Grade / Year Level Completed")

    grade_var = tk.StringVar()

    ctk.CTkEntry(
        grade_section,
        textvariable=grade_var,
        height=34,
        placeholder_text="e.g. Grade 12, 3rd Year College...",
        fg_color=C["white"],
        border_color=C["border"],
        border_width=1,
        text_color=C["text_dark"],
        font=ctk.CTkFont(
            family="Segoe UI",
            size=11
        )
    ).pack(fill="x", padx=12, pady=(0, 10))

    # =========================================================
    # CAUSE OF STOPPING
    # =========================================================
    cause_section = sub_section("Cause of Stopping School")

    cause_vars = {
        "Financial":  tk.IntVar(),
        "Family":     tk.IntVar(),
        "Work":       tk.IntVar(),
        "Others":     tk.IntVar(),
    }

    cause_grid = ctk.CTkFrame(
        cause_section,
        fg_color="transparent"
    )
    cause_grid.pack(anchor="w", padx=12, pady=(0, 10))

    for col, (cause, var) in enumerate(cause_vars.items()):

        ctk.CTkCheckBox(
            cause_grid,
            text=cause,
            variable=var,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=C["text_mid"],
            fg_color=C["accent"],
            hover_color=C["navy"]
        ).grid(
            row=0,
            column=col,
            sticky="w",
            padx=(0, 14),
            pady=2
        )

    # =========================================================
    # VOTER
    # =========================================================
    voter_section = sub_section("Voter Registration")

    voter_var = tk.StringVar()

    voter_row = ctk.CTkFrame(
        voter_section,
        fg_color="transparent"
    )
    voter_row.pack(anchor="w", padx=12, pady=(0, 10))

    for choice in ["Yes", "No"]:

        ctk.CTkRadioButton(
            voter_row,
            text=choice,
            variable=voter_var,
            value=choice,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=C["text_mid"],
            fg_color=C["accent"],
            hover_color=C["navy"]
        ).pack(side="left", padx=(0, 18))

    # =========================================================
    # STATUS
    # =========================================================
    status_section = sub_section("Current Status")

    ctk.CTkLabel(
        status_section,
        text="Select the option that best describes the youth's current situation:",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=9
        ),
        text_color=C["text_muted"]
    ).pack(anchor="w", padx=12, pady=(0, 6))

    status_var = tk.StringVar()

    status_options = [
        "Nag-aaral",
        "Kailanman di nag-aral",
        "Kasalukuyang elementarya",
        "Teenage Parent",
        "Out-of-School Youth",
        "Kasalukuyang High School",
        "Solo parent",
        "Nagtatrabaho",
        "Kasalukuyang kolehiyo",
        "Hindi nagtatrabaho",
        "PWD",
        "With ID",
        "No ID",
    ]

    status_grid = ctk.CTkFrame(
        status_section,
        fg_color="transparent"
    )
    status_grid.pack(anchor="w", padx=12, pady=(0, 10))

    for index, option in enumerate(status_options):

        row, col = divmod(index, 3)

        ctk.CTkRadioButton(
            status_grid,
            text=option,
            variable=status_var,
            value=option,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=C["text_mid"],
            fg_color=C["accent"],
            hover_color=C["navy"]
        ).grid(
            row=row,
            column=col,
            sticky="w",
            padx=(0, 14),
            pady=3
        )

    return youth_frame