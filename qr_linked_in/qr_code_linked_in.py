import qrcode
from PIL import Image, ImageDraw, ImageFont

# Constants
LINKEDIN_BLUE = "#225982"
QR_BOX_SIZE = 12
QR_BORDER = 4
QR_VERSION = 1
TEXT_AREA_HEIGHT = 120
LOGO_RATIO = 5
LOGO_PADDING = 20
CORNER_RADIUS = 40
FOOTER_BAR_HEIGHT = 6

# Font sizes
FONT_SIZE_LARGE = 24
FONT_SIZE_MEDIUM = 18
FONT_SIZE_SMALL = 14


def extract_username_from_url(profile_url):
    """Extract username from LinkedIn URL or return formatted username."""
    if "linkedin.com" in profile_url:
        username = profile_url.split("linkedin.com/in/")[-1].split("/")[0].split("?")[0]
        shortlink = f"linkedin.com/in/{username}" if username else "linkedin.com"
    else:
        username = profile_url.replace('@', '').replace('/', '')
        shortlink = f"linkedin.com/in/{username}"
    return shortlink


def generate_qr_code(data):
    """Generate QR code matrix from data."""
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=QR_BOX_SIZE,
        border=QR_BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.get_matrix()


# Constants for fallback logo dimensions
FALLBACK_LOGO_SIZE = 80
FALLBACK_LOGO_TEXT_X = 20
FALLBACK_LOGO_TEXT_Y = 15


def create_fallback_logo():
    """Create a fallback LinkedIn logo with blue background and 'in' text."""
    logo_img = Image.new('RGBA', (FALLBACK_LOGO_SIZE, FALLBACK_LOGO_SIZE), (0, 0, 0, 0))
    draw_logo = ImageDraw.Draw(logo_img)
    draw_logo.rectangle([0, 0, FALLBACK_LOGO_SIZE, FALLBACK_LOGO_SIZE], fill=LINKEDIN_BLUE)
    draw_logo.text((FALLBACK_LOGO_TEXT_X, FALLBACK_LOGO_TEXT_Y), "in", fill='white')
    return logo_img


def load_or_create_logo(logo_path):
    """Load logo from path or create fallback logo if file not found.
    
    Args:
        logo_path: Path to the logo image file
        
    Returns:
        PIL Image object in RGBA mode
        
    Note:
        If the logo file cannot be loaded, a fallback LinkedIn-style
        logo will be generated with a blue background and 'in' text.
    """
    try:
        logo_img = Image.open(logo_path).convert('RGBA')
    except (IOError, FileNotFoundError):
        logo_img = create_fallback_logo()
    return logo_img


def draw_qr_modules(draw, qr_modules):
    """Draw QR code modules on the image."""
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                x_pos = x * QR_BOX_SIZE + QR_BORDER * QR_BOX_SIZE
                y_pos = y * QR_BOX_SIZE + QR_BORDER * QR_BOX_SIZE
                draw.rectangle(
                    [x_pos, y_pos, x_pos + QR_BOX_SIZE, y_pos + QR_BOX_SIZE],
                    fill=LINKEDIN_BLUE
                )


def prepare_logo_with_background(logo_img, logo_size):
    """Resize the logo and add white background."""
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    logo_bg_size = logo_size + LOGO_PADDING
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)
    logo_bg.paste(logo_img, logo_pos, logo_img)

    return logo_bg, logo_bg_size


def _load_single_font(font_filename, font_size):
    """Load a single font with fallback to default."""
    try:
        return ImageFont.truetype(font_filename, font_size)
    except (OSError, IOError):
        return ImageFont.load_default()


def load_fonts():
    """Load fonts with fallback to default."""
    font_configs = [
        ("arialbd.ttf", FONT_SIZE_LARGE),
        ("arial.ttf", FONT_SIZE_MEDIUM),
        ("arial.ttf", FONT_SIZE_SMALL)
    ]

    return tuple(_load_single_font(filename, size) for filename, size in font_configs)


