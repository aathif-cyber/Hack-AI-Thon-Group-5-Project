"""
GreenGrid — Smart Energy Consumption & Carbon Tracker
Hack-AI-Thon 2026 | Group 5

A single-file, Tkinter-only interactive prototype.

No external GUI libraries are required.
The visual "3D" effect is created with Tkinter Canvas polygons,
gradients, shadows, isometric surfaces, and interactive hitboxes.

Core OOP classes:
    Appliance
    EnergyRecord
    EnergyReport
    RecommendationEngine
"""

from __future__ import annotations

import math
import tkinter as tk
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Tuple


# =============================================================================
# THEME
# =============================================================================

BG = "#07111F"
BG_2 = "#091728"
PANEL = "#0D1A2B"
PANEL_2 = "#11243A"
PANEL_3 = "#17324E"
TEXT = "#F3F8FF"
MUTED = "#8FA8C3"
GRID = "#1D3853"
CYAN = "#39E6FF"
GREEN = "#48E7A0"
LIME = "#B9FF63"
YELLOW = "#FFD166"
ORANGE = "#FF9D5C"
RED = "#FF607A"
PURPLE = "#9B80FF"
BLUE = "#60ABFF"
PINK = "#FF76C8"
WHITE = "#FFFFFF"
SHADOW = "#030A12"

FONT = "Segoe UI"
MONO = "Consolas"

ROOM_META = {
    "Living Room": {
        "subtitle": "Relax • Entertain • Connect",
        "wall": "#102338",
        "floor": "#123148",
        "accent": CYAN,
        "ambient": "#2C708C",
    },
    "Kitchen": {
        "subtitle": "Cook • Prepare • Optimize",
        "wall": "#2C1E29",
        "floor": "#3B2B20",
        "accent": ORANGE,
        "ambient": "#8D5B35",
    },
    "Bedroom": {
        "subtitle": "Rest • Recharge • Recover",
        "wall": "#1A1631",
        "floor": "#282044",
        "accent": PURPLE,
        "ambient": "#5C4B9E",
    },
    "Study": {
        "subtitle": "Focus • Create • Learn",
        "wall": "#10251E",
        "floor": "#1D3A2C",
        "accent": GREEN,
        "ambient": "#398064",
    },
}


# =============================================================================
# CORE OOP MODEL
# =============================================================================

@dataclass
class Appliance:
    """An electrical appliance and its daily usage profile."""

    name: str
    power_w: float
    room: str
    category: str
    icon: str
    color: str
    usage_hours: float
    position: Tuple[float, float]
    description: str
    enabled: bool = True

    @property
    def power_kw(self) -> float:
        return self.power_w / 1000.0

    def daily_kwh(self) -> float:
        if not self.enabled:
            return 0.0
        return self.power_kw * max(0.0, self.usage_hours)

    def monthly_kwh(self, days: int = 30) -> float:
        return self.daily_kwh() * days


@dataclass
class EnergyRecord:
    """Usage record for an appliance over a defined period."""

    appliance: Appliance
    usage_hours: float
    record_date: date = date.today()

    def energy_kwh(self) -> float:
        if not self.appliance.enabled:
            return 0.0
        return self.appliance.power_kw * max(0.0, self.usage_hours)


class EnergyReport:
    """Computes aggregate energy, cost, carbon, rankings and room totals."""

    def __init__(
        self,
        records: List[EnergyRecord],
        electricity_rate: float = 8.50,
        emission_factor: float = 0.71,
    ) -> None:
        self.records = records
        self.electricity_rate = electricity_rate
        self.emission_factor = emission_factor

    @property
    def total_kwh(self) -> float:
        return sum(record.energy_kwh() for record in self.records)

    @property
    def estimated_cost(self) -> float:
        return self.total_kwh * self.electricity_rate

    @property
    def estimated_emissions(self) -> float:
        return self.total_kwh * self.emission_factor

    def appliance_usage(self) -> List[Tuple[Appliance, float]]:
        values = [
            (record.appliance, record.energy_kwh())
            for record in self.records
        ]
        values.sort(key=lambda pair: pair[1], reverse=True)
        return values

    def top_consumers(self, count: int = 5) -> List[Tuple[Appliance, float]]:
        return self.appliance_usage()[:count]

    def room_totals(self) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for record in self.records:
            room = record.appliance.room
            totals[room] = totals.get(room, 0.0) + record.energy_kwh()
        return totals


class RecommendationEngine:
    """Generates concise and actionable energy-saving recommendations."""

    @staticmethod
    def build(report: EnergyReport) -> List[Tuple[str, str, str]]:
        recommendations: List[Tuple[str, str, str]] = []
        ranking = report.appliance_usage()

        if ranking:
            appliance, energy = ranking[0]
            saved = appliance.power_kw * report.electricity_rate
            recommendations.append(
                (
                    "HIGH IMPACT",
                    f"Trim {appliance.name} by 1 hour",
                    f"That could save roughly ₹{saved:.0f} per day "
                    f"at the current electricity rate.",
                )
            )

        climate = [
            (app, energy)
            for app, energy in ranking
            if app.category in {"Cooling", "Climate"}
        ]
        if climate:
            app, energy = climate[0]
            recommendations.append(
                (
                    "CLIMATE",
                    f"Optimize {app.name}",
                    f"Current load is {energy:.2f} kWh/day. "
                    "Use only when the room is occupied.",
                )
            )

        kitchen = [
            app for app, _ in ranking if app.category == "Kitchen"
        ]
        if kitchen:
            recommendations.append(
                (
                    "KITCHEN",
                    "Batch high-wattage tasks",
                    "Combine cooking cycles to reduce repeated heating time.",
                )
            )

        recommendations.append(
            (
                "STANDBY",
                "Kill vampire load",
                "Switch off screens, lamps and chargers when not in active use.",
            )
        )

        return recommendations[:4]


# =============================================================================
# DRAWING HELPERS
# =============================================================================

def hex_rgb(color: str) -> Tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def rgb_hex(rgb: Tuple[float, float, float]) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2]))),
    )


def mix(c1: str, c2: str, amount: float) -> str:
    a = hex_rgb(c1)
    b = hex_rgb(c2)
    amount = max(0.0, min(1.0, amount))
    return rgb_hex(
        (
            a[0] + (b[0] - a[0]) * amount,
            a[1] + (b[1] - a[1]) * amount,
            a[2] + (b[2] - a[2]) * amount,
        )
    )


def darken(color: str, amount: float) -> str:
    return mix(color, BG, amount)


def brighten(color: str, amount: float) -> str:
    return mix(color, WHITE, amount)


