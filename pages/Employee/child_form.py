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
    "sky":         "#0EA5E9",
    "sky_soft":    "#F0F9FF",
    "border":      "#E5E7EB",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
}


def create_child(parent):

    # ── Main container ────────────────────────────────────────
    child_frame = ctk.CTkFrame(
        parent,
        fg_color=C["white"],
        corner_radius=12,
        border_width=1,
        border_color=C["sky"]
    )

    # ── Header banner ─────────────────────────────────────────
    banner = ctk.CTkFrame(
        child_frame,
        fg_color=C["sky_soft"],
        corner_radius=0,
        height=50
    )

    banner.pack(fill="x")
    banner.pack_propagate(False)

    ctk.CTkFrame(
        banner,
        fg_color=C["sky"],
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
        text="Child Profiling",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=13,
            weight="bold"
        ),
        text_color=C["navy"]
    ).pack(anchor="w")

    ctk.CTkLabel(
        b_inner,
        text="Applicable for children aged 0–4 years old",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=9
        ),
        text_color=C["text_muted"]
    ).pack(anchor="w")

    # ── Body ─────────────────────────────────────────────────
    body = ctk.CTkFrame(
        child_frame,
        fg_color="transparent"
    )

    body.pack(fill="x", padx=14, pady=10)

    # ── Helpers ───────────────────────────────────────────────
    def sub_section(text, parent_w=body):

        section = ctk.CTkFrame(
            parent_w,
            fg_color=C["bg"],
            corner_radius=10
        )

        section.pack(fill="x", pady=(8, 0))

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

    def radio_row(parent_w, variable, options):

        row = ctk.CTkFrame(
            parent_w,
            fg_color="transparent"
        )

        row.pack(anchor="w", padx=12, pady=(0, 10))

        for opt in options:

            ctk.CTkRadioButton(
                row,
                text=opt,
                variable=variable,
                value=opt,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=10
                ),
                text_color=C["text_mid"],
                fg_color=C["accent"],
                hover_color=C["navy"]
            ).pack(side="left", padx=(0, 18))

    def divider():

        ctk.CTkFrame(
            body,
            fg_color=C["border"],
            height=1
        ).pack(fill="x", pady=(8, 4))

    # =========================================================
    # BIRTH CERTIFICATE
    # =========================================================
    bc_section = sub_section("Does the child have a birth certificate?")

    bc_var = tk.StringVar()

    radio_row(
        bc_section,
        bc_var,
        ["Yes", "No"]
    )

    # =========================================================
    # IMMUNIZATION STATUS
    # =========================================================
    immu_section = sub_section("Immunization Status")

    immu_var = tk.StringVar()

    radio_row(
        immu_section,
        immu_var,
        ["Complete", "Incomplete", "Unknown"]
    )

    # =========================================================
    # STUDYING
    # =========================================================
    study_section = sub_section("Is the child currently studying?")

    study_var = tk.StringVar()

    radio_row(
        study_section,
        study_var,
        ["Yes", "No"]
    )

    # =========================================================
    # SCHOOL INFO
    # =========================================================
    school_section = sub_section("School Information (if applicable)")

    school_row = ctk.CTkFrame(
        school_section,
        fg_color="transparent"
    )

    school_row.pack(fill="x", padx=12, pady=(0, 10))

    school_var = tk.StringVar()
    level_var  = tk.StringVar()

    for label, var, hint in [
        ("Name of School", school_var, "e.g. Luisiana Elementary School"),
        ("Grade Level", level_var, "e.g. Nursery, Kinder"),
    ]:

        col = ctk.CTkFrame(
            school_row,
            fg_color="transparent"
        )

        col.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkLabel(
            col,
            text=label,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold"
            ),
            text_color=C["text_mid"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            col,
            text=hint,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=8
            ),
            text_color=C["text_muted"]
        ).pack(anchor="w", pady=(1, 2))

        ctk.CTkEntry(
            col,
            textvariable=var,
            height=34,
            fg_color=C["white"],
            border_color=C["border"],
            border_width=1,
            text_color=C["text_dark"],
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            )
        ).pack(fill="x")

    # =========================================================
    # HEALTH PROBLEM
    # =========================================================
    health_section = sub_section("May problema sa kalusugan")

    health_var = tk.StringVar()

    ctk.CTkEntry(
        health_section,
        textvariable=health_var,
        height=34,
        placeholder_text="Ilarawan ang problema sa kalusugan, kung mayroon...",
        fg_color=C["white"],
        border_color=C["border"],
        border_width=1,
        text_color=C["text_dark"],
        font=ctk.CTkFont(
            family="Segoe UI",
            size=10
        )
    ).pack(fill="x", padx=12, pady=(0, 10))

    # Bottom padding
    ctk.CTkFrame(
        child_frame,
        fg_color="transparent",
        height=6
    ).pack()

    return child_frame