def draw_text_section(draw, img_width, img_height, display_name, shortlink, fonts):
    """Draw text section with name, shortlink, and scan prompt."""
    font_large, font_medium, font_small = fonts

    # Display name
    name_width = draw.textlength(display_name, font=font_large)
    name_x = (img_width - name_width) // 2
    draw.text((name_x, img_height + 15), display_name, fill=LINKEDIN_BLUE, font=font_large)

    # Shortlink
    shortlink_width = draw.textlength(shortlink, font=font_medium)
    shortlink_x = (img_width - shortlink_width) // 2
    draw.text((shortlink_x, img_height + 50), shortlink, fill="#333333", font=font_medium)

    # Scan prompt
    scan_text = "Scan to connect on LinkedIn"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 80), scan_text, fill="#666666", font=font_small)


def add_rounded_corners(image, img_width, new_height):
    """Add rounded corners to the image."""
    mask = Image.new("L", image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, img_width, new_height], radius=CORNER_RADIUS, fill=255)
    image.putalpha(mask)
    return image


def create_linkedin_qr_with_local_logo(logo_path="linkedin-logo.png"):
    """
    Generates a LinkedIn QR code with a local logo merged into the QR code image. The
    function incorporates user input to customize the QR code and its accompanying
    text, including the LinkedIn profile shortlink and display name. The QR code
    produced includes rounded corners and is saved as an image in PNG format.

    :param logo_path: Path to the logo image file to be embedded in the QR code.
                      Default is 'linkedin-logo.png'.
    :type logo_path: str
    :return: A PIL.Image object of the generated QR code with integrated logo and
             customized text section.
    :rtype: PIL.Image.Image
    """
    # Get user input
    profile_url = input("Enter LinkedIn profile URL or username: ")
    display_name = input("Enter your display name: ")

    # Process URL
    shortlink = extract_username_from_url(profile_url)
    print(f"Shortlink: {shortlink}")
    qr_data = f"https://{shortlink}"

    # Generate QR code
    qr_modules = generate_qr_code(qr_data)

    # Calculate dimensions
    width = len(qr_modules) * QR_BOX_SIZE + 2 * QR_BORDER * QR_BOX_SIZE
    height = len(qr_modules) * QR_BOX_SIZE + 2 * QR_BORDER * QR_BOX_SIZE + TEXT_AREA_HEIGHT

    # Create a base image and draw QR code
    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)
    draw_qr_modules(draw, qr_modules)

    # Load and prepare the logo
    logo_img = load_or_create_logo(logo_path)
    logo_size = width // LOGO_RATIO
    logo_bg, logo_bg_size = prepare_logo_with_background(logo_img, logo_size)

    # Paste logo on QR code
    qr_pos = ((width - logo_bg_size) // 2, (height - TEXT_AREA_HEIGHT - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    # Create final image with text section
    img_width, img_height = width, height - TEXT_AREA_HEIGHT
    new_height = img_height + TEXT_AREA_HEIGHT
    final_img = Image.new('RGB', (img_width, new_height), 'white')
    final_img.paste(qr_img.crop((0, 0, img_width, img_height)), (0, 0))

    # Draw text section
    draw = ImageDraw.Draw(final_img)
    fonts = load_fonts()
    draw_text_section(draw, img_width, img_height, display_name, shortlink, fonts)

    # Add footer bar
    bar_y = new_height - FOOTER_BAR_HEIGHT
    draw.rectangle([0, bar_y, img_width, bar_y + FOOTER_BAR_HEIGHT], fill=LINKEDIN_BLUE)

    # Add rounded corners
    final_img = add_rounded_corners(final_img, img_width, new_height)

    # Save image
    final_img.save("qr_linkedin_rounded_edges.png", format="PNG", quality=95)
    print(f"✅ LinkedIn QR code created with rounded edges!")
    print(f"📱 Shortlink: {shortlink}")
    print(f"🔗 QR points to: {qr_data}")
    return final_img


# Run LinkedIn version
print("Creating LinkedIn QR code with rounded edges...")
create_linkedin_qr_with_local_logo("linkedin-logo.png")
