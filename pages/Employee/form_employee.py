import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

from pages.Employee.youth_form import create_youth
from pages.Employee.child_form import create_child
from pages.Employee.ofw_sec import create_ofw_section
from pages.Employee.work_sec import create_work_section

from db import connect_db

C = {
    "bg":          "#F0F2F9",
    "white":       "#FFFFFF",
    "navy":        "#1a2057",
    "accent":      "#4353BD",
    "accent_soft": "#EEF0FB",
    "amber":       "#F59E0B",
    "amber_soft":  "#FFFBEB",
    "border":      "#E5E7EB",
    "border_focus":"#4353BD",
    "error":       "#dc2626",
    "text_dark":   "#111827",
    "text_mid":    "#374151",
    "text_muted":  "#9CA3AF",
}


def create_form_employee(parent):

    frame = ctk.CTkScrollableFrame(parent, fg_color=C["bg"])

    # ── Hero banner ───────────────────────────────────────────
    hero = ctk.CTkFrame(
        frame,
        fg_color=C["navy"],
        corner_radius=0,
        height=60
    )
    hero.pack(side="top", fill="x")
    hero.pack_propagate(False)

    ctk.CTkFrame(
        hero,
        fg_color=C["amber"],
        width=5,
        corner_radius=0
    ).pack(side="left", fill="y")

    h_inner = ctk.CTkFrame(hero, fg_color="transparent")
    h_inner.pack(side="left", padx=14, pady=6)

    ctk.CTkLabel(
        h_inner,
        text="Add Resident",
        font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        text_color=C["white"]
    ).pack(anchor="w")

    ctk.CTkLabel(
        h_inner,
        text="Fill in the respondent's information — all required fields are marked",
        font=ctk.CTkFont(family="Segoe UI", size=9),
        text_color="#8b9fd4"
    ).pack(anchor="w")

    # ── Content container ─────────────────────────────────────
    content = ctk.CTkFrame(frame, fg_color="transparent")
    content.pack(fill="x", padx=20, pady=6)

    # =========================================================
    # HELPERS
    # =========================================================

    def make_card(parent_w, title, subtitle=None):
        card = ctk.CTkFrame(parent_w, fg_color=C["white"], corner_radius=10)
        card.pack(fill="x", pady=(0, 3))
        card.pack_propagate(True)

        title_row = ctk.CTkFrame(card, fg_color="transparent", height=40)
        title_row.pack(fill="x", padx=10, pady=(4, 0))
        title_row.pack_propagate(False)

        ctk.CTkFrame(title_row, fg_color=C["accent"], width=3, corner_radius=2).pack(
            side="left", fill="y", padx=(0, 6)
        )

        t_text = ctk.CTkFrame(title_row, fg_color="transparent")
        t_text.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            t_text, text=title,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=C["text_dark"]
        ).pack(anchor="w")

        if subtitle:
            ctk.CTkLabel(
                t_text, text=subtitle,
                font=ctk.CTkFont(family="Segoe UI", size=8),
                text_color=C["text_muted"]
            ).pack(anchor="w")

        ctk.CTkFrame(card, fg_color=C["border"], height=1).pack(fill="x", padx=10, pady=(2, 2))

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x", padx=10, pady=(0, 4))

        return body

    def make_entry(parent_w, label, var, hint=None, required=False, show=None,
                   side=None, expand=True, padx_right=0):
        container = ctk.CTkFrame(parent_w, fg_color="transparent")
        if side:
            container.pack(side=side, fill="x", expand=expand, padx=(0, padx_right), pady=(0, 2))
        else:
            container.pack(fill="x", pady=(0, 2))
        lbl_row = ctk.CTkFrame(container, fg_color="transparent")
        lbl_row.pack(anchor="w")
        ctk.CTkLabel(lbl_row, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=C["text_mid"]).pack(side="left")
        if required:
            ctk.CTkLabel(lbl_row, text="  *",
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                text_color=C["error"]).pack(side="left")
        if hint:
            ctk.CTkLabel(container, text=hint,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=C["text_muted"]).pack(anchor="w", pady=(1, 2))
        e = ctk.CTkEntry(container, textvariable=var, height=32,
            fg_color=C["bg"], border_color=C["border"], border_width=1,
            text_color=C["text_dark"], font=ctk.CTkFont(family="Segoe UI", size=11))
        if show:
            e.configure(show=show)
        e.pack(fill="x", pady=(2, 0))
        return e

    def make_combo(parent_w, label, var, values, hint=None, required=False, width=None):
        container = ctk.CTkFrame(parent_w, fg_color="transparent")
        container.pack(fill="x", pady=(0, 2))
        lbl_row = ctk.CTkFrame(container, fg_color="transparent")
        lbl_row.pack(anchor="w")
        ctk.CTkLabel(lbl_row, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=C["text_mid"]).pack(side="left")
        if required:
            ctk.CTkLabel(lbl_row, text="  *",
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                text_color=C["error"]).pack(side="left")
        if hint:
            ctk.CTkLabel(container, text=hint,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=C["text_muted"]).pack(anchor="w", pady=(1, 2))
        kw = {"width": width} if width else {}
        cb = ctk.CTkComboBox(container, variable=var, values=values, state="readonly",
            height=32, fg_color=C["bg"], border_color=C["border"], border_width=1,
            text_color=C["text_dark"], font=ctk.CTkFont(family="Segoe UI", size=11),
            button_color=C["accent"], dropdown_fg_color=C["white"], **kw)
        cb.pack(fill="x" if not width else None, anchor="w", pady=(2, 0))
        return cb

    def make_date_field(parent_w, label, var, required=False,
                        side=None, expand=True, padx_right=0, maxdate=None):
        container = ctk.CTkFrame(parent_w, fg_color="transparent")
        if side:
            container.pack(side=side, fill="x", expand=expand, padx=(0, padx_right), pady=(0, 2))
        else:
            container.pack(fill="x", pady=(0, 2))
        lbl_row = ctk.CTkFrame(container, fg_color="transparent")
        lbl_row.pack(anchor="w")
        ctk.CTkLabel(lbl_row, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=C["text_mid"]).pack(side="left")
        if required:
            ctk.CTkLabel(lbl_row, text="  *",
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                text_color=C["error"]).pack(side="left")
        kw = {"maxdate": maxdate} if maxdate else {}
        de = DateEntry(container, textvariable=var, date_pattern="yyyy-mm-dd",
            font=("Segoe UI", 11), background="#1a2057", foreground="white",
            borderwidth=1, **kw)
        de.pack(fill="x", ipadx=10, ipady=4, pady=(2, 0))
        return de

    def make_radio_group(parent_w, label, var, options, hint=None):
        container = ctk.CTkFrame(parent_w, fg_color="transparent")
        container.pack(fill="x", pady=(0, 2))
        ctk.CTkLabel(container, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=C["text_mid"]).pack(anchor="w")
        if hint:
            ctk.CTkLabel(container, text=hint,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=C["text_muted"]).pack(anchor="w", pady=(1, 2))
        opt_row = ctk.CTkFrame(container, fg_color="transparent")
        opt_row.pack(anchor="w", pady=(2, 0))
        for opt in options:
            ctk.CTkRadioButton(opt_row, text=opt, variable=var, value=opt,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=C["text_mid"], fg_color=C["accent"],
                hover_color=C["navy"]).pack(side="left", padx=(0, 20))

    def divider(parent_w):
        ctk.CTkFrame(parent_w, fg_color=C["border"], height=1).pack(fill="x", pady=(2, 4))

    # =========================================================
    # VARIABLES
    # =========================================================
    first_name         = tk.StringVar()
    middle_name        = tk.StringVar()
    last_name          = tk.StringVar()
    ext_name           = tk.StringVar()
    birthdate_var      = tk.StringVar()
    age_var            = tk.StringVar()
    address_var        = tk.StringVar()
    barangay_var       = tk.StringVar()
    religion_var       = tk.StringVar()
    other_religion_var = tk.StringVar()
    sex_var            = tk.StringVar()
    interview_date_var = tk.StringVar()
    interviewer_var    = tk.StringVar()
    position_var       = tk.StringVar()
    emp_info_var       = tk.StringVar()
    place_var          = tk.StringVar()
    other_place_var    = tk.StringVar()
    status_var         = tk.StringVar()
    ofw_answer         = tk.StringVar()
    status_answer      = tk.StringVar(value="Studying")

    barangay_list = [
        "Barangay Zone I", "Barangay Zone II", "Barangay Zone III",
        "Barangay Zone IV", "Barangay Zone V", "Barangay Zone VI",
        "Barangay Zone VII", "Barangay Zone VIII",
        "De La Paz", "San Antonio", "San Buenaventura", "San Diego",
        "San Isidro", "San Jose", "San Juan", "San Luis",
        "San Pablo", "San Pedro", "San Rafael", "San Roque",
        "San Salvador", "Santo Domingo", "Santo Tomas",
    ]
    religions = [
        "Roman Catholic", "Aglipayan", "Iglesia ni Cristo", "Islam",
        "Christian", "Jehovah's Witness", "Seventh-day Adventist", "Others",
    ]

    # =========================================================
    # CARD 1 — Personal Information
    # =========================================================
    body1 = make_card(content, "Personal Information", "Respondent's legal name and identity")

    name_row = ctk.CTkFrame(body1, fg_color="transparent")
    name_row.pack(fill="x")
    make_entry(name_row, "First Name",           first_name,  required=True, side="left", padx_right=12)
    make_entry(name_row, "Middle Name",          middle_name, side="left", padx_right=12)
    make_entry(name_row, "Last Name",            last_name,   required=True, side="left", padx_right=12)
    make_entry(name_row, "Extension (e.g. Jr.)", ext_name,    side="left", expand=False)

    divider(body1)

    bd_row = ctk.CTkFrame(body1, fg_color="transparent")
    bd_row.pack(fill="x")
    make_date_field(bd_row, "Birthdate", birthdate_var, required=True,
                    side="left", padx_right=12, maxdate=datetime.today())

    age_container = ctk.CTkFrame(bd_row, fg_color="transparent")
    age_container.pack(side="left", fill="x", expand=True, pady=(0, 2))
    ctk.CTkLabel(age_container, text="Age (auto-calculated)",
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        text_color=C["text_mid"]).pack(anchor="w")
    ctk.CTkEntry(age_container, textvariable=age_var, state="readonly", height=32,
        fg_color=C["bg"], border_color=C["border"], border_width=1,
        text_color=C["accent"],
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).pack(fill="x", pady=(2, 0))

    def calculate_age(*_):
        try:
            val = birthdate_var.get()
            if len(val) != 10:
                age_var.set(""); return
            bd = datetime.strptime(val, "%Y-%m-%d")
            today = datetime.today()
            if bd > today:
                age_var.set(""); return
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            age_var.set(str(max(age, 0)))
        except:
            age_var.set("")

    birthdate_var.trace_add("write", calculate_age)
    divider(body1)
    make_radio_group(body1, "Sex", sex_var, ["Male", "Female", "LGBTQ+"])

    # =========================================================
    # CARD 2 — Address & Contact
    # =========================================================
    body2 = make_card(content, "Address & Contact", "Where the respondent lives and can be reached")
    make_entry(body2, "Street / House Address", address_var, required=True)
    addr_row = ctk.CTkFrame(body2, fg_color="transparent")
    addr_row.pack(fill="x")
    make_combo(addr_row, "Barangay", barangay_var, barangay_list, required=True)
    divider(body2)
    interview_row = ctk.CTkFrame(body2, fg_color="transparent")
    interview_row.pack(fill="x")
    make_date_field(interview_row, "Date of Interview", interview_date_var, side="left", padx_right=12)
    make_entry(interview_row, "Interviewed By", interviewer_var, side="left", padx_right=12)
    make_entry(interview_row, "Position", position_var, side="left")

    # =========================================================
    # CARD 3 — Religion
    # =========================================================
    body3 = make_card(content, "Religion")
    rel_row = ctk.CTkFrame(body3, fg_color="transparent")
    rel_row.pack(fill="x")
    rel_container = ctk.CTkFrame(rel_row, fg_color="transparent")
    rel_container.pack(side="left", fill="x", expand=True, padx=(0, 12), pady=(0, 2))
    ctk.CTkLabel(rel_container, text="Religion",
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        text_color=C["text_mid"]).pack(anchor="w")
    rel_cb = ctk.CTkComboBox(rel_container, variable=religion_var, values=religions,
        state="readonly", height=32, fg_color=C["bg"], border_color=C["border"],
        border_width=1, text_color=C["text_dark"],
        font=ctk.CTkFont(family="Segoe UI", size=11),
        button_color=C["accent"], dropdown_fg_color=C["white"])
    rel_cb.pack(fill="x", pady=(2, 0))
    other_rel_entry = ctk.CTkEntry(rel_container, textvariable=other_religion_var, height=32,
        placeholder_text="Please specify religion...", fg_color=C["bg"],
        border_color=C["border"], border_width=1,
        font=ctk.CTkFont(family="Segoe UI", size=11))
    other_rel_entry.pack_forget()

    def check_religion(choice):
        if choice == "Others":
            other_rel_entry.pack(fill="x", pady=(4, 0))
        else:
            other_rel_entry.pack_forget()
            other_religion_var.set("")
    rel_cb.configure(command=check_religion)

    # =========================================================
    # CARD 4 — Employment
    # =========================================================
    body4 = make_card(content, "Employment Information")
    make_radio_group(body4, "Type of Work", emp_info_var, ["Private", "Government", "Self-employed"])
    divider(body4)
    make_radio_group(body4, "Place of Work", place_var, ["Luisiana", "Others"],
                     hint="Select where the respondent primarily works")
    other_place_entry = ctk.CTkEntry(body4, textvariable=other_place_var, height=32,
        placeholder_text="Please specify place of work...", fg_color=C["bg"],
        border_color=C["border"], border_width=1,
        font=ctk.CTkFont(family="Segoe UI", size=11))
    other_place_entry.pack_forget()

    def check_place(*_):
        if place_var.get() == "Others":
            other_place_entry.pack(fill="x", pady=(0, 2))
        else:
            other_place_entry.pack_forget()
            other_place_var.set("")
    place_var.trace_add("write", check_place)
    divider(body4)
    make_radio_group(body4, "Employment Status", status_var, ["Contractual", "Regular"])

    # =========================================================
    # CARD 5 — OFW
    # =========================================================
    body5 = make_card(content, "OFW Information", "Overseas Filipino Worker status")
    ctk.CTkLabel(body5, text="Are you an OFW?",
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        text_color=C["text_mid"]).pack(anchor="w")
    ofw_radio_row = ctk.CTkFrame(body5, fg_color="transparent")
    ofw_radio_row.pack(anchor="w", pady=(2, 0))
    ofw_frame = create_ofw_section(body5)
    ofw_frame.pack_forget()

    def toggle_ofw():
        if ofw_answer.get() == "Yes":
            ofw_frame.pack(fill="x", pady=(4, 0))
        else:
            ofw_frame.pack_forget()

    for opt in ["Yes", "No"]:
        ctk.CTkRadioButton(ofw_radio_row, text=opt, variable=ofw_answer, value=opt,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=C["text_mid"], fg_color=C["accent"],
            hover_color=C["navy"], command=toggle_ofw).pack(side="left", padx=(0, 20))

    # =========================================================
    # CARD 6 — Current Activity
    # =========================================================
    body6 = make_card(content, "Current Activity")
    ctk.CTkLabel(body6, text="Currently:",
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        text_color=C["text_mid"]).pack(anchor="w")
    work_radio_row = ctk.CTkFrame(body6, fg_color="transparent")
    work_radio_row.pack(anchor="w", pady=(2, 0))
    work_frame = create_work_section(body6)
    work_frame.pack_forget()

    def toggle_work():
        if status_answer.get() == "Working":
            work_frame.pack(fill="x", pady=(4, 0))
        else:
            work_frame.pack_forget()

    for opt in ["Studying", "Working"]:
        ctk.CTkRadioButton(work_radio_row, text=opt, variable=status_answer, value=opt,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=C["text_mid"], fg_color=C["accent"],
            hover_color=C["navy"], command=toggle_work).pack(side="left", padx=(0, 20))

    # =========================================================
    # BOTTOM ACTION BAR — packed before age container so we can
    # insert the dynamic forms above it using before=action_bar
    # =========================================================
    action_bar = ctk.CTkFrame(content, fg_color=C["white"], corner_radius=10)
    action_bar.pack(fill="x", pady=(4, 0))

    inner_bar = ctk.CTkFrame(action_bar, fg_color="transparent")
    inner_bar.pack(fill="x", padx=12, pady=8)

    ctk.CTkLabel(inner_bar, text="* Required fields",
        font=ctk.CTkFont(family="Segoe UI", size=10),
        text_color=C["text_muted"]).pack(side="left")

    ctk.CTkButton(inner_bar, text="Clear Form", command=lambda: clear_form(),
        fg_color="transparent", border_width=1, border_color=C["border"],
        text_color=C["text_mid"], hover_color=C["bg"],
        font=ctk.CTkFont(family="Segoe UI", size=12),
        corner_radius=8, height=34, width=110).pack(side="right", padx=(8, 0))

    ctk.CTkButton(inner_bar, text="  ✓   Save Resident Information",
        command=lambda: save_data(),
        fg_color=C["accent"], hover_color=C["navy"], text_color=C["white"],
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        corner_radius=8, height=36, width=260).pack(side="right")

    # =========================================================
    # AGE DYNAMIC FORMS
    # Container starts hidden. It inserts itself above the action
    # bar only when an age-triggered form is needed, then fully
    # disappears (no leftover space) when the age no longer qualifies.
    # =========================================================
    age_dynamic_container = ctk.CTkFrame(content, fg_color="transparent")

    youth_frame = create_youth(age_dynamic_container)
    child_frame = create_child(age_dynamic_container)
    youth_frame.pack_forget()
    child_frame.pack_forget()
    age_dynamic_container.pack_forget()  # hidden by default — no space reserved

    def check_age(*_):
        # Always collapse everything first
        youth_frame.pack_forget()
        child_frame.pack_forget()
        age_dynamic_container.pack_forget()

        try:
            age = int(age_var.get())
            if 0 <= age <= 4:
                # Show container just above the save bar, then show child form inside it
                age_dynamic_container.pack(fill="x", pady=(0, 3), before=action_bar)
                child_frame.pack(fill="x")
            elif 15 <= age <= 30:
                # Show container just above the save bar, then show youth form inside it
                age_dynamic_container.pack(fill="x", pady=(0, 3), before=action_bar)
                youth_frame.pack(fill="x")
        except:
            pass  # age_var is empty or non-numeric — container stays hidden

    age_var.trace_add("write", check_age)

    # =========================================================
    # VALIDATION + CLEAR + SAVE
    # =========================================================
    def validate_form():
        if not first_name.get().strip():
            messagebox.showerror("Validation Error", "First Name is required.")
            return False
        if not last_name.get().strip():
            messagebox.showerror("Validation Error", "Last Name is required.")
            return False
        if not birthdate_var.get():
            messagebox.showerror("Validation Error", "Birthdate is required.")
            return False
        return True

    def clear_form():
        for var in [first_name, middle_name, last_name, ext_name,
                    birthdate_var, age_var, address_var, barangay_var,
                    religion_var, other_religion_var, sex_var,
                    interview_date_var, interviewer_var, position_var,
                    emp_info_var, place_var, other_place_var, status_var,
                    ofw_answer]:
            var.set("")
        status_answer.set("Studying")
        youth_frame.pack_forget()
        child_frame.pack_forget()
        age_dynamic_container.pack_forget()
        ofw_frame.pack_forget()
        work_frame.pack_forget()

    def save_data():
        if not validate_form():
            return
        try:
            conn   = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO responders (Date_Of_Interview) VALUES (%s)",
                (interview_date_var.get(),)
            )
            respondent_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO Personal_Information (
                    Respondent_ID, First_Name, Middle_Name, Last_Name,
                    Extension_Name, Age, Date_Of_Birth, Gender,
                    House_Number, Street_Name, Barangay, Religion, Contact_Number
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                respondent_id,
                first_name.get(), middle_name.get(), last_name.get(), ext_name.get(),
                age_var.get(), birthdate_var.get(), sex_var.get(),
                0, address_var.get(), barangay_var.get(),
                other_religion_var.get() if religion_var.get() == "Others" else religion_var.get(),
                0
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Saved", "Resident information saved successfully!")
            clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    return frame