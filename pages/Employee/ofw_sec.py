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
    "border":      "#E5E7EB",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
}


def create_ofw_section(parent):

    # ── Main container ────────────────────────────────────────
    form_frame = ctk.CTkFrame(
        parent,
        fg_color=C["white"],
        corner_radius=12,
        border_width=1,
        border_color=C["amber"]
    )

    # ── Header banner ─────────────────────────────────────────
    banner = ctk.CTkFrame(
        form_frame,
        fg_color=C["amber_soft"],
        corner_radius=0,
        height=50
    )

    banner.pack(fill="x")
    banner.pack_propagate(False)

    ctk.CTkFrame(
        banner,
        fg_color=C["amber"],
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
        text="Para sa mga OFW",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=13,
            weight="bold"
        ),
        text_color=C["navy"]
    ).pack(anchor="w")

    ctk.CTkLabel(
        b_inner,
        text="Overseas Filipino Worker information",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=9
        ),
        text_color=C["text_muted"]
    ).pack(anchor="w")

    # ── Body ─────────────────────────────────────────────────
    body = ctk.CTkFrame(
        form_frame,
        fg_color="transparent"
    )

    body.pack(fill="x", padx=14, pady=10)

    # ── Helper: section box ──────────────────────────────────
    def section_box(title):

        section = ctk.CTkFrame(
            body,
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
            text=title,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            ),
            text_color=C["text_dark"]
        ).pack(side="left")

        return section

    # =========================================================
    # OFW STATUS
    # =========================================================
    status_section = section_box("OFW Status")

    ofw_var = tk.StringVar()

    status_row = ctk.CTkFrame(
        status_section,
        fg_color="transparent"
    )

    status_row.pack(anchor="w", padx=12, pady=(0, 10))

    for opt in ["Kasalukuyang OFW", "Dating OFW"]:

        ctk.CTkRadioButton(
            status_row,
            text=opt,
            variable=ofw_var,
            value=opt,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            ),
            text_color=C["text_mid"],
            fg_color=C["accent"],
            hover_color=C["navy"]
        ).pack(side="left", padx=(0, 18))

    # =========================================================
    # OFW DETAILS
    # =========================================================
    details_section = section_box("OFW Details")

    fields_row = ctk.CTkFrame(
        details_section,
        fg_color="transparent"
    )

    fields_row.pack(fill="x", padx=12, pady=(0, 10))

    def make_field(parent_w, label, hint=None):

        container = ctk.CTkFrame(
            parent_w,
            fg_color="transparent"
        )

        container.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
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
            fg_color=C["white"],
            border_color=C["border"],
            border_width=1,
            text_color=C["text_dark"],
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10
            )
        ).pack(fill="x")

    make_field(
        fields_row,
        "Bansa kung saan nagtrabaho",
        hint="e.g. Saudi Arabia, Japan"
    )

    make_field(
        fields_row,
        "Uri ng trabaho sa abroad",
        hint="e.g. Domestic Worker, Engineer"
    )

    make_field(
        fields_row,
        "Panahon ng kontrata",
        hint="e.g. 2 taon, 6 buwan"
    )

    # Bottom spacing
    ctk.CTkFrame(
        form_frame,
        fg_color="transparent",
        height=6
    ).pack()

    return form_frame