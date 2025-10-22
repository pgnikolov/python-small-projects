import qrcode
from PIL import Image, ImageDraw, ImageFont
import random


def create_instagram_qr_with_local_logo(logo_path="instagram_logo.png"):
    profile_url = input("Enter instagram link to your profile:")

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)

    # Get QR code modules for custom coloring
    qr_modules = qr.get_matrix()

    # Instagram gradient colors
    INSTAGRAM_GRADIENT = [
        "#405DE6", "#5851DB", "#833AB4", "#C13584",
        "#E1306C", "#FD1D1D", "#F56040", "#F77737",
        "#FCAF45", "#FFDC80"
    ]

    # Create image with gradient QR code
    box_size = 12
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 100

    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw QR code with Instagram gradient colors
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                # Use different colors from Instagram gradient
                color_index = (x + y) % len(INSTAGRAM_GRADIENT)
                color = INSTAGRAM_GRADIENT[color_index]

                x_pos = x * box_size + border * box_size
                y_pos = y * box_size + border * box_size
                draw.rectangle(
                    [x_pos, y_pos, x_pos + box_size, y_pos + box_size],
                    fill=color
                )

    try:
        # Load local Instagram logo
        logo_img = Image.open(logo_path).convert('RGBA')
    except:
        # Create fallback logo
        logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        # Create Instagram-style logo with gradient
        draw_logo.ellipse([10, 10, 70, 70], outline='#E1306C', width=8)
        draw_logo.ellipse([30, 30, 50, 50], fill='#E1306C')

    # Resize logo
    logo_size = width // 5
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create white background for logo
    logo_bg_size = logo_size + 20
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')

    # Paste logo onto background (centered)
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)

    if logo_img.mode == 'RGBA':
        # Handle transparent logo
        logo_bg.paste(logo_img, logo_pos, logo_img)
    else:
        logo_bg.paste(logo_img, logo_pos)

    # Paste logo onto QR code
    qr_pos = ((width - logo_bg_size) // 2, (height - 100 - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    # Add text
    img_width, img_height = width, height - 100
    new_height = img_height + 100

    final_img = Image.new('RGB', (img_width, new_height), 'white')
    final_img.paste(qr_img.crop((0, 0, img_width, img_height)), (0, 0))

    draw = ImageDraw.Draw(final_img)

    try:
        font_large = ImageFont.truetype("arialbd.ttf", 26)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        try:
            font_large = ImageFont.truetype("arial.ttf", 26)
            font_small = ImageFont.truetype("arial.ttf", 18)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Handle text with gradient effect
    handle = input("Enter your username starting with @:")
    handle_width = draw.textlength(handle, font=font_large)
    handle_x = (img_width - handle_width) // 2

    # Create gradient text effect
    for i, char in enumerate(handle):
        char_color = INSTAGRAM_GRADIENT[i % len(INSTAGRAM_GRADIENT)]
        char_width = draw.textlength(char, font=font_large)
        draw.text((handle_x, img_height + 20), char, fill=char_color, font=font_large)
        handle_x += char_width

    # Scan text
    scan_text = "Scan to follow"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 60), scan_text, fill="#8E8E8E", font=font_small)

    # Add Instagram gradient bar at the bottom
    bar_height = 8
    bar_y = new_height - bar_height
    color_width = img_width // len(INSTAGRAM_GRADIENT)

    for i, color in enumerate(INSTAGRAM_GRADIENT):
        x_start = i * color_width
        x_end = (i + 1) * color_width
        if i == len(INSTAGRAM_GRADIENT) - 1:
            x_end = img_width
        draw.rectangle([x_start, bar_y, x_end, bar_y + bar_height], fill=color)

    final_img.save("qr_instagram.png", quality=95)
    print("QR code with Instagram gradient created!")
    return final_img


# Alternative version with smooth gradient
def create_instagram_qr_smooth_gradient(logo_path="instagram_logo.png"):
    profile_url = input("Enter instagram link to your profile:")

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)

    # Instagram gradient colors (smooth transition)
    GRADIENT_COLORS = ["#405DE6", "#833AB4", "#E1306C", "#F77737", "#FFDC80"]

    # Create smooth gradient effect
    qr_modules = qr.get_matrix()
    box_size = 10
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 120

    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw QR code with smooth gradient
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                # Calculate color based on position for smooth gradient
                progress = (x + y) / (len(qr_modules) + len(row))
                color_index = int(progress * (len(GRADIENT_COLORS) - 1))

                # Blend between colors for smoother transition
                if color_index < len(GRADIENT_COLORS) - 1:
                    blend_factor = progress * (len(GRADIENT_COLORS) - 1) - color_index
                    color1 = GRADIENT_COLORS[color_index]
                    color2 = GRADIENT_COLORS[color_index + 1]
                    # Simple blending (you can implement proper RGB blending)
                    color = color2 if blend_factor > 0.5 else color1
                else:
                    color = GRADIENT_COLORS[color_index]

                x_pos = x * box_size + border * box_size
                y_pos = y * box_size + border * box_size
                draw.rectangle(
                    [x_pos, y_pos, x_pos + box_size, y_pos + box_size],
                    fill=color
                )

    try:
        logo_img = Image.open(logo_path).convert('RGBA')
    except:
        logo_img = Image.new('RGBA', (70, 70), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        draw_logo.ellipse([5, 5, 65, 65], outline='#E1306C', width=6)
        draw_logo.ellipse([25, 25, 45, 45], fill='#E1306C')

    # Add logo to center
    logo_size = width // 6
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    logo_bg_size = logo_size + 15
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)

    if logo_img.mode == 'RGBA':
        logo_bg.paste(logo_img, logo_pos, logo_img)
    else:
        logo_bg.paste(logo_img, logo_pos)

    qr_pos = ((width - logo_bg_size) // 2, (height - 120 - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    # Final composition
    img_width, img_height = width, height - 120
    final_img = Image.new('RGB', (img_width, img_height + 120), 'white')
    final_img.paste(qr_img.crop((0, 0, img_width, img_height)), (0, 0))

    draw = ImageDraw.Draw(final_img)

    try:
        font_large = ImageFont.truetype("arialbd.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Handle text
    handle = input("Enter your username starting with @:")
    handle_width = draw.textlength(handle, font=font_large)
    handle_x = (img_width - handle_width) // 2
    draw.text((handle_x, img_height + 25), handle, fill="#E1306C", font=font_large)

    # Scan text
    scan_text = "Scan to follow on Instagram"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 65), scan_text, fill="#666666", font=font_small)

    # Gradient bar
    bar_height = 6
    bar_y = img_height + 100
    color_width = img_width // len(GRADIENT_COLORS)

    for i, color in enumerate(GRADIENT_COLORS):
        x_start = i * color_width
        x_end = (i + 1) * color_width
        if i == len(GRADIENT_COLORS) - 1:
            x_end = img_width
        draw.rectangle([x_start, bar_y, x_end, bar_y + bar_height], fill=color)

    final_img.save("qr_instagram.png", quality=95)
    print("🎨 Smooth gradient QR code created!")
    return final_img


# Run both versions
print("Creating gradient QR codes...")
create_instagram_qr_with_local_logo()
create_instagram_qr_smooth_gradient()