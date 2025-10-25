import qrcode
from PIL import Image, ImageDraw, ImageFont


def add_rounded_corners(image, radius=40):
    """
    Adds rounded corners to the provided image.

    This function takes an image and applies a mask with rounded corners
    to it. The corners are cut out based on the specified radius value.
    The resulting image includes transparency where the corners have been
    rounded. If no radius is specified, a default value is used.

    :param image: The source image on which the rounded corner mask
        will be applied.
    :type image: Image object
    :param radius: The radius of the rounded corners for the mask.
        Defaults to 40.
    :type radius: int
    :return: The image with rounded corners and transparency applied.
    :rtype: Image object
    """
    # Create a mask with rounded corners
    mask = Image.new('L', image.size, 0)
    mask_draw = ImageDraw.Draw(mask)

    # Draw rounded rectangle on mask
    mask_draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # Create result image with transparency
    result = Image.new('RGBA', image.size, (0, 0, 0, 0))
    result.paste(image, (0, 0), mask)

    return result


def create_instagram_qr_with_local_logo(logo_path="instagram_logo.png", rounded_corners=False, corner_radius=40):
    """
    Generates an Instagram QR code with a custom local logo and optional rounded corners.

    Creates a QR code for an Instagram profile with a customizable gradient pattern
    and integrates a local logo into the QR code. Additional text decorations, such as the
    Instagram handle and scan invitation text, are added to the QR code. The QR code can optionally
    include rounded corners for a stylistic touch.

    :param logo_path: Path to the local logo image file. Defaults to 'instagram_logo.png'.
    :param rounded_corners: Boolean flag to determine whether to apply rounded corners
        to the output QR code. Defaults to False.
    :param corner_radius: Specifies the radius of the corners if rounded_corners is set to True.
        Defaults to 40.
    :return: Final generated QR code image with Instagram gradient and logo.
    :rtype: PIL.Image.Image
    """
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
    except (FileNotFoundError, OSError, IOError) as e:
        print(f"⚠️ Logo file not found or invalid: {e}. Using fallback logo.")
        logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        draw_logo.ellipse([10, 10, 70, 70], outline='#E1306C', width=8)
        draw_logo.ellipse([30, 30, 50, 50], fill='#E1306C')

    # Resize logo
    logo_size = width // 5
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create white background for logo
    logo_bg_size = logo_size + 20
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')

    # Paste logo onto the background (centered)
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
    except (OSError, IOError):
        try:
            font_large = ImageFont.truetype("arial.ttf", 26)
            font_small = ImageFont.truetype("arial.ttf", 18)
        except (OSError, IOError):
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Handle text with a gradient effect
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

    # Add rounded corners if requested
    if rounded_corners:
        final_img = add_rounded_corners(final_img, corner_radius)
        filename = "qr_instagram_rounded.png"
    else:
        filename = "qr_instagram.png"

    final_img.save(filename, quality=95)
    print(f"QR code with Instagram gradient created! {'(Rounded corners)' if rounded_corners else ''}")
    return final_img


