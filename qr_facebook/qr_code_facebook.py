import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_facebook_qr_with_local_logo(logo_path="facebook_logo.png"):
    profile_url = input("Enter Facebook link to your profile: ")

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

    # Single Facebook blue color
    FACEBOOK_BLUE = "#3f5c99"

    # Create image with blue QR code
    box_size = 12
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 100

    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw QR code with single Facebook blue color
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                x_pos = x * box_size + border * box_size
                y_pos = y * box_size + border * box_size
                draw.rectangle(
                    [x_pos, y_pos, x_pos + box_size, y_pos + box_size],
                    fill=FACEBOOK_BLUE
                )

    try:
        # Load local Facebook logo
        logo_img = Image.open(logo_path).convert('RGBA')
    except:
        # Create fallback Facebook-style logo
        logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        # Create Facebook-style "f" logo
        draw_logo.rectangle([20, 10, 60, 70], fill=FACEBOOK_BLUE)
        draw_logo.rectangle([25, 15, 55, 35], fill='white')
        draw_logo.polygon([(35, 35), (45, 35), (45, 65), (35, 65)], fill='white')

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

    # Handle text
    handle = input("Enter your Facebook username or name: ")
    handle_width = draw.textlength(handle, font=font_large)
    handle_x = (img_width - handle_width) // 2

    # Use Facebook blue for text
    draw.text((handle_x, img_height + 20), handle, fill=FACEBOOK_BLUE, font=font_large)

    # Scan text
    scan_text = "Scan to follow on Facebook"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 60), scan_text, fill="#666666", font=font_small)

    # Add Facebook blue bar at the bottom
    bar_height = 8
    bar_y = new_height - bar_height
    draw.rectangle([0, bar_y, img_width, bar_y + bar_height], fill=FACEBOOK_BLUE)

    final_img.save("qr_facebook.png", quality=95)
    print("QR code with Facebook blue created!")
    return final_img


# Run Facebook version
print("Creating Facebook QR code...")
create_facebook_qr_with_local_logo()