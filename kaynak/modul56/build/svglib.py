"""Broadsheet-style SVG helpers for mechanism diagrams (mekanizma-semasi.md rules)."""
import html

NEU = "var(--color-neutral-700)"
TXT = "var(--color-text)"
CYAN = "var(--color-accent-700)"
MAG = "var(--color-accent-2-900)"
FONT = 'font-family="var(--font-body)"'


def esc(s):
    return html.escape(str(s), quote=False)


class SVG:
    def __init__(self, w, h, label, mid):
        self.w, self.h, self.label, self.mid = w, h, label, mid
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def marker(self):
        d = []
        for suf, col in (("", NEU), ("c", CYAN), ("m", MAG)):
            d.append(f'<marker id="{self.mid}{suf}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
                     f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
        return "<defs>" + "".join(d) + "</defs>"

    def _m(self, color):
        return {CYAN: "c", MAG: "m"}.get(color, "")

    def box(self, x, y, w, h, lines, kind="normal", align="middle", title_bold=True, fs1=12.5, fs2=11, lh=15, pad_top=None, fill="white"):
        """lines: list of str or (str, style) ; style in {'title','sub','cyan','mag','bold','ital'}"""
        if kind == "key":
            stroke = f'stroke="{CYAN}" stroke-width="1.5"'
        elif kind == "mag":
            stroke = f'stroke="{MAG}" stroke-width="1.5"'
        elif kind == "none":
            stroke = 'stroke="none"'
        else:
            stroke = f'stroke="{NEU}" stroke-opacity="0.35" stroke-width="1"'
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" {stroke}/>')
        n = len(lines)
        total = fs1 + (n - 1) * lh
        y0 = y + (h - total) / 2 + fs1 * 0.8 if pad_top is None else y + pad_top
        if align == "middle":
            tx, anchor = x + w / 2, "middle"
        else:
            tx, anchor = x + 10, "start"
        for i, ln in enumerate(lines):
            if isinstance(ln, tuple):
                t, st = ln
            else:
                t, st = ln, ("title" if i == 0 else "sub")
            self.text(tx, y0 + i * lh, t, st, anchor, fs1, fs2)

    def text(self, x, y, t, st="sub", anchor="start", fs1=12.5, fs2=11, rotate=None):
        attrs = {"title": (fs1, TXT, "700", "normal"),
                 "plain": (fs1, TXT, "400", "normal"),
                 "sub": (fs2, NEU, "400", "normal"),
                 "body": (fs2, TXT, "400", "normal"),
                 "cyan": (fs2, CYAN, "400", "italic"),
                 "cyanb": (fs2, CYAN, "700", "normal"),
                 "mag": (fs2, MAG, "400", "italic"),
                 "magb": (fs2, MAG, "700", "normal"),
                 "cap": (10, NEU, "700", "normal"),
                 "small": (10, NEU, "400", "normal")}
        fs, col, wt, style = attrs[st]
        extra = ' letter-spacing="0.08em"' if st == "cap" else ""
        rot = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {FONT} font-size="{fs}" '
                 f'font-weight="{wt}" font-style="{style}" fill="{col}" xml:space="preserve"{extra}{rot}>{esc(t)}</text>')

    def arrow(self, x1, y1, x2, y2, color=NEU, marker=True, width=1.5):
        m = f' marker-end="url(#{self.mid}{self._m(color)})"' if marker else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{m}/>')

    def path(self, d, color=NEU, marker=True, width=1.5, fill="none"):
        m = f' marker-end="url(#{self.mid}{self._m(color)})"' if marker else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"{m}/>')

    def block(self, x, y, length=28, color=MAG):
        """magenta blocking bar across a vertical arrow at (x,y)"""
        self.add(f'<line x1="{x-length/2}" y1="{y}" x2="{x+length/2}" y2="{y}" stroke="{color}" stroke-width="2.5"/>')

    def render(self):
        body = "\n  ".join(self.parts)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" width="100%" style="display:block" role="img" '
                f'aria-label="{esc(self.label)}">\n  {self.marker()}\n  {body}\n</svg>')

    def save(self, path):
        open(path, "w").write(self.render())
