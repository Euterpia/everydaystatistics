#!/usr/bin/env python3
"""Compose the Everyday Statistics social-share (OG) image.

A 1200x630 raster card, on-brand with the site palette (paper / ink / gold) and
the real hero headline + tagline. Raster JPG so Facebook, LinkedIn, WhatsApp, X,
iMessage and Slack render a preview (SVG never previews on those platforms).

Run with the SEO venv interpreter:
    ~/.claude/skills/seo/.venv/bin/python tools/make_og_image.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (244, 236, 221)        # --paper        #F4ECDD
PAPER_RAISED = (248, 241, 226) # --paper-raised #F8F1E2
INK = (42, 37, 32)             # --ink          #2A2520
INK_SOFT = (74, 64, 54)        # --ink-soft     #4A4036
INK_MUTE = (122, 110, 94)      # --ink-mute     #7A6E5E
GOLD = (176, 138, 62)          # --gold         #B08A3E
GOLD_DEEP = (142, 110, 44)     # --gold-deep    #8E6E2C

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_ITALIC = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_tracked(draw, xy, text, fnt, fill, tracking, anchor_center_x=None):
    """Draw letter-spaced text. If anchor_center_x given, centre the whole run."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (anchor_center_x - total / 2) if anchor_center_x is not None else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Subtle raised inner panel + gold hairline frame
margin = 38
d.rectangle([margin, margin, W - margin, H - margin], fill=PAPER_RAISED, outline=GOLD, width=2)
inner = margin + 16
d.rectangle([inner, inner, W - inner, H - inner], outline=GOLD, width=1)

cx = W // 2

# Eyebrow label
draw_tracked(d, (0, 118), "STATISTICAL SELF-DEFENCE", font(SANS_BOLD, 22), GOLD_DEEP, 7, anchor_center_x=cx)

# Title (two lines: roman then italic)
title1 = font(SERIF, 76)
title2 = font(SERIF_ITALIC, 76)
d.text((cx, 196), "How to read a number", font=title1, fill=INK, anchor="ma")
d.text((cx, 286), "without being lied to.", font=title2, fill=INK, anchor="ma")

# Gold rule
rule_w = 120
d.line([cx - rule_w // 2, 398, cx + rule_w // 2, 398], fill=GOLD, width=2)

# Subtitle / tagline (the meta description)
sub = font(SERIF, 30)
d.text((cx, 424), "Statistical literacy for everyone. Free.", font=sub, fill=INK_SOFT, anchor="ma")
d.text((cx, 466), "No prior knowledge required.", font=sub, fill=INK_SOFT, anchor="ma")

# Footer line
draw_tracked(d, (0, 548), "EVERYDAYSTATISTICS.COM", font(SANS_BOLD, 18), INK_MUTE, 4, anchor_center_x=cx)

img.save("public/og-image.jpg", "JPEG", quality=88, optimize=True)
print("Wrote public/og-image.jpg", img.size)
