# 📘 Facebook QR Code Generator

A comprehensive Python toolkit for creating Facebook-themed QR codes with clean blue styling, automatic shortlink generation, logo integration, and custom text labels for profiles or pages.

---

## 📦 Project Contents

This folder contains **two versions** of the Facebook QR code generator:

1. **`qr_code_facebook.py`** - Enhanced version with modular architecture and robust error handling
2. **`qr_code_fb_shortlink.py`** - Shortlink-focused version with automatic URL shortening

---

## ✨ Features

### Common Features (Both Versions)

* **Facebook Blue Styling:** Generates QR codes in Facebook's signature blue color (`#3f5c99`)
* **Custom Logo Support:** Automatically embeds your Facebook logo or generates a fallback "f" logo
* **Personalized Text Area:** Adds your name and "Scan to follow on Facebook" message
* **Professional Layout:** Includes a Facebook-blue footer bar for a clean finish
* **High-Quality Output:** Exports sharp PNG images ready for sharing or printing
* **Cross-Platform Font Support:** Automatically detects and loads fonts on Windows, macOS, and Linux
* **Robust Error Handling:** Graceful fallbacks for missing logos and fonts

### Enhanced Version Features (`qr_code_facebook.py`)

* **Modular Architecture:** Clean separation of concerns with helper functions
* **URL Validation:** Validates and sanitizes Facebook profile URLs
* **Platform-Specific Font Paths:** Smart font detection for Windows, macOS, and Linux
* **Comprehensive Error Messages:** Detailed feedback for troubleshooting
* **Input Validation:** Prevents empty or invalid inputs

### Shortlink Version Features (`qr_code_fb_shortlink.py`)

* **Automatic Shortlink Detection:** Converts full Facebook URLs to `fb.com/username` format
* **Profile ID Support:** Handles `profile.php?id=XXXX` style links
* **Three-Size Font System:** Large, medium, and small fonts for hierarchical text display
* **Display Name + Shortlink:** Shows both your display name and shortened URL

---

## 🚀 Quick Start

### Prerequisites

* Python 3.6 or higher
* Required Python packages:

```bash
pip install qrcode[pil] pillow
```

---

## 📥 Installation

#### 1. Clone or download the repository:

```bash
git clone <repository-url>
cd qr_facebook
```

#### 2. Install dependencies:

```bash
pip install qrcode[pil] pillow
```

#### 3. (Optional) Add your logo as `facebook_logo.png` in the same directory

---

## 🎯 Usage

### Enhanced Version (`qr_code_facebook.py`)

```bash
python qr_code_facebook.py
```

**Interactive prompts:**
1. Enter your Facebook profile URL or username
2. Enter your Facebook username or display name
3. The script generates `qr_facebook.png`

**Features:**
- Full error handling and validation
- Works with URLs or plain usernames
- Provides detailed success/error messages

---

### Shortlink Version (`qr_code_fb_shortlink.py`)

```bash
python qr_code_fb_shortlink.py
```

**Interactive prompts:**
1. Enter Facebook profile URL or username
2. Automatically generates shortlink (e.g., `fb.com/username`)
3. Enter your display name
4. The script creates `qr_facebook.png`

**Output includes:**
- Display name (large font)
- Shortlink URL (medium font)
- "Scan to follow on Facebook" (small font)

---

## 🎨 Customization Options

### Color Theme

Both versions use Facebook's signature blue. To customize:

```python
FACEBOOK_BLUE = "#3f5c99"
```

### QR Code Parameters

Adjust QR code size and error correction:

```python
qr = qrcode.QRCode(
    version=1,                                      # QR code size (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
    box_size=12,                                    # Pixel size of each module
    border=4,                                       # Border width in modules
)
```

### Font Customization

#### Enhanced Version (`qr_code_facebook.py`)

The enhanced version automatically detects system fonts across platforms:

**Windows:**
```python
"C:\\Windows\\Fonts\\arialbd.ttf"
"C:\\Windows\\Fonts\\arial.ttf"
```