# Alternative version with a smooth gradient
def create_instagram_qr_smooth_gradient(logo_path="instagram_logo.png", rounded_corners=False, corner_radius=40):
    """
    Generate a smooth-gradient QR code for an Instagram profile.

    This function generates a visually appealing QR code with a smooth Instagram-style gradient
    and optionally includes a logo in the center. The resulting QR code can be customized
    to include rounded corners. Text such as the handle and a "scan" message will also be
    added below the QR code for additional context.

    :param logo_path: Path to the logo image to include in the QR code.
    :param rounded_corners: Flag to apply rounded corners to the final QR code image.
    :param corner_radius: Radius for the rounded corners if enabled.
    :return: The generated QR code image object.
    """
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

    # Create a smooth gradient effect
    qr_modules = qr.get_matrix()
    box_size = 10
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 120

    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw QR code with a smooth gradient
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                # Calculate color based on position for a smooth gradient
                progress = (x + y) / (len(qr_modules) + len(row))
                color_index = int(progress * (len(GRADIENT_COLORS) - 1))

                # Blend between colors for a smoother transition
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
    except (FileNotFoundError, OSError, IOError) as e:
        print(f"⚠️ Logo file not found or invalid: {e}. Using fallback logo.")
        logo_img = Image.new('RGBA', (70, 70), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        draw_logo.ellipse([5, 5, 65, 65], outline='#E1306C', width=6)
        draw_logo.ellipse([25, 25, 45, 45], fill='#E1306C')

    # Add logo to the center
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

    # Add rounded corners if requested
    if rounded_corners:
        final_img = add_rounded_corners(final_img, corner_radius)
        filename = "qr_instagram_smooth_rounded.png"
    else:
        filename = "qr_instagram_smooth.png"

    final_img.save(filename, quality=95)
    print(f"🎨 Smooth gradient QR code created! {'(Rounded corners)' if rounded_corners else ''}")
    return final_img


# Black and white QR code version
def create_instagram_qr_black_white(logo_path="instagram_logo.png", rounded_corners=False, corner_radius=40):
    """
    Create a black-and-white Instagram QR code with optional customization, such as adding a logo,
    rounded corners, and corner radius, and additional text for user instructions.

    :param logo_path: Path to the logo image file to be added in the center of the QR code.
    :type logo_path: str, optional
    :param rounded_corners: Flag indicating whether the image should have rounded corners.
    :type rounded_corners: bool, optional
    :param corner_radius: Radius for rounding the corners of the final image.
    :type corner_radius: int, optional
    :return: The generated QR code image.
    :rtype: PIL.Image.Image
    """
    profile_url = input("Enter Instagram link to your profile: ")

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)

    # Get QR code modules
    qr_modules = qr.get_matrix()

    # Create image
    box_size = 12
    border = 4
    width = len(qr_modules) * box_size + 2 * border * box_size
    height = len(qr_modules) * box_size + 2 * border * box_size + 100

    qr_img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(qr_img)

    # Draw black and white QR code
    for y, row in enumerate(qr_modules):
        for x, module in enumerate(row):
            if module:
                x_pos = x * box_size + border * box_size
                y_pos = y * box_size + border * box_size
                draw.rectangle(
                    [x_pos, y_pos, x_pos + box_size, y_pos + box_size],
                    fill='black'
                )

    try:
        # Load local Instagram logo
        logo_img = Image.open(logo_path).convert('RGBA')
    except (FileNotFoundError, OSError, IOError) as e:
        # Create fallback logo
        print(f"⚠️ Logo file not found or invalid: {e}. Using fallback logo.")
        logo_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_img)
        # Create an Instagram-style logo
        draw_logo.ellipse([10, 10, 70, 70], outline='black', width=8)
        draw_logo.ellipse([30, 30, 50, 50], fill='black')

    # Resize logo
    logo_size = width // 5
    logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create white background for logo
    logo_bg_size = logo_size + 20
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')
    logo_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)

    if logo_img.mode == 'RGBA':
        logo_bg.paste(logo_img, logo_pos, logo_img)
    else:
        logo_bg.paste(logo_img, logo_pos)

    # Paste logo onto QR code
    qr_pos = ((width - logo_bg_size) // 2, (height - 100 - logo_bg_size) // 2)
    qr_img.paste(logo_bg, qr_pos)

    # Add text area
    img_width, img_height = width, height - 100
    new_height = img_height + 100

    final_img = Image.new('RGB', (img_width, new_height), 'white')
    final_img.paste(qr_img.crop((0, 0, img_width, img_height)), (0, 0))

    draw = ImageDraw.Draw(final_img)

    try:
        font_large = ImageFont.truetype("arialbd.ttf", 26)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except (OSError, IOError):
        try:
            font_large = ImageFont.truetype("arial.ttf", 26)
            font_small = ImageFont.truetype("arial.ttf", 18)
        except (OSError, IOError):
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Handle text
    handle = input("Enter your username starting with @: ")
    handle_width = draw.textlength(handle, font=font_large)
    handle_x = (img_width - handle_width) // 2
    draw.text((handle_x, img_height + 20), handle, fill='black', font=font_large)

    # Scan text
    scan_text = "Scan to follow"
    scan_width = draw.textlength(scan_text, font=font_small)
    scan_x = (img_width - scan_width) // 2
    draw.text((scan_x, img_height + 60), scan_text, fill="#666666", font=font_small)

    # Add a black bar at the bottom
    bar_height = 8
    bar_y = new_height - bar_height
    draw.rectangle([0, bar_y, img_width, bar_y + bar_height], fill='black')

    # Add rounded corners if requested
    if rounded_corners:
        final_img = add_rounded_corners(final_img, corner_radius)
        filename = "qr_instagram_bw_rounded.png"
    else:
        filename = "qr_instagram_bw.png"

    final_img.save(filename, quality=95)
    print(f"⚫⚪ Black and white QR code created! {'(Rounded corners)' if rounded_corners else ''}")
    return final_img


# Menu system
def main():
    print("🎨 Instagram QR Code Generator")
    print("=" * 50)
    print("1. Color Gradient QR Code")
    print("2. Smooth Gradient QR Code")
    print("3. Black & White QR Code")
    print("4. Generate All Versions")
    print("=" * 50)

    choice = input("Choose an option (1-4): ").strip()

    # Ask about rounded corners
    rounded_choice = input("Add rounded corners? (y/n): ").strip().lower()
    rounded_corners = rounded_choice in ['y', 'yes', '1']

    corner_radius = 40
    if rounded_corners:
        radius_choice = input("Enter corner radius (default 40): ").strip()
        if radius_choice.isdigit():
            corner_radius = int(radius_choice)

    if choice == "1":
        create_instagram_qr_with_local_logo(rounded_corners=rounded_corners, corner_radius=corner_radius)
    elif choice == "2":
        create_instagram_qr_smooth_gradient(rounded_corners=rounded_corners, corner_radius=corner_radius)
    elif choice == "3":
        create_instagram_qr_black_white(rounded_corners=rounded_corners, corner_radius=corner_radius)
    elif choice == "4":
        print("\nGenerating all QR code versions...")
        create_instagram_qr_with_local_logo(rounded_corners=rounded_corners, corner_radius=corner_radius)
        create_instagram_qr_smooth_gradient(rounded_corners=rounded_corners, corner_radius=corner_radius)
        create_instagram_qr_black_white(rounded_corners=rounded_corners, corner_radius=corner_radius)
        print("\n✅ All QR code versions generated!")
    else:
        print("❌ Invalid choice. Please run the script again.")


# Run the program
if __name__ == "__main__":
    main()
