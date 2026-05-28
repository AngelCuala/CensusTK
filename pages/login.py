import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def make_rounded_rect(width, height, radius, fill, outline=None, outline_width=0):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [0, 0, width - 1, height - 1],
        radius=radius, fill=fill,
        outline=outline, width=outline_width
    )
    return img


def make_orb(size, color_rgba):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, size - 1, size - 1], fill=color_rgba)
    return img.filter(ImageFilter.GaussianBlur(size // 3))


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# ─────────────────────────────────────────────
#  ROUNDED ENTRY WIDGET
# ─────────────────────────────────────────────

class RoundedEntry(tk.Frame):
    def __init__(self, parent, icon, textvariable, placeholder="",
                 show_char=None, **kwargs):
        super().__init__(parent, bg=parent["bg"], **kwargs)

        self._placeholder = placeholder
        self._show_char   = show_char
        self._active      = False
        self._visible     = False              # password currently visible?
        self._bg_photo    = None

        self._canvas = tk.Canvas(self, height=48, bg=parent["bg"],
                                 highlightthickness=0)
        self._canvas.pack(fill="x")

        self._icon_lbl = tk.Label(self._canvas, text=icon,
                                  bg="#1e2a45", fg="#6c8ab0",
                                  font=("Segoe UI", 13))

        self._var   = textvariable
        self._entry = tk.Entry(self._canvas, textvariable=self._var,
                               bd=0, bg="#1e2a45", fg="#8fa8c8",
                               insertbackground="#5b8dee",
                               font=("Segoe UI", 11),
                               relief="flat", show="")
        self._entry.insert(0, placeholder)

        # Eye toggle — only for password fields
        self._eye_btn = None
        if self._show_char:
            self._eye_btn = tk.Label(
                self._canvas, text="🙈",
                bg="#1e2a45", fg="#6c8ab0",
                font=("Segoe UI", 11),
                cursor="hand2"
            )
            self._eye_btn.bind("<Button-1>", self._toggle_visibility)

        self._canvas.bind("<Configure>", self._redraw)
        self._entry.bind("<FocusIn>",    self._on_focus_in)
        self._entry.bind("<FocusOut>",   self._on_focus_out)

    def _redraw(self, event=None):
        w = max(self._canvas.winfo_width(), 120)
        h = 48
        self._canvas.config(height=h)
        self._canvas.delete("all")

        color  = "#263352" if self._active else "#1e2a45"
        border = hex_to_rgb("#5b8dee") + (255,) if self._active \
                 else hex_to_rgb("#2d3f61") + (255,)

        img = make_rounded_rect(w, h, 12,
                                fill=hex_to_rgb(color) + (255,),
                                outline=border, outline_width=2)
        self._bg_photo = ImageTk.PhotoImage(img)
        self._canvas.create_image(0, 0, anchor="nw", image=self._bg_photo)

        self._icon_lbl.config(bg=color)
        self._canvas.create_window(16, h // 2, anchor="w", window=self._icon_lbl)

        entry_width = w - 100 if self._eye_btn else w - 70
        self._canvas.create_window(48, h // 2, anchor="w",
                                   window=self._entry, width=entry_width, height=28)

        if self._eye_btn:
            self._eye_btn.config(bg=color)
            self._canvas.create_window(w - 14, h // 2, anchor="e",
                                       window=self._eye_btn)

    def _toggle_visibility(self, _=None):
        self._visible = not self._visible
        if self._visible:
            self._entry.config(show="")
            self._eye_btn.config(text="👁")
        else:
            # Only mask when not showing placeholder
            if self._entry.get() != self._placeholder:
                self._entry.config(show=self._show_char)
            self._eye_btn.config(text="🚫")

    def _on_focus_in(self, _=None):
        self._active = True
        if self._entry.get() == self._placeholder:
            self._entry.delete(0, "end")
        self._entry.config(fg="#dde8ff")
        if self._show_char and not self._visible:
            self._entry.config(show=self._show_char)
        self._redraw()

    def _on_focus_out(self, _=None):
        self._active = False
        if not self._entry.get():
            self._entry.config(show="")
            self._entry.insert(0, self._placeholder)
            self._entry.config(fg="#8fa8c8")
        self._redraw()

    def get(self):
        v = self._var.get()
        return "" if v == self._placeholder else v


# ─────────────────────────────────────────────
#  ANIMATED LOGIN BUTTON
# ─────────────────────────────────────────────

class GlowButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, height=50, bd=0,
                         highlightthickness=0, bg=parent["bg"], **kwargs)
        self._text      = text
        self._command   = command
        self._hover     = False
        self._btn_photo = None
        self._shd_photo = None

        self.bind("<Configure>", self._draw)
        self.bind("<Enter>",     self._on_enter)
        self.bind("<Leave>",     self._on_leave)
        self.bind("<Button-1>",  self._on_click)

    def _draw(self, _=None):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            return
        self.delete("all")

        fill = (74, 122, 232, 255) if self._hover else (53, 99, 210, 255)

        shadow_img = make_rounded_rect(w, h - 4, 14, (0, 0, 0, 60))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(6))
        self._shd_photo = ImageTk.PhotoImage(shadow_img)
        self.create_image(0, 6, anchor="nw", image=self._shd_photo)

        btn_img = make_rounded_rect(w, h - 6, 14, fill)
        self._btn_photo = ImageTk.PhotoImage(btn_img)
        self.create_image(0, 0, anchor="nw", image=self._btn_photo)

        self.create_text(w // 2, (h - 6) // 2,
                         text=self._text, fill="white",
                         font=("Segoe UI", 12, "bold"))

    def _on_enter(self, _=None):
        self._hover = True;  self._draw(); self.config(cursor="hand2")

    def _on_leave(self, _=None):
        self._hover = False; self._draw()

    def _on_click(self, _=None):
        self._command()


# ─────────────────────────────────────────────
#  MAIN LOGIN BUILDER
# ─────────────────────────────────────────────

def create_login(parent, on_login):

    for w in parent.winfo_children():
        w.destroy()

    CARD_BG = "#111827"

    # ── Root frame ──────────────────────────────────────────────────────────
    frame = tk.Frame(parent, bg="#0a0e23")
    frame.pack(fill="both", expand=True)

    frame.update_idletasks()

    # ── Background canvas (full-size, behind everything) ────────────────────
    bg_canvas = tk.Canvas(frame, highlightthickness=0, bg="#0a0e23")
    bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    _bg_store = {}

    BG_IMAGE_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "municipal.jpg"
    )

    try:
        _raw_bg = Image.open(BG_IMAGE_PATH).convert("RGBA")
    except Exception as e:
        print("Background image error:", e)
        _raw_bg = None

    def draw_background(event=None):
        bg_canvas.delete("all")
        w = frame.winfo_width()
        h = frame.winfo_height()
        if w < 2 or h < 2:
            return

        if _raw_bg is not None:
            img_w, img_h = _raw_bg.size
            scale = max(w / img_w, h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            resized = _raw_bg.resize((new_w, new_h), Image.LANCZOS)

            left = (new_w - w) // 2
            top  = (new_h - h) // 2
            cropped = resized.crop((left, top, left + w, top + h))

            overlay = Image.new("RGBA", (w, h), (5, 10, 25, 175))
            blended = Image.alpha_composite(cropped, overlay)
            blended = blended.filter(ImageFilter.GaussianBlur(2))

            _bg_store["bg"] = ImageTk.PhotoImage(blended)
            bg_canvas.create_image(0, 0, anchor="nw", image=_bg_store["bg"])

        else:
            from PIL import Image as _I
            grad = _I.new("RGB", (w, h))
            pixels = grad.load()
            for y in range(h):
                t = y / h
                for x in range(w):
                    s = x / w
                    pixels[x, y] = (
                        min(255, int(10 + t*20 + s*15)),
                        min(255, int(14 + t*26 + s*12)),
                        min(255, int(35 + t*35 + s*25)),
                    )
            _bg_store["bg"] = ImageTk.PhotoImage(grad)
            bg_canvas.create_image(0, 0, anchor="nw", image=_bg_store["bg"])

        orb_data = [
            (int(w * 0.15), int(h * 0.25), 340, (30,  90, 220, 35)),
            (int(w * 0.82), int(h * 0.15), 260, (90,  40, 200, 30)),
            (int(w * 0.70), int(h * 0.82), 300, (20, 120, 180, 28)),
        ]
        for i, (ox, oy, sz, col) in enumerate(orb_data):
            orb = make_orb(sz, col)
            _bg_store[f"orb{i}"] = ImageTk.PhotoImage(orb)
            bg_canvas.create_image(ox, oy, anchor="center",
                                   image=_bg_store[f"orb{i}"])

    frame.bind("<Configure>", draw_background)

    # ── Card canvas ─────────────────────────────────────────────────────────
    CARD_W = 420
    CARD_H = 520
    CARD_R = 24

    card_canvas = tk.Canvas(frame, width=CARD_W, height=CARD_H,
                             bd=0, highlightthickness=0, bg="#0a0e23")
    card_canvas.place(relx=0.5, rely=0.5, anchor="center")

    _card_store = {}

    def draw_card():
        card_canvas.delete("all")

        shadow = make_rounded_rect(CARD_W, CARD_H, CARD_R, (0, 0, 0, 140))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        _card_store["shadow"] = ImageTk.PhotoImage(shadow)
        card_canvas.create_image(8, 10, anchor="nw", image=_card_store["shadow"])

        card_img = make_rounded_rect(
            CARD_W, CARD_H, CARD_R,
            (17, 24, 39, 250),
            outline=(42, 62, 100, 255),
            outline_width=1
        )
        _card_store["body"] = ImageTk.PhotoImage(card_img)
        card_canvas.create_image(0, 0, anchor="nw", image=_card_store["body"])

    draw_card()

    # ── Content frame ────────────────────────────────────────────────────────
    content = tk.Frame(card_canvas, bg=CARD_BG)
    card_canvas.create_window(CARD_W // 2, CARD_H // 2, anchor="center",
                               window=content, width=CARD_W - 60,
                               height=CARD_H - 40)

    # ── Logo ─────────────────────────────────────────────────────────────────
    try:
        logo_img = Image.open("assets/logo.png").resize((70, 70), Image.LANCZOS)
        mask = Image.new("L", (70, 70), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 69, 69], fill=255)
        logo_img.putalpha(mask)
        _logo_photo = ImageTk.PhotoImage(logo_img)
        logo_lbl = tk.Label(content, image=_logo_photo, bg=CARD_BG)
        logo_lbl.image = _logo_photo
        logo_lbl.pack(pady=(20, 6))
    except Exception:
        tk.Label(content, text="🏛", bg=CARD_BG, fg="#5b8dee",
                 font=("Segoe UI", 36)).pack(pady=(20, 6))

    # ── Title ─────────────────────────────────────────────────────────────────
    tk.Label(content, text="Welcome Back",
             bg=CARD_BG, fg="#e8eef8",
             font=("Segoe UI", 20, "bold")).pack()

    tk.Label(content, text="Sign in to your account",
             bg=CARD_BG, fg="#4a6080",
             font=("Segoe UI", 10)).pack(pady=(3, 22))

    tk.Frame(content, height=1, bg="#1e2d4a").pack(fill="x", pady=(0, 22))

    # ── Entries ───────────────────────────────────────────────────────────────
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    RoundedEntry(content, "👤", username_var,
                 placeholder="Username or Email").pack(fill="x", pady=5)
    RoundedEntry(content, "🔒", password_var,
                 placeholder="Password", show_char="●").pack(fill="x", pady=5)


    # ── Login logic ───────────────────────────────────────────────────────────
    def login():
        user = username_var.get().strip()
        pwd  = password_var.get().strip()
        if user == "Username or Email": user = ""
        if pwd  == "Password":          pwd  = ""
        if not user or not pwd:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            from db import connect_db
            conn = connect_db()
        except Exception:
            messagebox.showerror("Database Error", "Cannot connect to database.")
            return

        if conn is None:
            messagebox.showerror("Database Error", "Cannot connect to database.")
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM accounts
            WHERE (Username = %s OR Email = %s) AND Password = %s
        """, (user, user, pwd))
        account = cursor.fetchone()
        conn.close()

        if account:
            on_login({
                "User_ID":    account["User_ID"],
                "First_Name": account["First_Name"],
                "Last_Name":  account.get("Last_Name", ""),
                "Username":   account["Username"],
                "Email":      account["Email"],
                "User_type":  account["User_type"],
            })
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # ── Button ────────────────────────────────────────────────────────────────
    GlowButton(content, "Sign In", login).pack(
        fill="x",
        ipady=4,
        pady=(18, 0)
    )

    parent.bind("<Return>", lambda e: login())

    # ── Footer ────────────────────────────────────────────────────────────────
    tk.Label(content,
             text="Municipal Information System  •  v2.0",
             bg=CARD_BG, fg="#253550",
             font=("Segoe UI", 8)).pack(side="bottom", pady=(20, 0))

    frame.after(100, lambda: draw_background())

    return frame


# ─────────────────────────────────────────────
#  STANDALONE TEST ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Municipal Information System")
    root.geometry("900x600")
    root.minsize(700, 500)

    def on_login(user_data):
        print("Logged in:", user_data)
        messagebox.showinfo("Success", f"Welcome, {user_data['First_Name']}!")

    create_login(root, on_login)
    root.mainloop()