def rounded_rect(
    canvas: tk.Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    radius: float,
    fill: str,
    outline: str = "",
    width: int = 1,
) -> None:
    """Draw a rounded rectangle using standard Canvas primitives."""
    if x2 <= x1 or y2 <= y1:
        return

    canvas.create_rectangle(
        x1 + radius, y1, x2 - radius, y2,
        fill=fill, outline=""
    )
    canvas.create_rectangle(
        x1, y1 + radius, x2, y2 - radius,
        fill=fill, outline=""
    )
    canvas.create_arc(
        x1, y1, x1 + radius * 2, y1 + radius * 2,
        start=90, extent=90, fill=fill, outline=""
    )
    canvas.create_arc(
        x2 - radius * 2, y1, x2, y1 + radius * 2,
        start=0, extent=90, fill=fill, outline=""
    )
    canvas.create_arc(
        x1, y2 - radius * 2, x1 + radius * 2, y2,
        start=180, extent=90, fill=fill, outline=""
    )
    canvas.create_arc(
        x2 - radius * 2, y2 - radius * 2, x2, y2,
        start=270, extent=90, fill=fill, outline=""
    )

    if outline:
        canvas.create_line(
            x1 + radius, y1, x2 - radius, y1,
            fill=outline, width=width
        )
        canvas.create_line(
            x2, y1 + radius, x2, y2 - radius,
            fill=outline, width=width
        )
        canvas.create_line(
            x2 - radius, y2, x1 + radius, y2,
            fill=outline, width=width
        )
        canvas.create_line(
            x1, y2 - radius, x1, y1 + radius,
            fill=outline, width=width
        )


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class GreenGridApp(tk.Tk):
    """Premium Tkinter dashboard and game-like energy environment."""

    def __init__(self) -> None:
        super().__init__()

        self.title("GreenGrid • Smart Energy Intelligence")
        self.geometry("1440x900")
        self.minsize(1180, 760)
        self.configure(bg=BG)

        try:
            self.state("zoomed")
        except tk.TclError:
            pass

        self.electricity_rate = 8.50
        self.emission_factor = 0.71

        self.current_room = "Living Room"
        self.selected_appliance: Optional[Appliance] = None
        self.current_view = "dashboard"
        self.animation_phase = 0.0
        self.nav_buttons: Dict[str, tk.Button] = {}
        self.room_buttons: Dict[str, tk.Button] = {}
        self.appliance_button_refs: Dict[str, tk.Button] = {}
        self.appliance_hitboxes: List[Tuple[Tuple[float, float, float, float], Appliance]] = []
        self.room_canvas: Optional[tk.Canvas] = None
        self.scene_status = tk.StringVar(value="Select an appliance in the room.")

        self.appliances = self._build_appliances()
        self.records: List[EnergyRecord] = [
            EnergyRecord(app, app.usage_hours) for app in self.appliances
        ]
        self.report = self._make_report()

        self._build_shell()
        self.show_dashboard()
        self._animate()

    # -------------------------------------------------------------------------
    # MODEL SETUP
    # -------------------------------------------------------------------------

    def _build_appliances(self) -> List[Appliance]:
        return [
            Appliance(
                "Smart TV", 120, "Living Room", "Entertainment",
                "TV", CYAN, 4.0, (0.48, 0.44),
                "Large display for movies, sports and entertainment."
            ),
            Appliance(
                "Ceiling Fan", 75, "Living Room", "Cooling",
                "FAN", GREEN, 7.0, (0.77, 0.20),
                "High-efficiency ceiling fan for air circulation."
            ),
            Appliance(
                "Air Conditioner", 1500, "Living Room", "Climate",
                "AC", BLUE, 4.5, (0.76, 0.55),
                "Inverter AC used for high-comfort cooling."
            ),
            Appliance(
                "Refrigerator", 180, "Kitchen", "Kitchen",
                "FR", ORANGE, 12.0, (0.24, 0.68),
                "Main refrigerator with low-power cycling."
            ),
            Appliance(
                "Microwave", 1000, "Kitchen", "Kitchen",
                "MW", YELLOW, 0.7, (0.50, 0.64),
                "Quick cooking and reheating."
            ),
            Appliance(
                "Induction Stove", 1800, "Kitchen", "Kitchen",
                "IND", RED, 1.0, (0.74, 0.65),
                "High-wattage cooking zone."
            ),
            Appliance(
                "Bedside Lamp", 12, "Bedroom", "Lighting",
                "LAMP", PURPLE, 4.0, (0.27, 0.69),
                "Warm ambient bedside light."
            ),
            Appliance(
                "Air Cooler", 200, "Bedroom", "Cooling",
                "COOL", GREEN, 5.0, (0.73, 0.56),
                "Portable evening cooler."
            ),
            Appliance(
                "Study Laptop", 90, "Study", "Study",
                "PC", GREEN, 6.0, (0.53, 0.58),
                "Laptop workstation for learning and creation."
            ),
            Appliance(
                "Desk Lamp", 10, "Study", "Lighting",
                "LAMP", YELLOW, 5.0, (0.27, 0.66),
                "Focused task lighting."
            ),
        ]

    def _make_report(self) -> EnergyReport:
        for record in self.records:
            record.usage_hours = record.appliance.usage_hours
        return EnergyReport(
            self.records,
            electricity_rate=self.electricity_rate,
            emission_factor=self.emission_factor,
        )

    def _recalculate(self) -> None:
        self.report = self._make_report()

    # -------------------------------------------------------------------------
    # APP SHELL
    # -------------------------------------------------------------------------

    def _build_shell(self) -> None:
        self.topbar = tk.Frame(self, bg=BG, height=78)
        self.topbar.pack(fill="x", side="top")
        self.topbar.pack_propagate(False)

        brand = tk.Frame(self.topbar, bg=BG)
        brand.pack(side="left", padx=(22, 8))

        tk.Label(
            brand,
            text="🌱",
            bg=BG,
            fg=LIME,
            font=("Segoe UI Emoji", 27),
        ).pack(side="left")

        title_box = tk.Frame(brand, bg=BG)
        title_box.pack(side="left", padx=(8, 0))

        tk.Label(
            title_box,
            text="GreenGrid",
            bg=BG,
            fg=TEXT,
            font=(FONT, 22, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="SMART ENERGY INTELLIGENCE",
            bg=BG,
            fg=CYAN,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w")

        nav = tk.Frame(self.topbar, bg=BG)
        nav.pack(side="left", padx=24, fill="y")

        for label, key in [
            ("⌂  Dashboard", "dashboard"),
            ("◈  Energy World", "world"),
            ("⚡  Insights", "insights"),
        ]:
            button = tk.Button(
                nav,
                text=label,
                command=lambda k=key: self.switch_view(k),
                bg=BG,
                fg=MUTED,
                activebackground=BG,
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                font=(FONT, 10, "bold"),
                padx=14,
                cursor="hand2",
            )
            button.pack(side="left", pady=17)
            self.nav_buttons[key] = button

        status = tk.Frame(self.topbar, bg=BG)
        status.pack(side="right", padx=22)

        self.live_dot = tk.Label(
            status,
            text="●",
            bg=BG,
            fg=GREEN,
            font=(FONT, 12),
        )
        self.live_dot.pack(side="left")

        tk.Label(
            status,
            text="LIVE MODEL",
            bg=BG,
            fg=MUTED,
            font=(FONT, 9, "bold"),
        ).pack(side="left", padx=(4, 16))

        self.datetime_label = tk.Label(
            status,
            text="Today • --:--",
            bg=BG,
            fg=MUTED,
            font=(FONT, 9),
        )
        self.datetime_label.pack(side="left")

        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.footer = tk.Frame(self, bg=BG, height=24)
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)

        self.footer_label = tk.Label(
            self.footer,
            text="🌱 GreenGrid • Sustainable energy, visualized.",
            bg=BG,
            fg="#55728E",
            font=(FONT, 8),
        )
        self.footer_label.pack(side="left", padx=22)

        self.set_nav("dashboard")

    def switch_view(self, view: str) -> None:
        if view == "dashboard":
            self.show_dashboard()
        elif view == "world":
            self.show_energy_world()
        elif view == "insights":
            self.show_insights()

    def set_nav(self, active: str) -> None:
        for key, btn in self.nav_buttons.items():
            if key == active:
                btn.configure(fg=CYAN, bg=darken(CYAN, 0.84))
            else:
                btn.configure(fg=MUTED, bg=BG)

    def clear_body(self) -> None:
        for child in self.body.winfo_children():
            child.destroy()

    # -------------------------------------------------------------------------
    # COMMON UI
    # -------------------------------------------------------------------------

    def make_header(
        self,
        parent: tk.Widget,
        title: str,
        subtitle: str,
        accent: str = CYAN,
    ) -> tk.Frame:
        head = tk.Frame(parent, bg=BG)
        head.pack(fill="x", pady=(4, 16))

        marker = tk.Frame(head, bg=accent, width=4, height=48)
        marker.pack(side="left", fill="y")

        text = tk.Frame(head, bg=BG)
        text.pack(side="left", padx=12)

        tk.Label(
            text,
            text=title,
            bg=BG,
            fg=TEXT,
            font=(FONT, 24, "bold"),
        ).pack(anchor="w")

        tk.Label(
            text,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=(FONT, 10),
        ).pack(anchor="w", pady=(2, 0))

        return head

    def metric_card(
        self,
        parent: tk.Widget,
        title: str,
        value: str,
        sub: str,
        accent: str,
        icon: str,
    ) -> tk.Frame:
        card = tk.Frame(parent, bg=PANEL)
        card.pack_propagate(False)

        top = tk.Frame(card, bg=PANEL)
        top.pack(fill="x", padx=16, pady=(13, 4))

        tk.Label(
            top,
            text=icon,
            bg=PANEL,
            fg=accent,
            font=("Segoe UI Emoji", 18),
        ).pack(side="left")

        tk.Label(
            top,
            text=title.upper(),
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold"),
        ).pack(side="left", padx=8)

        tk.Label(
            card,
            text=value,
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 21, "bold"),
        ).pack(anchor="w", padx=16)

        tk.Label(
            card,
            text=sub,
            bg=PANEL,
            fg=accent,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w", padx=16, pady=(2, 12))

        return card

    def section_title(
        self,
        parent: tk.Widget,
        title: str,
        subtitle: str = "",
        accent: str = CYAN,
    ) -> tk.Frame:
        box = tk.Frame(parent, bg=BG)
        box.pack(fill="x", pady=(0, 10))

        tk.Frame(box, bg=accent, width=3, height=26).pack(side="left")

        text = tk.Frame(box, bg=BG)
        text.pack(side="left", padx=9)

        tk.Label(
            text,
            text=title,
            bg=BG,
            fg=TEXT,
            font=(FONT, 13, "bold"),
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                text,
                text=subtitle,
                bg=BG,
                fg=MUTED,
                font=(FONT, 8),
            ).pack(anchor="w")

        return box

    # -------------------------------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------------------------------

    def show_dashboard(self) -> None:
        self.current_view = "dashboard"
        self.set_nav("dashboard")
        self.clear_body()

        self.make_header(
            self.body,
            "Energy Command Center",
            "A live snapshot of how your home consumes energy.",
            CYAN,
        )

        metrics = tk.Frame(self.body, bg=BG)
        metrics.pack(fill="x", pady=(0, 14))

        for i in range(4):
            metrics.columnconfigure(i, weight=1)

        metric_specs = [
            (
                "TOTAL ENERGY",
                f"{self.report.total_kwh:.1f} kWh",
                "estimated daily consumption",
                CYAN,
                "⚡",
            ),
            (
                "EST. COST",
                f"₹{self.report.estimated_cost:,.0f}",
                "estimated daily electricity cost",
                YELLOW,
                "₹",
            ),
            (
                "CARBON IMPACT",
                f"{self.report.estimated_emissions:.1f} kg",
                "estimated CO₂ equivalent",
                GREEN,
                "🌍",
            ),
            (
                "ACTIVE LOADS",
                f"{sum(a.enabled for a in self.appliances)}/{len(self.appliances)}",
                "appliances currently online",
                PURPLE,
                "◉",
            ),
        ]

        for i, spec in enumerate(metric_specs):
            card = self.metric_card(metrics, *spec)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 8 if i < 3 else 0))

        content = tk.Frame(self.body, bg=BG)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=7)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=1)

        left = tk.Frame(content, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        right = tk.Frame(content, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self._dashboard_chart(left)
        self._top_consumers_panel(right)

    def _dashboard_chart(self, parent: tk.Widget) -> None:
        section = self.section_title(
            parent,
            "⚡ Energy by Room",
            "Daily estimated consumption",
            CYAN,
        )

        card = tk.Frame(parent, bg=PANEL)
        card.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            card,
            bg=PANEL,
            highlightthickness=0,
        )
        canvas.pack(fill="both", expand=True, padx=16, pady=12)

        canvas.bind(
            "<Configure>",
            lambda _e: self._draw_room_chart(canvas),
        )
        self._draw_room_chart(canvas)

    def _draw_room_chart(self, canvas: tk.Canvas) -> None:
        canvas.delete("all")
        w = max(300, canvas.winfo_width())
        h = max(260, canvas.winfo_height())
        totals = self.report.room_totals()
        max_value = max(totals.values(), default=1.0)

        left = 52
        right = 28
        bottom = 48
        top = 28
        plot_h = h - top - bottom
        plot_w = w - left - right
        names = list(totals.keys())
        gap = 22
        bar_w = max(28, (plot_w - gap * (len(names) - 1)) / len(names))

        for step in range(5):
            value = max_value * step / 4
            y = h - bottom - (plot_h * step / 4)
            canvas.create_line(
                left, y, w - right, y,
                fill=GRID, width=1, dash=(2, 6)
            )
            canvas.create_text(
                left - 10, y,
                text=f"{value:.1f}",
                fill=MUTED,
                font=(FONT, 8),
                anchor="e",
            )

        for index, room in enumerate(names):
            value = totals[room]
            x = left + index * (bar_w + gap)
            bar_h = plot_h * (value / max_value if max_value else 0)
            y1 = h - bottom
            y0 = y1 - bar_h
            color = ROOM_META[room]["accent"]

            # Glow
            canvas.create_rectangle(
                x - 3, y0 - 3, x + bar_w + 3, y1 + 3,
                fill=darken(color, 0.70),
                outline="",
            )
            canvas.create_rectangle(
                x, y0, x + bar_w, y1,
                fill=darken(color, 0.25),
                outline=color,
                width=2,
            )

            # Inner highlight
            canvas.create_rectangle(
                x + 7, y0 + 7, x + bar_w - 7, y1,
                fill=darken(color, 0.46),
                outline="",
            )

            canvas.create_text(
                x + bar_w / 2, y0 - 10,
                text=f"{value:.1f}",
                fill=TEXT,
                font=(FONT, 9, "bold"),
            )

            canvas.create_text(
                x + bar_w / 2, y1 + 20,
                text=room.replace(" Room", ""),
                fill=MUTED,
                font=(FONT, 8, "bold"),
            )

        canvas.create_text(
            14, 15,
            text="kWh / day",
            fill=MUTED,
            font=(FONT, 8, "bold"),
            anchor="nw",
        )

    def _top_consumers_panel(self, parent: tk.Widget) -> None:
        self.section_title(
            parent,
            "🔥 Top Consumers",
            "Where the energy is going",
            RED,
        )

        card = tk.Frame(parent, bg=PANEL)
        card.pack(fill="both", expand=True)

        ranking = self.report.top_consumers(5)
        max_energy = ranking[0][1] if ranking else 1

        for index, (app, energy) in enumerate(ranking, start=1):
            row = tk.Frame(card, bg=PANEL)
            row.pack(fill="x", padx=14, pady=(8 if index == 1 else 4, 4))

            num = tk.Label(
                row,
                text=f"{index:02}",
                bg=PANEL,
                fg=app.color,
                font=(MONO, 10, "bold"),
                width=3,
            )
            num.pack(side="left")

            info = tk.Frame(row, bg=PANEL)
            info.pack(side="left", fill="x", expand=True)

            tk.Label(
                info,
                text=app.name,
                bg=PANEL,
                fg=TEXT,
                font=(FONT, 9, "bold"),
            ).pack(anchor="w")

            track = tk.Frame(info, bg=PANEL_3, height=7)
            track.pack(fill="x", pady=(5, 2))
            track.pack_propagate(False)

            bar = tk.Frame(
                track,
                bg=app.color,
                height=7,
                width=max(4, int(150 * energy / max_energy)),
            )
            bar.pack(side="left", fill="y")

            tk.Label(
                row,
                text=f"{energy:.2f}",
                bg=PANEL,
                fg=TEXT,
                font=(MONO, 9, "bold"),
                width=7,
                anchor="e",
            ).pack(side="right")

        # Recommendation card
        recs = RecommendationEngine.build(self.report)
        rec = recs[0]

        tip = tk.Frame(card, bg=darken(CYAN, 0.86))
        tip.pack(fill="x", padx=14, pady=12)

        tk.Label(
            tip,
            text="💡",
            bg=darken(CYAN, 0.86),
            fg=CYAN,
            font=("Segoe UI Emoji", 16),
        ).pack(side="left", padx=10)

        text = tk.Frame(tip, bg=darken(CYAN, 0.86))
        text.pack(side="left", fill="x", expand=True, pady=9)

        tk.Label(
            text,
            text=rec[1],
            bg=darken(CYAN, 0.86),
            fg=TEXT,
            font=(FONT, 9, "bold"),
        ).pack(anchor="w")

        tk.Label(
            text,
            text=rec[2],
            bg=darken(CYAN, 0.86),
            fg=MUTED,
            font=(FONT, 8),
            wraplength=250,
            justify="left",
        ).pack(anchor="w", pady=(2, 0))

    # -------------------------------------------------------------------------
    # ENERGY WORLD
    # -------------------------------------------------------------------------

    def show_energy_world(self) -> None:
        self.current_view = "world"
        self.set_nav("world")
        self.clear_body()

        header = self.make_header(
            self.body,
            "Energy World",
            "Explore your home • click appliances • tune usage • watch the numbers react",
            GREEN,
        )

        world = tk.Frame(self.body, bg=BG)
        world.pack(fill="both", expand=True)

        sidebar = tk.Frame(world, bg=PANEL, width=238)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="🏠 YOUR HOME",
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 4))

        tk.Label(
            sidebar,
            text="Pick a room",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8),
        ).pack(anchor="w", padx=16)

        for room in ROOM_META:
            self._room_selector(sidebar, room)

        spacer = tk.Frame(sidebar, bg=PANEL)
        spacer.pack(fill="both", expand=True)

        self.world_stats = tk.Frame(sidebar, bg=PANEL)
        self.world_stats.pack(fill="x", padx=12, pady=12)
        self._update_world_stats()

        canvas_panel = tk.Frame(world, bg=PANEL)
        canvas_panel.pack(side="left", fill="both", expand=True)

        scene_bar = tk.Frame(canvas_panel, bg=PANEL, height=48)
        scene_bar.pack(fill="x")
        scene_bar.pack_propagate(False)

        meta = ROOM_META[self.current_room]

        self.room_name_label = tk.Label(
            scene_bar,
            text=f"{self.current_room}  •  {meta['subtitle']}",
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 13, "bold"),
        )
        self.room_name_label.pack(side="left", padx=16)

        tk.Label(
            scene_bar,
            text="CLICK AN APPLIANCE TO INSPECT",
            bg=PANEL,
            fg=meta["accent"],
            font=(FONT, 8, "bold"),
        ).pack(side="right", padx=16)

        self.room_canvas = tk.Canvas(
            canvas_panel,
            bg=meta["wall"],
            highlightthickness=0,
            cursor="arrow",
        )
        self.room_canvas.pack(fill="both", expand=True)

        self.room_canvas.bind("<Configure>", lambda _e: self._draw_room_scene())
        self.room_canvas.bind("<Button-1>", self._room_click)
        self.room_canvas.bind("<Motion>", self._room_motion)

        if self.selected_appliance and self.selected_appliance.room != self.current_room:
            self.selected_appliance = None

        self._draw_room_scene()

        # Appliance inspector
        inspector = tk.Frame(world, bg=PANEL, width=300)
        inspector.pack(side="right", fill="y", padx=(10, 0))
        inspector.pack_propagate(False)
        self.inspector = inspector
        self._draw_inspector()

    def _room_selector(self, parent: tk.Frame, room: str) -> None:
        active = room == self.current_room
        accent = ROOM_META[room]["accent"]

        button = tk.Button(
            parent,
            text=f"  {room}",
            command=lambda r=room: self.select_room(r),
            bg=darken(accent, 0.83) if active else PANEL,
            fg=TEXT if active else MUTED,
            activebackground=darken(accent, 0.76),
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            anchor="w",
            font=(FONT, 9, "bold"),
            padx=8,
            pady=9,
            cursor="hand2",
        )
        button.pack(fill="x", padx=10, pady=3)
        self.room_buttons[room] = button

        if active:
            button.configure(highlightthickness=1, highlightbackground=accent)
        else:
            button.configure(highlightthickness=0)

    def select_room(self, room: str) -> None:
        self.current_room = room
        self.selected_appliance = None
        if self.current_view == "world":
            self.show_energy_world()

    def _update_world_stats(self) -> None:
        for child in self.world_stats.winfo_children():
            child.destroy()

        room_value = self.report.room_totals().get(self.current_room, 0.0)
        active_count = sum(
            1 for app in self.appliances
            if app.room == self.current_room and app.enabled
        )

        tk.Label(
            self.world_stats,
            text="ROOM ENERGY",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w", padx=4)

        tk.Label(
            self.world_stats,
            text=f"{room_value:.2f} kWh",
            bg=PANEL,
            fg=ROOM_META[self.current_room]["accent"],
            font=(FONT, 18, "bold"),
        ).pack(anchor="w", padx=4, pady=(3, 8))

        tk.Label(
            self.world_stats,
            text=f"● {active_count} active appliance(s)",
            bg=PANEL,
            fg=GREEN,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w", padx=4)

    def _draw_room_scene(self) -> None:
        canvas = self.room_canvas
        if canvas is None:
            return

        canvas.delete("all")
        self.appliance_hitboxes.clear()

        w = max(600, canvas.winfo_width())
        h = max(440, canvas.winfo_height())
        meta = ROOM_META[self.current_room]
        accent = meta["accent"]

        # Background glow
        for step in range(8, 0, -1):
            inset = step * 12
            canvas.create_oval(
                w * 0.50 - 280 - inset,
                h * 0.48 - 220 - inset,
                w * 0.50 + 280 + inset,
                h * 0.48 + 220 + inset,
                fill=mix(meta["wall"], meta["ambient"], (9 - step) / 60),
                outline="",
            )

        # Back wall
        wall_y = h * 0.54
        canvas.create_rectangle(
            0, 0, w, wall_y,
            fill=meta["wall"],
            outline="",
        )

        # Subtle wall panels
        for x in range(0, int(w), 70):
            canvas.create_line(
                x, 0, x, wall_y,
                fill=mix(meta["wall"], WHITE, 0.03),
                width=1,
            )

        # Floor perspective
        cx = w * 0.50
        horizon = wall_y
        floor_top = horizon
        floor_bottom = h
        left = w * 0.07
        right = w * 0.93

        canvas.create_polygon(
            left, floor_top,
            right, floor_top,
            w * 0.99, floor_bottom,
            w * 0.01, floor_bottom,
            fill=meta["floor"],
            outline="",
        )

        # Isometric floor grid
        for i in range(1, 8):
            y = floor_top + (floor_bottom - floor_top) * i / 8
            canvas.create_line(
                left + i * 4, y,
                right - i * 4, y,
                fill=mix(meta["floor"], WHITE, 0.07),
            )

        for i in range(-10, 11):
            x = cx + i * 60
            canvas.create_line(
                cx, floor_top,
                x, floor_bottom,
                fill=mix(meta["floor"], WHITE, 0.06),
            )

        # Wall art / window / ambience
        self._draw_room_decor(canvas, w, h)

        # Small room label
        canvas.create_rectangle(
            18, 18, 190, 51,
            fill=darken(accent, 0.76),
            outline=accent,
            width=1,
        )
        canvas.create_text(
            31, 34,
            text=f"◉ {self.current_room.upper()}",
            fill=accent,
            font=(FONT, 9, "bold"),
            anchor="w",
        )

        # Appliance objects
        room_apps = [a for a in self.appliances if a.room == self.current_room]
        for appliance in room_apps:
            px = appliance.position[0] * w
            py = horizon + appliance.position[1] * (h - horizon)
            self._draw_appliance_3d(canvas, appliance, px, py)

        if not room_apps:
            canvas.create_text(
                cx, h * 0.55,
                text="No appliances in this room",
                fill=MUTED,
                font=(FONT, 12),
            )

    def _draw_room_decor(self, canvas: tk.Canvas, w: float, h: float) -> None:
        accent = ROOM_META[self.current_room]["accent"]
        wall_y = h * 0.54

        if self.current_room == "Living Room":
            # Window
            x1, y1, x2, y2 = w * 0.10, h * 0.16, w * 0.32, h * 0.40
            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#0A243A",
                outline=accent,
                width=2,
            )
            canvas.create_line(
                (x1 + x2) / 2, y1,
                (x1 + x2) / 2, y2,
                fill=accent,
                width=1,
            )
            canvas.create_line(
                x1, (y1 + y2) / 2,
                x2, (y1 + y2) / 2,
                fill=accent,
                width=1,
            )

            # Sofa
            self._draw_sofa(canvas, w * 0.18, wall_y * 0.74, 170, 70)

        elif self.current_room == "Kitchen":
            # Cabinets
            canvas.create_rectangle(
                w * 0.08, h * 0.13, w * 0.90, h * 0.29,
                fill="#31263A",
                outline=ORANGE,
            )
            for i in range(4):
                x1 = w * 0.08 + i * (w * 0.82 / 4)
                x2 = w * 0.08 + (i + 1) * (w * 0.82 / 4)
                canvas.create_rectangle(
                    x1 + 3, h * 0.14, x2 - 3, h * 0.28,
                    fill="#382C3A",
                    outline="#583B42",
                )
                canvas.create_oval(
                    (x1 + x2) / 2 - 2, h * 0.20 - 2,
                    (x1 + x2) / 2 + 2, h * 0.20 + 2,
                    fill=ORANGE,
                    outline="",
                )

        elif self.current_room == "Bedroom":
            # Bed headboard
            canvas.create_rectangle(
                w * 0.35, h * 0.15, w * 0.72, h * 0.45,
                fill="#33275C",
                outline=PURPLE,
                width=2,
            )
            # Pillow
            canvas.create_rectangle(
                w * 0.42, h * 0.26, w * 0.54, h * 0.35,
                fill="#5A4A86",
                outline="",
            )
            canvas.create_rectangle(
                w * 0.56, h * 0.26, w * 0.68, h * 0.35,
                fill="#5A4A86",
                outline="",
            )

        elif self.current_room == "Study":
            # Bookshelf
            canvas.create_rectangle(
                w * 0.08, h * 0.12, w * 0.27, h * 0.49,
                fill="#244C3B",
                outline=GREEN,
                width=1,
            )
            for row in range(4):
                y = h * 0.19 + row * h * 0.075
                canvas.create_line(
                    w * 0.10, y, w * 0.25, y,
                    fill="#3E8063",
                    width=2,
                )
                for col in range(5):
                    x = w * 0.11 + col * 25
                    canvas.create_line(
                        x, y - 15, x, y - 2,
                        fill=[CYAN, ORANGE, PURPLE, YELLOW, PINK][col],
                        width=3,
                    )

        canvas.create_line(
            0, wall_y, w, wall_y,
            fill=mix(accent, WHITE, 0.12),
            width=2,
        )

    def _draw_sofa(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        canvas.create_rectangle(
            x + 10, y + 18,
            x + width, y + height,
            fill="#173C50",
            outline=CYAN,
            width=1,
        )
        canvas.create_rectangle(
            x, y,
            x + width - 14, y + height * 0.55,
            fill="#1B4D62",
            outline=CYAN,
            width=1,
        )
        canvas.create_rectangle(
            x - 10, y + 12,
            x + 10, y + height,
            fill="#194359",
            outline=CYAN,
        )
        canvas.create_text(
            x + width / 2,
            y + 38,
            text="SOFA",
            fill="#73CFE3",
            font=(FONT, 8, "bold"),
        )

    def _draw_appliance_3d(
        self,
        canvas: tk.Canvas,
        appliance: Appliance,
        x: float,
        y: float,
    ) -> None:
        selected = self.selected_appliance is appliance
        accent = appliance.color
        active = appliance.enabled
        scale = 1.0

        # Shadow
        canvas.create_oval(
            x - 48, y + 26,
            x + 48, y + 48,
            fill="#08101A",
            outline="",
        )

        if appliance.icon == "TV":
            self._draw_tv(canvas, x, y, accent, selected, active)
        elif appliance.icon == "FR":
            self._draw_refrigerator(canvas, x, y, accent, selected, active)
        elif appliance.icon in {"LAMP"}:
            self._draw_lamp(canvas, x, y, accent, selected, active)
        elif appliance.icon == "PC":
            self._draw_laptop(canvas, x, y, accent, selected, active)
        elif appliance.icon in {"FAN"}:
            self._draw_fan(canvas, x, y, accent, selected, active)
        elif appliance.icon in {"AC"}:
            self._draw_ac(canvas, x, y, accent, selected, active)
        elif appliance.icon == "MW":
            self._draw_box_appliance(canvas, x, y, accent, selected, active, "MW")
        elif appliance.icon == "IND":
            self._draw_stove(canvas, x, y, accent, selected, active)
        elif appliance.icon == "COOL":
            self._draw_cooler(canvas, x, y, accent, selected, active)
        else:
            self._draw_box_appliance(
                canvas, x, y, accent, selected, active, appliance.icon
            )

        # Floating name plate
        label_bg = darken(accent, 0.79) if active else "#172331"
        width = max(70, 34 + len(appliance.name) * 4.2)

        rounded_rect(
            canvas,
            x - width / 2,
            y + 48,
            x + width / 2,
            y + 73,
            8,
            label_bg,
            accent if selected else "",
            1,
        )
        canvas.create_text(
            x,
            y + 60,
            text=appliance.name,
            fill=TEXT if active else MUTED,
            font=(FONT, 8, "bold"),
        )

        # Energy pulse
        if active:
            pulse = (math.sin(self.animation_phase * 2.2) + 1) / 2
            r = 2 + pulse * 3
            canvas.create_oval(
                x + width / 2 - 12 - r,
                y + 60 - r,
                x + width / 2 - 12 + r,
                y + 60 + r,
                fill=accent,
                outline="",
            )

        # Hitbox
        half_w = max(52, width / 2)
        self.appliance_hitboxes.append(
            ((x - half_w, y - 58, x + half_w, y + 74), appliance)
        )

    def _draw_tv(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        glow = color if active else "#314254"
        outline = WHITE if selected else color if active else "#3C5268"

        canvas.create_polygon(
            x - 72, y - 48,
            x + 57, y - 42,
            x + 57, y + 18,
            x - 72, y + 10,
            fill=SHADOW,
            outline="",
        )
        canvas.create_polygon(
            x - 78, y - 54,
            x + 51, y - 48,
            x + 64, y - 38,
            x - 65, y - 44,
            fill="#1A2D43",
            outline=outline,
            width=2,
        )
        canvas.create_polygon(
            x - 65, y - 44,
            x + 38, y - 39,
            x + 38, y + 4,
            x - 65, y - 1,
            fill=darken(glow, 0.48),
            outline=color if active else "#304457",
        )
        canvas.create_line(
            x - 8, y + 5, x + 16, y + 10,
            fill=color if active else "#40546A", width=3
        )
        canvas.create_line(
            x + 4, y + 10, x + 12, y + 25,
            fill="#5C7187", width=2
        )

    def _draw_refrigerator(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        outline = WHITE if selected else color if active else "#3C5268"

        canvas.create_polygon(
            x - 43, y - 62,
            x + 31, y - 55,
            x + 45, y + 25,
            x - 29, y + 33,
            fill="#102130",
            outline=outline,
            width=2,
        )
        canvas.create_polygon(
            x - 29, y - 55,
            x + 31, y - 49,
            x + 31, y + 22,
            x - 29, y + 28,
            fill=darken(color, 0.55),
            outline="",
        )
        canvas.create_line(
            x - 29, y - 12,
            x + 31, y - 7,
            fill="#426078",
            width=2,
        )
        canvas.create_line(
            x + 6, y - 39,
            x + 6, y - 26,
            fill=color if active else "#536A7B",
            width=3,
        )

    def _draw_lamp(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        glow = color if active else "#435063"
        outline = WHITE if selected else color if active else "#48596B"

        if active:
            for r, alpha in [(30, 0.86), (23, 0.80), (17, 0.70)]:
                canvas.create_oval(
                    x - r, y - 45 - r / 3,
                    x + r, y - 45 + r / 3,
                    fill=darken(glow, alpha),
                    outline="",
                )

        canvas.create_polygon(
            x - 30, y - 54,
            x + 30, y - 54,
            x + 19, y - 21,
            x - 19, y - 21,
            fill=darken(glow, 0.35),
            outline=outline,
            width=2,
        )
        canvas.create_line(
            x, y - 21, x, y + 18,
            fill="#A8BBD0", width=3
        )
        canvas.create_line(
            x - 19, y + 18, x + 19, y + 18,
            fill="#A8BBD0", width=4
        )

    def _draw_laptop(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        outline = WHITE if selected else color if active else "#3C5268"

        canvas.create_polygon(
            x - 42, y - 51,
            x + 32, y - 47,
            x + 30, y - 3,
            x - 42, y - 6,
            fill="#17283B",
            outline=outline,
            width=2,
        )
        canvas.create_polygon(
            x - 31, y - 42,
            x + 22, y - 39,
            x + 22, y - 11,
            x - 31, y - 14,
            fill=darken(color, 0.42) if active else "#152637",
            outline="",
        )
        canvas.create_polygon(
            x - 54, y - 5,
            x + 43, y - 1,
            x + 59, y + 13,
            x - 38, y + 10,
            fill="#2A4057",
            outline=outline,
            width=2,
        )

    def _draw_fan(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        outline = WHITE if selected else color if active else "#465A6E"
        cx, cy = x, y - 34

        for angle in range(0, 360, 120):
            rad = math.radians(angle + self.animation_phase * 55)
            px = cx + math.cos(rad) * 35
            py = cy + math.sin(rad) * 35
            canvas.create_polygon(
                cx, cy,
                px + math.cos(rad + 0.7) * 10,
                py + math.sin(rad + 0.7) * 10,
                px, py,
                px + math.cos(rad - 0.7) * 10,
                py + math.sin(rad - 0.7) * 10,
                fill=darken(color, 0.30 if active else 0.70),
                outline=outline,
            )

        canvas.create_oval(
            cx - 9, cy - 9, cx + 9, cy + 9,
            fill="#D5E4EF" if active else "#53687A",
            outline=outline,
        )
        canvas.create_line(
            x, cy + 9, x, y + 19,
            fill="#687E91", width=3
        )

    def _draw_ac(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        outline = WHITE if selected else color if active else "#465A6E"

        canvas.create_polygon(
            x - 56, y - 43,
            x + 50, y - 40,
            x + 55, y - 6,
            x - 50, y - 9,
            fill="#15273A",
            outline=outline,
            width=2,
        )

        for i in range(5):
            xx = x - 35 + i * 17
            canvas.create_line(
                xx, y - 25, xx + 10, y - 24,
                fill=color if active else "#42596D",
                width=2,
            )

        if active:
            canvas.create_text(
                x + 28, y - 30,
                text="❄",
                fill=CYAN,
                font=("Segoe UI Emoji", 10),
            )

    def _draw_box_appliance(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
        text: str,
    ) -> None:
        outline = WHITE if selected else color if active else "#465A6E"

        canvas.create_polygon(
            x - 48, y - 43,
            x + 35, y - 48,
            x + 47, y + 19,
            x - 38, y + 24,
            fill="#17283A",
            outline=outline,
            width=2,
        )
        canvas.create_polygon(
            x - 37, y - 32,
            x + 25, y - 36,
            x + 25, y + 10,
            x - 33, y + 13,
            fill=darken(color, 0.49) if active else "#152535",
            outline="",
        )
        canvas.create_text(
            x - 4, y - 10,
            text=text,
            fill=color if active else "#607489",
            font=(FONT, 10, "bold"),
        )

    def _draw_stove(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        outline = WHITE if selected else color if active else "#465A6E"

        canvas.create_polygon(
            x - 60, y - 32,
            x + 43, y - 37,
            x + 53, y + 10,
            x - 49, y + 15,
            fill="#172A3A",
            outline=outline,
            width=2,
        )

        for dx, dy, r in [(-25, -12, 13), (13, -13, 13), (-21, 2, 11), (18, 2, 11)]:
            canvas.create_oval(
                x + dx - r,
                y + dy - r / 2,
                x + dx + r,
                y + dy + r / 2,
                fill=darken(RED if active else "#4C5765", 0.22),
                outline=RED if active else "#617083",
                width=2,
            )

    def _draw_cooler(
        self,
        canvas: tk.Canvas,
        x: float,
        y: float,
        color: str,
        selected: bool,
        active: bool,
    ) -> None:
        outline = WHITE if selected else color if active else "#465A6E"

        canvas.create_polygon(
            x - 35, y - 46,
            x + 30, y - 41,
            x + 34, y + 22,
            x - 40, y + 16,
            fill="#173143",
            outline=outline,
            width=2,
        )
        canvas.create_oval(
            x - 20, y - 25,
            x + 17, y + 8,
            fill=darken(CYAN if active else "#5B6978", 0.46),
            outline=CYAN if active else "#657487",
            width=2,
        )
        for angle in range(0, 360, 90):
            rad = math.radians(angle + self.animation_phase * 40)
            x2 = x + math.cos(rad) * 16
            y2 = y - 8 + math.sin(rad) * 16
            canvas.create_line(
                x, y - 8, x2, y2,
                fill=CYAN if active else "#748292",
                width=2,
            )

    def _room_motion(self, event: tk.Event) -> None:
        if self.room_canvas is None:
            return

        hovered = None
        for (x1, y1, x2, y2), appliance in self.appliance_hitboxes:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                hovered = appliance
                break

        self.room_canvas.configure(cursor="hand2" if hovered else "arrow")

        if hovered:
            self.scene_status.set(
                f"{hovered.name}  •  {hovered.power_w:.0f} W  •  "
                f"{hovered.usage_hours:.1f} h/day  •  "
                f"{hovered.daily_kwh():.2f} kWh/day"
            )
        else:
            self.scene_status.set(
                f"Explore {self.current_room} — click an appliance for details."
            )

    def _room_click(self, event: tk.Event) -> None:
        for (x1, y1, x2, y2), appliance in self.appliance_hitboxes:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_appliance = appliance
                self._draw_room_scene()
                self._draw_inspector()
                return

    # -------------------------------------------------------------------------
    # INSPECTOR
    # -------------------------------------------------------------------------

    def _draw_inspector(self) -> None:
        if not hasattr(self, "inspector"):
            return

        for child in self.inspector.winfo_children():
            child.destroy()

        if not self.selected_appliance:
            tk.Label(
                self.inspector,
                text="◉  APPLIANCE INSPECTOR",
                bg=PANEL,
                fg=CYAN,
                font=(FONT, 9, "bold"),
            ).pack(anchor="w", padx=18, pady=(20, 8))

            tk.Label(
                self.inspector,
                text="Pick an object",
                bg=PANEL,
                fg=TEXT,
                font=(FONT, 18, "bold"),
            ).pack(anchor="w", padx=18)

            tk.Label(
                self.inspector,
                text="Click any 3D appliance in the room to see its energy profile, power draw and controls.",
                bg=PANEL,
                fg=MUTED,
                font=(FONT, 9),
                justify="left",
                wraplength=250,
            ).pack(anchor="w", padx=18, pady=(8, 16))

            for icon, title, desc, color in [
                ("🖱", "Explore", "Click objects to inspect them.", CYAN),
                ("⚡", "Tune", "Change usage hours and switch loads.", YELLOW),
                ("💡", "Act", "Apply the recommendations to lower consumption.", GREEN),
            ]:
                row = tk.Frame(self.inspector, bg=PANEL_2)
                row.pack(fill="x", padx=16, pady=5)

                tk.Label(
                    row,
                    text=icon,
                    bg=PANEL_2,
                    fg=color,
                    font=("Segoe UI Emoji", 14),
                ).pack(side="left", padx=10, pady=9)

                txt = tk.Frame(row, bg=PANEL_2)
                txt.pack(side="left", fill="x", expand=True, pady=8)

                tk.Label(
                    txt,
                    text=title,
                    bg=PANEL_2,
                    fg=TEXT,
                    font=(FONT, 9, "bold"),
                ).pack(anchor="w")

                tk.Label(
                    txt,
                    text=desc,
                    bg=PANEL_2,
                    fg=MUTED,
                    font=(FONT, 8),
                    wraplength=185,
                    justify="left",
                ).pack(anchor="w")

            return

        app = self.selected_appliance

        top = tk.Frame(self.inspector, bg=PANEL)
        top.pack(fill="x", padx=18, pady=(18, 4))

        tk.Label(
            top,
            text=app.icon,
            bg=darken(app.color, 0.72),
            fg=app.color,
            font=(FONT, 13, "bold"),
            padx=10,
            pady=6,
        ).pack(side="left")

        info = tk.Frame(top, bg=PANEL)
        info.pack(side="left", padx=10)

        tk.Label(
            info,
            text=app.name,
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 15, "bold"),
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f"{app.room}  •  {app.category}",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8),
        ).pack(anchor="w")

        tk.Label(
            self.inspector,
            text=app.description,
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 9),
            justify="left",
            wraplength=252,
        ).pack(anchor="w", padx=18, pady=(5, 16))

        stats = tk.Frame(self.inspector, bg=PANEL_2)
        stats.pack(fill="x", padx=16, pady=2)

        stats.columnconfigure(0, weight=1)
        stats.columnconfigure(1, weight=1)

        values = [
            ("POWER", f"{app.power_w:.0f} W", app.color),
            ("DAILY ENERGY", f"{app.daily_kwh():.2f} kWh", CYAN),
            ("DAILY COST", f"₹{app.daily_kwh() * self.electricity_rate:.2f}", YELLOW),
            ("CO₂ / DAY", f"{app.daily_kwh() * self.emission_factor:.2f} kg", GREEN),
        ]

        for i, (label, value, color) in enumerate(values):
            r, c = divmod(i, 2)
            box = tk.Frame(stats, bg=PANEL_2)
            box.grid(row=r, column=c, sticky="ew", padx=8, pady=8)

            tk.Label(
                box,
                text=label,
                bg=PANEL_2,
                fg=MUTED,
                font=(FONT, 7, "bold"),
            ).pack(anchor="w")

            tk.Label(
                box,
                text=value,
                bg=PANEL_2,
                fg=color,
                font=(FONT, 11, "bold"),
            ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            self.inspector,
            text="USAGE HOURS / DAY",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 4))

        slider_value = tk.DoubleVar(value=app.usage_hours)

        slider = tk.Scale(
            self.inspector,
            from_=0,
            to=24,
            resolution=0.5,
            orient="horizontal",
            variable=slider_value,
            showvalue=False,
            bg=PANEL,
            fg=TEXT,
            highlightthickness=0,
            troughcolor=PANEL_3,
            activebackground=app.color,
            sliderrelief="flat",
            command=lambda value, a=app: self._change_usage(
                a, float(value)
            ),
        )
        slider.pack(fill="x", padx=16)

        self.usage_value_label = tk.Label(
            self.inspector,
            text=f"{app.usage_hours:.1f} hours",
            bg=PANEL,
            fg=app.color,
            font=(FONT, 18, "bold"),
        )
        self.usage_value_label.pack(anchor="w", padx=18, pady=(2, 10))

        button_row = tk.Frame(self.inspector, bg=PANEL)
        button_row.pack(fill="x", padx=16, pady=6)

        toggle_text = "⏻  TURN OFF" if app.enabled else "●  TURN ON"
        toggle_color = RED if app.enabled else GREEN

        toggle = tk.Button(
            button_row,
            text=toggle_text,
            command=lambda a=app: self._toggle_appliance(a),
            bg=darken(toggle_color, 0.77),
            fg=toggle_color,
            activebackground=darken(toggle_color, 0.66),
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            font=(FONT, 9, "bold"),
            padx=12,
            pady=9,
            cursor="hand2",
        )
        toggle.pack(side="left", fill="x", expand=True, padx=(0, 5))

        focus = tk.Button(
            button_row,
            text="⚡ MAX IMPACT",
            command=lambda a=app: self._focus_app(a),
            bg=darken(CYAN, 0.82),
            fg=CYAN,
            activebackground=darken(CYAN, 0.72),
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            font=(FONT, 9, "bold"),
            padx=10,
            pady=9,
            cursor="hand2",
        )
        focus.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # mini bar
        canvas = tk.Canvas(
            self.inspector,
            bg=PANEL,
            height=70,
            highlightthickness=0,
        )
        canvas.pack(fill="x", padx=16, pady=14)
        self._draw_appliance_meter(canvas, app)

    def _draw_appliance_meter(self, canvas: tk.Canvas, app: Appliance) -> None:
        canvas.delete("all")
        canvas.create_text(
            0, 4,
            text="RELATIVE DAILY LOAD",
            fill=MUTED,
            font=(FONT, 8, "bold"),
            anchor="nw",
        )

        max_value = max(
            (a.daily_kwh() for a in self.appliances if a.enabled),
            default=1.0,
        )
        ratio = app.daily_kwh() / max_value if max_value else 0

        rounded_rect(
            canvas,
            0, 28,
            260, 45,
            8,
            PANEL_3,
        )
        rounded_rect(
            canvas,
            0, 28,
            max(8, 260 * ratio), 45,
            8,
            app.color if app.enabled else "#3A495A",
        )
        canvas.create_text(
            260, 35,
            text=f"{ratio * 100:.0f}%",
            fill=TEXT,
            font=(FONT, 9, "bold"),
            anchor="e",
        )

    def _change_usage(self, appliance: Appliance, hours: float) -> None:
        appliance.usage_hours = max(0.0, min(24.0, hours))
        for record in self.records:
            if record.appliance is appliance:
                record.usage_hours = appliance.usage_hours
        self._recalculate()

        if self.selected_appliance is appliance and hasattr(
            self, "usage_value_label"
        ):
            self.usage_value_label.configure(
                text=f"{appliance.usage_hours:.1f} hours"
            )

        self._refresh_active_view()

    def _toggle_appliance(self, appliance: Appliance) -> None:
        appliance.enabled = not appliance.enabled
        self._recalculate()
        self._refresh_active_view()
        self._draw_inspector()

    def _focus_app(self, appliance: Appliance) -> None:
        self.selected_appliance = appliance
        self.current_room = appliance.room
        if self.current_view != "world":
            self.show_energy_world()
        else:
            self._draw_room_scene()
            self._draw_inspector()

    def _refresh_active_view(self) -> None:
        if self.current_view == "dashboard":
            self.show_dashboard()
        elif self.current_view == "world":
            self._draw_room_scene()
            self._update_world_stats()
            self._draw_inspector()
        elif self.current_view == "insights":
            self.show_insights()

    # -------------------------------------------------------------------------
    # INSIGHTS
    # -------------------------------------------------------------------------

    def show_insights(self) -> None:
        self.current_view = "insights"
        self.set_nav("insights")
        self.clear_body()

        self.make_header(
            self.body,
            "Energy Insights",
            "Turn the raw numbers into clear actions for your home.",
            PURPLE,
        )

        content = tk.Frame(self.body, bg=BG)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        left = tk.Frame(content, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        right = tk.Frame(content, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self._insights_ranking(left)
        self._insights_recommendations(right)

    def _insights_ranking(self, parent: tk.Widget) -> None:
        self.section_title(
            parent,
            "🔥 Consumption Leaderboard",
            "Highest estimated daily energy use",
            RED,
        )

        panel = tk.Frame(parent, bg=PANEL)
        panel.pack(fill="both", expand=True)

        ranking = self.report.appliance_usage()
        max_energy = ranking[0][1] if ranking else 1

        for idx, (app, energy) in enumerate(ranking, start=1):
            row = tk.Frame(panel, bg=PANEL)
            row.pack(fill="x", padx=16, pady=(10 if idx == 1 else 5, 5))

            badge = tk.Label(
                row,
                text=str(idx),
                bg=darken(app.color, 0.80),
                fg=app.color,
                font=(MONO, 9, "bold"),
                width=3,
                pady=5,
            )
            badge.pack(side="left")

            center = tk.Frame(row, bg=PANEL)
            center.pack(side="left", fill="x", expand=True, padx=9)

            line = tk.Frame(center, bg=PANEL)
            line.pack(fill="x")

            tk.Label(
                line,
                text=app.name,
                bg=PANEL,
                fg=TEXT,
                font=(FONT, 9, "bold"),
            ).pack(side="left")

            tk.Label(
                line,
                text=app.room,
                bg=PANEL,
                fg=MUTED,
                font=(FONT, 8),
            ).pack(side="right")

            track = tk.Frame(center, bg=PANEL_3, height=8)
            track.pack(fill="x", pady=(5, 0))
            track.pack_propagate(False)

            fill = tk.Frame(
                track,
                bg=app.color,
                width=max(4, int(240 * energy / max_energy)),
            )
            fill.pack(side="left", fill="y")

            tk.Label(
                row,
                text=f"{energy:.2f} kWh",
                bg=PANEL,
                fg=TEXT,
                font=(MONO, 9, "bold"),
                width=11,
                anchor="e",
            ).pack(side="right")

    def _insights_recommendations(self, parent: tk.Widget) -> None:
        self.section_title(
            parent,
            "💡 Action Plan",
            "Practical ideas generated from the current model",
            GREEN,
        )

        panel = tk.Frame(parent, bg=PANEL)
        panel.pack(fill="both", expand=True)

        recommendations = RecommendationEngine.build(self.report)
        colors = [RED, CYAN, ORANGE, GREEN]

        for idx, (tag, title, description) in enumerate(recommendations):
            color = colors[idx % len(colors)]

            box = tk.Frame(
                panel,
                bg=darken(color, 0.84),
            )
            box.pack(fill="x", padx=14, pady=8)

            top = tk.Frame(box, bg=darken(color, 0.84))
            top.pack(fill="x", padx=12, pady=(10, 5))

            tk.Label(
                top,
                text=tag,
                bg=darken(color, 0.84),
                fg=color,
                font=(FONT, 8, "bold"),
            ).pack(side="left")

            tk.Label(
                top,
                text=title,
                bg=darken(color, 0.84),
                fg=TEXT,
                font=(FONT, 10, "bold"),
            ).pack(side="right")

            tk.Label(
                box,
                text=description,
                bg=darken(color, 0.84),
                fg=MUTED,
                font=(FONT, 8),
                justify="left",
                wraplength=490,
            ).pack(anchor="w", padx=12, pady=(0, 11))

        self._insight_score(panel)

    def _insight_score(self, parent: tk.Frame) -> None:
        # Simple illustrative score based on relative daily load.
        score = max(
            15,
            min(98, 100 - self.report.total_kwh * 3.2)
        )
        score = round(score)

        box = tk.Frame(parent, bg=PANEL_2)
        box.pack(fill="x", padx=14, pady=(10, 14))

        left = tk.Frame(box, bg=PANEL_2)
        left.pack(side="left", padx=14, pady=12)

        tk.Label(
            left,
            text="🌱",
            bg=PANEL_2,
            fg=GREEN,
            font=("Segoe UI Emoji", 20),
        ).pack(side="left")

        tx = tk.Frame(left, bg=PANEL_2)
        tx.pack(side="left", padx=10)

        tk.Label(
            tx,
            text="GreenGrid Efficiency Pulse",
            bg=PANEL_2,
            fg=TEXT,
            font=(FONT, 9, "bold"),
        ).pack(anchor="w")

        tk.Label(
            tx,
            text="Illustrative score for the current prototype profile.",
            bg=PANEL_2,
            fg=MUTED,
            font=(FONT, 7),
        ).pack(anchor="w")

        tk.Label(
            box,
            text=f"{score}",
            bg=PANEL_2,
            fg=GREEN,
            font=(FONT, 24, "bold"),
        ).pack(side="right", padx=18)

    # -------------------------------------------------------------------------
    # ANIMATION
    # -------------------------------------------------------------------------

    def _animate(self) -> None:
        self.animation_phase += 0.08

        if self.current_view == "world" and self.room_canvas is not None:
            self._draw_room_scene()

        # Animate status dot subtly.
        if hasattr(self, "live_dot"):
            pulse = (math.sin(self.animation_phase * 2.0) + 1) / 2
            self.live_dot.configure(
                fg=mix(GREEN, WHITE, pulse * 0.25)
            )

        # Clock
        from datetime import datetime
        now = datetime.now().strftime("%a • %I:%M %p")
        self.datetime_label.configure(text=now)

        self._animation_job = self.after(55, self._animate)


# =============================================================================
# ENTRY POINT
# =============================================================================

def main() -> None:
    app = GreenGridApp()
    app.mainloop()


if __name__ == "__main__":
    main()
