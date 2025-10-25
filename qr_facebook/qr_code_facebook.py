import qrcode
from PIL import Image, ImageDraw, ImageFont
import sys
import re

# Constants
FACEBOOK_BLUE = "#3f5c99"
TEXT_DARK_GRAY = "#666666"
BOX_SIZE = 12
BORDER = 4
TEXT_AREA_HEIGHT = 100
LOGO_SIZE_RATIO = 5
LOGO_PADDING = 20
FOOTER_BAR_HEIGHT = 8

def _validate_profile_url(profile_url):
    """Validate Facebook profile URL or username."""
    if not profile_url or not profile_url.strip():
        raise ValueError("Profile URL cannot be empty")
    
    # Basic validation for Facebook URLs
    if "facebook.com" in profile_url.lower() or "fb.com" in profile_url.lower():
        return profile_url.strip()
    
    # Assume it's a username if no domain found
    # Remove invalid characters
    clean_username = re.sub(r'[^a-zA-Z0-9._-]', '', profile_url.strip())
    if not clean_username:
        raise ValueError("Invalid username format")
    
    return f"https://facebook.com/{clean_username}"

def _create_qr_code(profile_url):
    """Create and return QR code matrix for the given URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=BOX_SIZE,
        border=BORDER,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    return qr.get_matrix()


def _draw_qr_modules(qr_modules, width, height):
    """Draw QR code modules on a white image."""
    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                x_pos = x * BOX_SIZE + BORDER * BOX_SIZE
                y_pos = y * BOX_SIZE + BORDER * BOX_SIZE
                draw.rectangle(
                    [x_pos, y_pos, x_pos + BOX_SIZE, y_pos + BOX_SIZE],
                    fill=FACEBOOK_BLUE
                )

    return qr_img


def _create_fallback_facebook_logo():
    """Create a fallback Facebook-style logo with the 'f' icon."""
    logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
    draw_logo = ImageDraw.Draw(logo_img)
    draw_logo.rectangle([20, 10, 60, 70], fill=FACEBOOK_BLUE)
    draw_logo.rectangle([25, 15, 55, 35], fill='white')
    draw_logo.polygon([(35, 35), (45, 35), (45, 65), (35, 65)], fill='white')
    return logo_img


def _load_or_create_logo(logo_path):
    """Load logo from path or create a fallback Facebook-style logo."""
    # Validate logo_path
    if not logo_path:
        print("No logo path provided. Using fallback logo.")
        return _create_fallback_facebook_logo()
    
    try:
        logo_img = Image.open(logo_path).convert('RGBA')
        print(f"Successfully loaded logo from: {logo_path}")
        return logo_img
    except FileNotFoundError:
        print(f"Logo file not found at '{logo_path}'. Using fallback logo.")
        return _create_fallback_facebook_logo()
    except (IOError, OSError) as e:
        print(f"Error reading logo file '{logo_path}': {e}. Using fallback logo.")
        return _create_fallback_facebook_logo()
    except Exception as e:
        print(f"Unexpected error loading logo: {e}. Using fallback logo.")
        return _create_fallback_facebook_logo()


def _place_logo_on_qr(qr_img, logo_img, qr_width):
    """Resize the logo, add white background, and place it on the QR code."""
    logo_size = qr_width // LOGO_SIZE_RATIO
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create white background for logo
    logo_bg_size = logo_size + LOGO_PADDING
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')

    # Center logo in the background
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)
    if logo_img.mode == 'RGBA':
        logo_bg.paste(logo_img, logo_pos, logo_img)
    else:
        logo_bg.paste(logo_img, logo_pos)

    # Calculate QR position and paste logo
    qr_height = qr_img.height
    qr_pos = ((qr_width - logo_bg_size) // 2, (qr_height - TEXT_AREA_HEIGHT - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    return qr_img


def _load_fonts():
    """Load fonts with fallback options and cross-platform support."""
    # Platform-specific font paths
    font_candidates = []
    if sys.platform == "win32":
        # Windows - use full paths
        font_candidates = [
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
            "arialbd.ttf",  # Fallback to PATH
            "arial.ttf"
        ]
    elif sys.platform == "darwin":  # macOS
        font_candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        ]
    else:  # Linux and others
        font_candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
    
    font_large = None
    font_small = None
    
    # Try to load fonts
    for font_path in font_candidates:
        try:
            font_large = ImageFont.truetype(font_path, 26)
            font_small = ImageFont.truetype(font_path, 18)
            print(f"Successfully loaded font: {font_path}")
            break
        except (IOError, OSError):
            continue
    
    # Fallback to default if all attempts failed
    if font_large is None:
        print("⚠️ Could not load system fonts. Using default font.")
        try:
            font_large = ImageFont.load_default(size=26)
            font_small = ImageFont.load_default(size=18)
        except TypeError:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    return font_large, font_small

def _add_text_elements(final_img, width, qr_height, handle, font_large, font_small):
    """Add username, scan text, and footer bar to the image."""
    draw = ImageDraw.Draw(final_img)

    # Draw username
    handle_width = draw.textlength(handle, font=font_large)
    handle_x = (width - handle_width) // 2
    draw.text((handle_x, qr_height + 20), handle, fill=FACEBOOK_BLUE, font=font_large)

    # Draw scan instruction
    scan_text = "Scan to follow on Facebook"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (width - scan_width) // 2
    draw.text((scan_x, qr_height + 60), scan_text, fill=TEXT_DARK_GRAY, font=font_small)

    # Draw footer bar
    bar_y = final_img.height - FOOTER_BAR_HEIGHT
    draw.rectangle([0, bar_y, width, bar_y + FOOTER_BAR_HEIGHT], fill=FACEBOOK_BLUE)

    return final_img

def create_facebook_qr_with_local_logo(logo_path="facebook_logo.png", output_path="qr_facebook.png"):
    """Generate a Facebook-themed QR code with logo and custom text."""
    try:
        # Get and validate profile URL
        profile_url = input("Enter Facebook link to your profile: ").strip()
        if not profile_url:
            print("❌ Error: Profile URL cannot be empty.")
            return None
        
        profile_url = _validate_profile_url(profile_url)
        
        # Create QR code
        qr_modules = _create_qr_code(profile_url)
        
        # Calculate dimensions
        qr_width = len(qr_modules) * BOX_SIZE + 2 * BORDER * BOX_SIZE
        total_height = len(qr_modules) * BOX_SIZE + 2 * BORDER * BOX_SIZE + TEXT_AREA_HEIGHT
        
        # Draw QR code
        qr_img = _draw_qr_modules(qr_modules, qr_width, total_height)
        
        # Add logo
        logo_img = _load_or_create_logo(logo_path)
        qr_img = _place_logo_on_qr(qr_img, logo_img, qr_width)
        
        # Prepare final image with text area
        qr_height = total_height - TEXT_AREA_HEIGHT
        final_img = Image.new('RGB', (qr_width, total_height), 'white')
        final_img.paste(qr_img.crop((0, 0, qr_width, qr_height)), (0, 0))
        
        # Load fonts and add text elements
        font_large, font_small = _load_fonts()
        handle = input("Enter your Facebook username or name: ").strip()
        
        if not handle:
            print("⚠️ Warning: Username is empty. Using default text.")
            handle = "Facebook Profile"
        
        final_img = _add_text_elements(final_img, qr_width, qr_height, handle, font_large, font_small)
        
        # Save result with error handling
        try:
            final_img.save(output_path, quality=95)
            print(f"✅ QR code with Facebook blue created: {output_path}")
        except (IOError, OSError) as e:
            print(f"❌ Error saving file: {e}")
            return None
        
        return final_img
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        return None
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

# Run Facebook version with proper guard
if __name__ == "__main__":
    print("Creating Facebook QR code...")
    create_facebook_qr_with_local_logo()
