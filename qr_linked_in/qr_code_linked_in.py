import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_linkedin_qr_with_local_logo(logo_path="linkedin-logo.png"):
    profile_url = input("Enter LinkedIn profile URL or username: ")

    # Create shortlink
    if "linkedin.com" in profile_url:
        username = profile_url.split("linkedin.com/in/")[-1].split("/")[0].split("?")[0]
        shortlink = f"linkedin.com/in/{username}" if username else "linkedin.com"
    else:
        shortlink = f"linkedin.com/in/{profile_url.replace('@', '').replace('/', '')}"

    print(f"Shortlink: {shortlink}")

    qr_data = f"https://{shortlink}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_modules = qr.get_matrix()

    LINKEDIN_BLUE = "#225982"
    box_size = 12
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 120

    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw normal QR code
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                x_pos = x * box_size + border * box_size
                y_pos = y * box_size + border * box_size
                draw.rectangle(
                    [x_pos, y_pos, x_pos + box_size, y_pos + box_size],
                    fill=LINKEDIN_BLUE
                )

    # Load LinkedIn logo
    try:
        logo_img = Image.open(logo_path).convert('RGBA')
    except:
        logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        draw_logo.rectangle([0, 0, 80, 80], fill=LINKEDIN_BLUE)
        draw_logo.text((20, 15), "in", fill='white')

    logo_size = width // 5
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # White background behind logo
    logo_bg_size = logo_size + 20
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)
    logo_bg.paste(logo_img, logo_pos, logo_img)
    qr_pos = ((width - logo_bg_size) // 2, (height - 120 - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    # Add text section
    img_width, img_height = width, height - 120
    new_height = img_height + 120
    final_img = Image.new('RGB', (img_width, new_height), 'white')
    final_img.paste(qr_img.crop((0, 0, img_width, img_height)), (0, 0))
    draw = ImageDraw.Draw(final_img)

    try:
        font_large = ImageFont.truetype("arialbd.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    display_name = input("Enter your display name: ")
    name_width = draw.textlength(display_name, font=font_large)
    name_x = (img_width - name_width) // 2
    draw.text((name_x, img_height + 15), display_name, fill=LINKEDIN_BLUE, font=font_large)

    shortlink_width = draw.textlength(shortlink, font=font_medium)
    shortlink_x = (img_width - shortlink_width) // 2
    draw.text((shortlink_x, img_height + 50), shortlink, fill="#333333", font=font_medium)

    scan_text = "Scan to connect on LinkedIn"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 80), scan_text, fill="#666666", font=font_small)

    bar_height = 6
    bar_y = new_height - bar_height
    draw.rectangle([0, bar_y, img_width, bar_y + bar_height], fill=LINKEDIN_BLUE)

    # ✅ Add rounded corners to entire image
    radius = 40  # corner radius (adjust to your liking)
    mask = Image.new("L", final_img.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, img_width, new_height], radius=radius, fill=255)
    final_img.putalpha(mask)

    # Save as PNG with transparency
    final_img.save("qr_linkedin_rounded_edges.png", format="PNG", quality=95)

    print(f"✅ LinkedIn QR code created with rounded edges!")
    print(f"📱 Shortlink: {shortlink}")
    print(f"🔗 QR points to: {qr_data}")
    return final_img


# Run LinkedIn version
print("Creating LinkedIn QR code with rounded edges...")
create_linkedin_qr_with_local_logo("linkedin-logo.png")