**macOS:**
```python
"/System/Library/Fonts/Supplemental/Arial.ttf"
"/System/Library/Fonts/Supplemental/Arial Bold.ttf"
```

**Linux:**
```python
"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
```

Fonts automatically fall back to system defaults if none are found.

#### Shortlink Version (`qr_code_fb_shortlink.py`)

Uses three font sizes for text hierarchy:

```python
FONT_SIZE_LARGE = 24   # Display name
FONT_SIZE_MEDIUM = 18  # Shortlink
FONT_SIZE_SMALL = 14   # Subtitle text
```

**Note:** The shortlink version currently uses relative font paths. For improved cross-platform compatibility, consider updating it to use the platform-specific paths from the enhanced version.

---

## 📁 File Structure

```bash
qr_facebook/
├── qr_code_facebook.py        # Enhanced version with full error handling
├── qr_code_fb_shortlink.py    # Shortlink-focused version
├── facebook_logo.png          # Optional custom logo
├── qr_facebook.png            # Generated QR code output
└── README.md                  # This file
```

---

## 📸 Output Examples

### Enhanced Version Output

Your generated QR code includes:
* Blue QR pattern in Facebook color
* Centered logo with white background
* User name or page name
* "Scan to follow on Facebook" text
* Facebook-blue footer bar

### Shortlink Version Output

Your generated QR code includes:
* Blue QR pattern
* Centered Facebook logo
* Display name (large, Facebook blue)
* Shortlink text (medium, dark gray)
* "Scan to follow on Facebook" (small, gray)
* Footer bar in Facebook blue

---

## 🛠️ Technical Details

### Dependencies

* **`qrcode`**: QR code generation with high error correction
* **`Pillow (PIL)`**: Image creation, drawing, and manipulation
* **`re`** (shortlink version): Regular expression parsing for profile URLs
* **`sys`** (enhanced version): Platform detection for font paths

### Error Handling Features

#### Enhanced Version (`qr_code_facebook.py`)

* **URL Validation:** Sanitizes and validates Facebook URLs
* **Empty Input Protection:** Prevents blank profile URLs and usernames
* **Logo Loading Errors:** Creates fallback logo if file is missing or corrupted
* **Font Loading Errors:** Tries multiple font paths before falling back to defaults
* **Keyboard Interrupts:** Gracefully handles Ctrl+C cancellation
* **File Save Errors:** Catches and reports I/O errors during save

#### Shortlink Version (`qr_code_fb_shortlink.py`)

* **Profile URL Parsing:** Handles multiple Facebook URL formats
* **Profile ID Extraction:** Supports `profile.php?id=` style URLs
* **Username Sanitization:** Cleans special characters from usernames
* **Logo Fallback:** Auto-generates "f" logo if file missing
* **Font Fallback:** Uses default fonts if system fonts unavailable

### Cross-Platform Compatibility

Both versions work on:
- ✅ Windows (7, 8, 10, 11)
- ✅ macOS (10.14+)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

The enhanced version provides **superior cross-platform font support** with automatic platform detection.

---

## 🔧 Shortlink Format Examples

The shortlink version handles these input formats:

| Input | Generated Shortlink |
|-------|-------------------|
| `https://facebook.com/john.doe` | `fb.com/john.doe` |
| `https://www.facebook.com/profile.php?id=123456` | `fb.com/123456` |
| `john.doe` | `fb.com/john.doe` |
| `@john.doe` | `fb.com/john.doe` |

---

## ⚠️ Important Notes

* Ensure your Facebook profile is **public** for optimal QR code usability
* Use PNG format for clear, non-pixelated results
* Higher `box_size` values produce larger QR codes
* Test generated QR codes with multiple scanners before printing
* The shortlink format (`fb.com/username`) creates cleaner, faster-scanning QR codes

---

## 🐛 Troubleshooting

### QR Code Doesn't Scan

