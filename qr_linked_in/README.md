# LinkedIn QR Code Generator
A Python script that generates elegant, LinkedIn-themed QR codes for professional profiles — featuring custom branding, a corporate blue palette, and rounded-corner design.

---

## Features

* **LinkedIn Blue Styling:** Uses LinkedIn's signature blue color for clean, professional QR codes
* **Custom Logo Integration:** Automatically embeds your LinkedIn logo or generates a fallback logo
* **Rounded Corners:** Smooth, modern rounded edges for a polished finish
* **Personalized Text Area:** Displays your name, short LinkedIn URL, and a “Scan to connect” message
* **High-Quality Output:** Exports crisp, high-resolution PNG images
* **Auto Shortlink Detection:** Accepts both full URLs and simple usernames

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
cd linkedin-qr-generator
```

#### 2. Ensure you have the required dependencies:

```bash
pip install qrcode[pil] pillow
```

#### 3. (Optional) Place your LinkedIn logo as `linkedin-logo.png` in the same directory

---

## Basic Usage

### Run the script and follow the prompts:

```bash
python linkedin_qr_generator.py
```

#### The script will:

1. Ask for your LinkedIn profile URL or username
2. Automatically extract or build your LinkedIn shortlink
3. Request your display name
4. Generate a sleek LinkedIn-style QR code
5. Save it as `qr_linkedin_rounded_edges.png`

---

## Customization Options

### Color and Styling

* Default color is LinkedIn Blue:

  ```python
  LINKEDIN_BLUE = "#225982"
  ```
* You can modify it to any corporate color scheme for custom branding.

### Font Configuration

Change or customize font settings here:

```python
font_large = ImageFont.truetype("arialbd.ttf", 24)  # Display name
font_medium = ImageFont.truetype("arial.ttf", 18)   # Shortlink
font_small = ImageFont.truetype("arial.ttf", 14)    # Subtitle text
```

If unavailable, system default fonts are used automatically.

### Rounded Corners

Adjust the corner radius:

```python
radius = 40  # corner radius
```

Increase or decrease for sharper or softer corners.

---

## 📁 File Structure

```bash
linkedin-qr-generator/
├── linkedin_qr_generator.py     # Main script
├── linkedin-logo.png            # Optional LinkedIn logo
├── qr_linkedin_rounded_edges.png # Generated QR code
└── README.md                    # This file
```

---

## 🛠️ Technical Details

#### Dependencies

* `qrcode`: QR code generation
* `PIL/Pillow`: Image drawing and processing

#### Key Features

* **Rounded corner masking** for a premium finish
* **Error correction level H** for reliable scanning
* **High-quality resampling** for logo placement
* **Smart shortlink extraction** from profile URLs

---

## 📸 Output Example

The generated QR code includes:

* LinkedIn-blue QR modules
* Centered logo with white background
* Display name (your name)
* Short LinkedIn URL
* “Scan to connect on LinkedIn” text
* LinkedIn-blue footer bar
* Smooth rounded edges for a professional look

---

## 🤝 Contributing

Contributions are welcome!
Feel free to submit pull requests for:

* Additional layout or font options
* Color theme presets (e.g., dark mode)
* Logo positioning improvements
* Performance or UX enhancements

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## ⚠️ Notes

* Ensure your LinkedIn profile is public for easy access
* Test the QR code with multiple devices or QR scanners
* PNG format preserves transparency for clean design
* Rounded corners improve appearance but may require transparent backgrounds

---

## 🐛 Troubleshooting

#### QR Code Doesn’t Scan:

* Increase `box_size` value in the QRCode settings
* Ensure strong contrast between background and QR code
* Test under good lighting and high display brightness

#### Logo Not Appearing:

* Check that `linkedin-logo.png` exists in the script directory
* Ensure the file is a valid image format (PNG recommended)
* The fallback logo will auto-generate if missing

#### Font Issues:

* Install `Arial` or modify paths to use available fonts
* Script falls back to default system fonts if necessary
