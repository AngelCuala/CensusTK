import customtkinter as ctk
import tkinter as tk

# ── Shared palette ────────────────────────────────────────────
C = {
    "bg":          "#F0F2F9",
    "white":       "#FFFFFF",
    "navy":        "#1a2057",
    "accent":      "#4353BD",
    "accent_soft": "#EEF0FB",
    "border":      "#E5E7EB",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
}


def create_work_section(parent):

    form_frame = ctk.CTkFrame(
        parent,
        fg_color=C["white"],
        corner_radius=16
    )

    # ── Helper: compact section ───────────────────────────────
    def compact_box():
        box = ctk.CTkFrame(
            form_frame,
            fg_color=C["bg"],
            corner_radius=10
        )
        box.pack(fill="x", padx=20, pady=(0, 10))
        return box

    # ── Helper: field ─────────────────────────────────────────
    def field(parent_w, label, variable, hint=None):
        container = ctk.CTkFrame(parent_w, fg_color="transparent")
        container.pack(
            side="left",
            padx=(0, 12),
            pady=8,
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            container,
            text=label,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=C["text_mid"]
        ).pack(anchor="w")

        if hint:
            ctk.CTkLabel(
                container,
                text=hint,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=8
                ),
                text_color=C["text_muted"]
            ).pack(anchor="w", pady=(1, 2))

        ctk.CTkEntry(
            container,
            height=34,
            textvariable=variable,
            fg_color=C["white"],
            border_color=C["border"],
            border_width=1,
            text_color=C["text_dark"],
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            )
        ).pack(fill="x")

    # ── Helper: radio group ───────────────────────────────────
    def radio_group(label, variable, options):

        box = compact_box()

        ctk.CTkLabel(
            box,
            text=label,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=C["text_dark"]
        ).pack(anchor="w", padx=14, pady=(10, 4))

        opt_row = ctk.CTkFrame(
            box,
            fg_color="transparent"
        )
        opt_row.pack(anchor="w", padx=14, pady=(0, 10))

        for opt in options:
            ctk.CTkRadioButton(
                opt_row,
                text=opt,
                variable=variable,
                value=opt,
                text_color=C["text_mid"],
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=10
                ),
                fg_color=C["accent"],
                hover_color=C["navy"]
            ).pack(side="left", padx=(0, 16))

    # ── Compact section header ────────────────────────────────
    def sub_section(text):
        row = ctk.CTkFrame(
            form_frame,
            fg_color="transparent",
            height=28
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(10, 4)
        )

        row.pack_propagate(False)

        ctk.CTkFrame(
            row,
            fg_color=C["accent"],
            width=3,
            corner_radius=2
        ).pack(side="left", fill="y", padx=(0, 8))

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

    # =========================================================
    # WORKPLACE + SALARY
    # =========================================================
    sub_section("Employment Details")

    top_box = compact_box()

    top_row = ctk.CTkFrame(
        top_box,
        fg_color="transparent"
    )

    top_row.pack(
        fill="x",
        padx=12,
        pady=4
    )

    workplace_var = tk.StringVar()
    salary_var    = tk.StringVar()

    field(
        top_row,
        "Workplace Name",
        workplace_var,
        hint="Company or establishment name"
    )

    field(
        top_row,
        "Monthly Salary (PHP)",
        salary_var,
        hint="Approximate gross amount"
    )

    # =========================================================
    # UNDEREMPLOYED
    # =========================================================
    underemp_var = tk.StringVar()

    sub_section("Underemployment")

    radio_group(
        "If Underemployed — Reason",
        underemp_var,
        [
            "Low Salary",
            "Part-time",
            "Unrelated to Degree",
            "Others"
        ]
    )

    # =========================================================
    # UNEMPLOYED
    # =========================================================
    unemp_var = tk.StringVar()

    sub_section("Unemployment")

    radio_group(
        "For the Unemployed — Reason",
        unemp_var,
        [
            "No Work",
            "Lack of Skills",
            "Lack of Credibility",
            "Unfinished Education"
        ]
    )

    # =========================================================
    # PESO PROGRAM
    # =========================================================
    sub_section("PESO Interest")

    goback_var = tk.StringVar()

    peso_box = ctk.CTkFrame(
        form_frame,
        fg_color=C["accent_soft"],
        corner_radius=10
    )

    peso_box.pack(
        fill="x",
        padx=20,
        pady=(0, 14)
    )

    ctk.CTkLabel(
        peso_box,
        text="📋 PESO Interest",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=11,
            weight="bold"
        ),
        text_color=C["accent"]
    ).pack(anchor="w", padx=14, pady=(10, 2))

    ctk.CTkLabel(
        peso_box,
        text="Interesado ka bang makilahok sa mga local employment o livelihood program ng PESO?",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=10
        ),
        text_color=C["text_mid"],
        justify="left",
        wraplength=500
    ).pack(anchor="w", padx=14)

    peso_opts = ctk.CTkFrame(
        peso_box,
        fg_color="transparent"
    )

    peso_opts.pack(
        anchor="w",
        padx=14,
        pady=(6, 10)
    )

    for opt in ["Oo", "Hindi"]:
        ctk.CTkRadioButton(
            peso_opts,
            text=opt,
            variable=goback_var,
            value=opt,
            text_color=C["text_mid"],
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            fg_color=C["accent"],
            hover_color=C["navy"]
        ).pack(side="left", padx=(0, 16))

    return form_frame