**Solution:**
* Increase `box_size` value (default: 12)
* Ensure strong contrast between QR code and background
* Test under good lighting conditions
* Try increasing error correction level (already at maximum in both versions)

### Logo Not Appearing

**Solution:**
* Verify `facebook_logo.png` exists in the script directory
* Ensure the file is a valid PNG image
* Check file permissions (readable by Python)
* Both versions will auto-generate a fallback logo if needed

### Font Issues

**Symptoms:**
* Text appears in default font instead of Arial
* Warning message: "⚠️ Could not load system fonts"

**Solution:**

**For Enhanced Version (`qr_code_facebook.py`):**
- Install Arial fonts for your operating system
- On Linux: `sudo apt-get install ttf-mscorefonts-installer`
- Script will automatically fall back to Liberation or DejaVu fonts

**For Shortlink Version (`qr_code_fb_shortlink.py`):**
- Place `arialbd.ttf` and `arial.ttf` in the script directory, or
- Update `FONT_PATHS` to point to your system fonts
- Consider migrating to the enhanced version's platform-specific paths

### Platform-Specific Font Paths Not Working

**Solution:**
* Verify font installation: `fc-list | grep -i arial` (Linux/macOS)
* Check Windows fonts folder: `C:\Windows\Fonts`
* Update font paths in `_load_fonts()` function if using custom fonts

### "Profile URL cannot be empty" Error

**Solution:**
* Ensure you enter a valid Facebook URL or username
* Don't leave the input prompt blank
* Format: `https://facebook.com/username` or just `username`

### Script Exits Without Creating QR Code

**Solution:**
* Check for Python exceptions in terminal output
* Ensure all dependencies are installed: `pip list | grep -E "qrcode|Pillow"`
* Verify you have write permissions in the script directory
* Check available disk space

---

## 🚀 Recommended Improvements

### For Shortlink Version

To match the enhanced version's robustness, consider adding:

1. **Platform-Specific Font Paths**
   ```python
   import sys
   if sys.platform == "win32":
       FONT_PATHS = ["C:\\Windows\\Fonts\\arialbd.ttf", ...]
   ```

2. **Input Validation**
   ```python
   if not profile_url or not profile_url.strip():
       print("❌ Error: Profile URL cannot be empty.")
       return None
   ```

3. **Better Error Messages**
   ```python
   except FileNotFoundError:
       print(f"Logo file not found at '{logo_path}'. Using fallback logo.")
   ```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

* **GUI Version:** Tkinter or PyQt interface
* **Batch Processing:** Generate multiple QR codes from CSV
* **Custom Themes:** Dark mode, alternate color schemes
* **QR Code Styling:** Rounded corners, custom patterns
* **Analytics:** Track scan counts (requires external service)
* **Animated QR Codes:** GIF output with logo animation

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## 📚 Related Projects

Check out the other QR code generators in this repository:

* **Instagram QR Generator** (`qr_instagram/`) - Gradient colors, rounded corners, multiple modes
* **LinkedIn QR Generator** (`qr_linked_in/`) - Professional blue styling, rounded corners

---

## 💡 Tips for Best Results

1. **Test Before Printing:** Always test QR codes digitally before mass printing
2. **Maintain Contrast:** Ensure sufficient contrast for reliable scanning
3. **Size Appropriately:** Minimum recommended print size is 2cm × 2cm
4. **Error Correction:** The high error correction level allows up to 30% damage
5. **Logo Size:** Keep logos small (current: 1/5 of QR code width) for scan reliability
6. **Profile URLs:** Use short, clean URLs for faster QR code generation
7. **Public Profiles:** Ensure your Facebook profile is public for best user experience

---

## 🔗 External Resources

* [QR Code Specification](https://www.qrcode.com/en/about/standards.html)
* [Pillow Documentation](https://pillow.readthedocs.io/)
* [Python QRCode Library](https://github.com/lincolnloop/python-qrcode)
* [Facebook URL Formats](https://developers.facebook.com/docs/)

---

**Created with ❤️ for seamless social media sharing**
```
