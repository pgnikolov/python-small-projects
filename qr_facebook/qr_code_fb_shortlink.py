import qrcode
from PIL import Image, ImageDraw, ImageFont


def _create_fallback_logo(facebook_blue):
    """Create a fallback Facebook-style 'f' logo."""
    logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
    draw_logo = ImageDraw.Draw(logo_img)
    draw_logo.rectangle([20, 10, 60, 70], fill=facebook_blue)
    draw_logo.rectangle([25, 15, 55, 35], fill='white')
    draw_logo.polygon([(35, 35), (45, 35), (45, 65), (35, 65)], fill='white')
    return logo_img


def _load_or_create_fallback_logo(logo_path, facebook_blue):
    """Load logo from path or create fallback if not available."""
    try:
        logo_img = Image.open(logo_path).convert('RGBA')
        print(f"Successfully loaded logo from: {logo_path}")
        return logo_img
    except FileNotFoundError:
        print(f"Logo file not found at '{logo_path}'. Creating fallback logo.")
        return _create_fallback_logo(facebook_blue)
    except (IOError, OSError) as e:
        print(f"Error reading logo file: {e}. Creating fallback logo.")
        return _create_fallback_logo(facebook_blue)


def _extract_facebook_shortlink(profile_url):
    """Extract or create a Facebook shortlink from profile URL or username."""
    if "facebook.com" in profile_url:
        if "/profile.php" in profile_url:
            import re
            match = re.search(r'id=(\d+)', profile_url)
            return f"fb.com/{match.group(1)}" if match else "fb.com/profile"
        else:
            username = profile_url.split("facebook.com/")[-1].split("/")[0].split("?")[0]
            return f"fb.com/{username}" if username else "fb.com"
    else:
        # If just username provided
        clean_username = profile_url.replace('@', '').replace('/', '')
        return f"fb.com/{clean_username}"


def _load_fonts():
    """Load fonts with fallback to system defaults."""
    FONT_SIZE_LARGE = 24
    FONT_SIZE_MEDIUM = 18
    FONT_SIZE_SMALL = 14
    FONT_PATHS = ["arialbd.ttf", "arial.ttf"]

    def _try_load_font(font_path, size):
        """Attempt to load a TrueType font, return None on failure."""
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError):
            return None

    # Try loading fonts from available paths
    for font_path in FONT_PATHS:
        font_large = _try_load_font(font_path, FONT_SIZE_LARGE)
        if font_large is not None:
            font_medium = _try_load_font(font_path, FONT_SIZE_MEDIUM)
            font_small = _try_load_font(font_path, FONT_SIZE_SMALL)
            return font_large, font_medium, font_small

    # Fallback to the default font if all attempts fail
    default_font = ImageFont.load_default()
    return default_font, default_font, default_font


def create_facebook_qr_with_local_logo(logo_path="facebook_logo.png"):
    # Define Facebook blue color constant
    FACEBOOK_BLUE = "#3f5c99"

    # Load or create logo
    logo_img = _load_or_create_fallback_logo(logo_path, FACEBOOK_BLUE)

    # Get Facebook profile and create shortlink
    profile_url = input("Enter Facebook profile URL or username: ")
    shortlink = _extract_facebook_shortlink(profile_url)
    print(f"Shortlink: {shortlink}")

    # Use the shortlink for QR code
    qr_data = f"https://{shortlink}"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Get QR code modules for custom coloring
    qr_modules = qr.get_matrix()

    # Create an image with blue QR code
    box_size = 12
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 120
    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw QR code with a single Facebook blue color
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                x_pos = x * box_size + border * box_size
                y_pos = y * box_size + border * box_size
                draw.rectangle(
                    [x_pos, y_pos, x_pos + box_size, y_pos + box_size],
                    fill=FACEBOOK_BLUE
                )

    # Resize logo
    logo_size = width // 5
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create white background for logo
    logo_bg_size = logo_size + 20
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')

    # Paste logo onto the background (centered)
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)
    if logo_img.mode == 'RGBA':
        logo_bg.paste(logo_img, logo_pos, logo_img)
    else:
        logo_bg.paste(logo_img, logo_pos)

    # Paste logo onto QR code
    qr_pos = ((width - logo_bg_size) // 2, (height - 120 - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    # Add a text section
    img_width, img_height = width, height - 120
    new_height = img_height + 120
    final_img = Image.new('RGB', (img_width, new_height), 'white')
    final_img.paste(qr_img.crop((0, 0, img_width, img_height)), (0, 0))
    draw = ImageDraw.Draw(final_img)

    # Load fonts
    font_large, font_medium, font_small = _load_fonts()

    # Display name
    display_name = input("Enter your display name: ")
    name_width = draw.textlength(display_name, font=font_large)
    name_x = (img_width - name_width) // 2
    draw.text((name_x, img_height + 15), display_name, fill=FACEBOOK_BLUE, font=font_large)

    # Shortlink text
    shortlink_width = draw.textlength(shortlink, font=font_medium)
    shortlink_x = (img_width - shortlink_width) // 2
    draw.text((shortlink_x, img_height + 50), shortlink, fill="#333333", font=font_medium)

    # Scan text
    scan_text = "Scan to follow on Facebook"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 80), scan_text, fill="#666666", font=font_small)

    # Add Facebook blue bar at the bottom
    bar_height = 6
    bar_y = new_height - bar_height
    draw.rectangle([0, bar_y, img_width, bar_y + bar_height], fill=FACEBOOK_BLUE)

    final_img.save("qr_facebook.png", quality=95)
    print(f"✅ Facebook QR code created!")
    print(f"📱 Shortlink: {shortlink}")
    print(f"🔗 QR points to: {qr_data}")
    return final_img


# Run Facebook version
print("Creating Facebook QR code with shortlink...")
create_facebook_qr_with_local_logo()