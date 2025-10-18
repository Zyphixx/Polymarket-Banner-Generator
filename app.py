from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64

app = Flask(__name__)

TEMPLATES_DIR = "static"
FONTS_DIR = "fonts"
FONT_PATH = os.path.join(FONTS_DIR, "Syne-Bold.ttf")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    nickname = data.get("nickname", "").strip()
    twitter = data.get("twitter", "").strip()
    template_id = data.get("template", "1").strip()

    template_path = os.path.join(TEMPLATES_DIR, f"poly{template_id}.png")
    if not os.path.exists(template_path):
        return jsonify({"error": f"Template poly{template_id}.png not found"}), 404

    # ⚡ Add .POLY suffix in uppercase
    nickname_full = f"{nickname}.POLY"

    # Load image in RGBA mode — lossless quality
    img = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Main fonts
    font_big = ImageFont.truetype(FONT_PATH, 140)
    font_small = ImageFont.truetype(FONT_PATH, 40)

    # --- 1️⃣ poly1 ---
    if template_id == "1":
        bbox_nick = draw.textbbox((0, 0), nickname_full, font=font_big)
        text_height = bbox_nick[3] - bbox_nick[1]
        top_margin = 166
        bottom_margin = 166
        nickname_y = (h - bottom_margin + top_margin - text_height) / 2
        nickname_x = w / 2
        draw.text(
            (nickname_x, nickname_y),
            nickname_full,
            font=font_big,
            fill="white",
            anchor="ma",
        )

        # Twitter ID — slightly above nickname (+7 pixels)
        twitter_x = (w / 2) - ((bbox_nick[2] - bbox_nick[0]) / 2)
        twitter_y = nickname_y - 14
        draw.text(
            (twitter_x, twitter_y),
            f"@{twitter}",
            font=font_small,
            fill="#FFFFFF",
            anchor="la",
        )

    # --- 2️⃣ poly2 ---
    elif template_id == "2":
        font_big = ImageFont.truetype(FONT_PATH, 140)
        font_small = ImageFont.truetype(FONT_PATH, 40)

        top_nick = 282
        bottom_nick = 50
        right_nick = 70

        top_twitter = 305
        bottom_twitter = 188
        right_twitter = 70

        bbox_nick = draw.textbbox((0, 0), nickname_full, font=font_big)
        text_height_nick = bbox_nick[3] - bbox_nick[1]
        nickname_y = (h - bottom_nick + top_nick - text_height_nick) / 2
        nickname_x = w - right_nick
        draw.text(
            (nickname_x, nickname_y),
            nickname_full,
            font=font_big,
            fill="white",
            anchor="ra",
        )

        # Twitter ID — slightly below nickname (+7 pixels)
        bbox_twitter = draw.textbbox((0, 0), f"@{twitter}", font=font_small)
        text_height_twitter = bbox_twitter[3] - bbox_twitter[1]
        twitter_y = (h - bottom_twitter + top_twitter - text_height_twitter) / 2 + 7
        twitter_x = w - right_twitter
        draw.text(
            (twitter_x, twitter_y),
            f"@{twitter}",
            font=font_small,
            fill="#FFFFFF",
            anchor="ra",
        )

    # --- 3️⃣ poly3 ---
    elif template_id == "3":
        bbox_nick = draw.textbbox((0, 0), nickname_full, font=font_big)
        text_height_nick = bbox_nick[3] - bbox_nick[1]
        top_nick = 166
        bottom_nick = 166
        nickname_y = (h - bottom_nick + top_nick - text_height_nick) / 2
        nickname_x = w / 2
        draw.text(
            (nickname_x, nickname_y),
            nickname_full,
            font=font_big,
            fill="white",
            anchor="ma",
        )

        bbox_twitter = draw.textbbox((0, 0), f"@{twitter}", font=font_small)
        text_height_twitter = bbox_twitter[3] - bbox_twitter[1]
        top_twitter = 210
        bottom_twitter = 304
        twitter_y = (h - bottom_twitter + top_twitter - text_height_twitter) / 2
        twitter_x = (w / 2) - ((bbox_nick[2] - bbox_nick[0]) / 2)
        draw.text(
            (twitter_x, twitter_y),
            f"@{twitter}",
            font=font_small,
            fill="#FFFFFF",
            anchor="la",
        )

    # --- 4️⃣ Save PNG with maximum quality ---
    buf = io.BytesIO()
    img.save(
        buf,
        format="PNG",
        dpi=(300, 300),  # 🔥 high resolution
        compress_level=0,  # 🔥 lossless
    )
    buf.seek(0)

    # Convert to base64 for preview
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return jsonify({"image": f"data:image/png;base64,{img_b64}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
