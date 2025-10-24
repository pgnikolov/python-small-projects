# 📘 Facebook QR Code Generator (Simple Version)

A Python script that creates Facebook-themed QR codes with clean blue styling, optional logo integration, and custom text labels for your profile or page.

---

## Features

* **Facebook Blue Styling:** Generates QR codes in Facebook’s signature blue color
* **Custom Logo Support:** Automatically embeds your Facebook logo or generates a fallback “f” logo
* **Personalized Text Area:** Adds your name and “Scan to follow on Facebook” message
* **Professional Layout:** Includes a Facebook-blue footer bar for a clean finish
* **High-Quality Output:** Exports sharp PNG images ready for sharing or printing

---

## Quick Start

### Prerequisites

* Python 3.6 or higher
* Required Python packages:

```bash
pip install qrcode[pil] pillow
```

---

## Installation

#### 1. Clone or download the script:

```bash
git clone <repository-url>
cd facebook-qr-generator
```

#### 2. Ensure dependencies are installed:

```bash
pip install qrcode[pil] pillow
```

#### 3. (Optional) Add your logo as `facebook_logo.png` in the same directory

---

## Basic Usage

### Run the script:

```bash
python facebook_qr_generator.py
```

#### The script will:

1. Ask for your Facebook profile URL
2. Request your name or username
3. Generate a Facebook-blue QR code
4. Save it as `qr_facebook.png`

---

## Customization Options

### Color Theme

Edit the main color:

```python
FACEBOOK_BLUE = "#3f5c99"
```

### Font Customization

Change font settings:

```python
font_large = ImageFont.truetype("arialbd.ttf", 26)  # For name
font_small = ImageFont.truetype("arial.ttf", 18)    # For subtitle
```

If fonts are missing, system defaults are used.

---

## 📁 File Structure

```bash
facebook-qr-generator/
├── facebook_qr_generator.py   # Main script
├── facebook_logo.png          # Optional logo
├── qr_facebook.png            # Generated QR code
└── README.md                  # This file
```

---

## 📸 Output Example

Your generated QR code includes:

* Blue QR pattern in Facebook color
* Centered logo with white background
* User name or page name below
* “Scan to follow on Facebook” text
* Facebook-blue footer bar

---

## 🛠️ Technical Details

#### Dependencies

* `qrcode`: QR code generation
* `Pillow`: Image creation and drawing

#### Error Handling

* **Logo not found:** Creates a fallback “f” logo
* **Font issues:** Falls back to system fonts automatically

---

## ⚠️ Notes

* Works best with public Facebook profiles or pages
* Use PNG format for clear, non-pixelated results
* Higher `box_size` values produce larger QR codes

---

## 🐛 Troubleshooting

#### QR Code Doesn’t Scan

* Increase contrast (white background, darker QR color)
* Raise `box_size` in QR configuration

#### Logo Not Appearing

* Check `facebook_logo.png` file path
* Use a valid PNG with transparency

---

# 📗 Facebook QR Code Generator (Shortlink Version)

A more advanced version of the generator that automatically extracts or builds shortlinks (like `fb.com/username`) for cleaner QR codes.

---

## Features

* **Automatic Shortlink Detection:** Converts full Facebook URLs to `fb.com/username` format
* **Professional Design:** Includes name, shortlink, and “Scan to follow” message
* **Facebook Blue Styling:** Consistent with the platform’s visual identity
* **Fallback Logo System:** Generates a clean “f” logo if none is found
* **High-Resolution PNG Output:** Suitable for business cards, flyers, or profiles

---

## Quick Start

### Prerequisites

* Python 3.6 or higher
* Required packages:

```bash
pip install qrcode[pil] pillow
```

---

## Installation

#### 1. Clone or download:

```bash
git clone <repository-url>
cd facebook-qr-shortlink-generator
```

#### 2. Install dependencies:

```bash
pip install qrcode[pil] pillow
```

#### 3. (Optional) Add your logo as `facebook_logo.png` in the same directory

---

## Basic Usage

### Run:

```bash
python facebook_qr_shortlink_generator.py
```

#### The script will:

1. Ask for your Facebook profile URL or username
2. Automatically build your shortlink (e.g., `fb.com/username`)
3. Request your display name
4. Generate a Facebook-themed QR code
5. Save it as `qr_facebook.png`

---

## Customization Options

### Shortlink Logic

Automatically detects multiple formats:

* Full profile URLs
* `profile.php?id=XXXX` links
* Simple usernames

### Appearance Settings

```python
FACEBOOK_BLUE = "#3f5c99"
box_size = 12
border = 4
```

### Fonts

```python
font_large = ImageFont.truetype("arialbd.ttf", 24)  # Name
font_medium = ImageFont.truetype("arial.ttf", 18)   # Shortlink
font_small = ImageFont.truetype("arial.ttf", 14)    # Subtitle
```

---

## 📁 File Structure

```bash
facebook-qr-shortlink-generator/
├── facebook_qr_shortlink_generator.py  # Main script
├── facebook_logo.png                   # Optional logo
├── qr_facebook.png                     # Generated QR
└── README.md                           # This file
```

---

## 📸 Output Example

The generated QR code includes:

* Blue QR pattern
* Centered Facebook logo
* Display name in Facebook Blue
* Shortlink text below
* “Scan to follow on Facebook” message
* Footer bar in Facebook Blue

---

## 🛠️ Technical Details

#### Dependencies

* `qrcode`: QR code creation
* `Pillow`: Drawing and composition
* `re`: For extracting user IDs from profile links

#### Error Handling

* Detects malformed URLs
* Generates fallback shortlinks if needed
* Auto-adjusts fonts if unavailable

---

## ⚠️ Notes

* Ensure your profile is public for optimal usability
* Shortlink format makes the QR cleaner and faster to scan
* PNG output preserves crispness and color consistency

---

## 🐛 Troubleshooting

#### QR Doesn’t Scan

* Increase contrast between QR and background
* Raise `box_size`
* Test with multiple QR reader apps

#### Logo Not Appearing

* Ensure `facebook_logo.png` is in the same directory
* Must be a valid image file

#### Font Issues

* Install Arial fonts or adjust to available system fonts
