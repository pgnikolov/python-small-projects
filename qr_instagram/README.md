# 🎨 Instagram QR Code Generator

A powerful Python script that generates stunning, professional-looking QR codes for Instagram profiles — featuring gradient color effects, logo integration, rounded corners, and multiple style modes.

---

## ✨ Features

* **Instagram Gradient Styling:** Classic multi-tone Instagram gradient for colorful QR codes
* **Smooth Gradient Mode:** Soft blended color transitions for a modern, elegant look
* **Black & White Mode:** Clean minimalist QR codes for professional branding
* **Rounded Corners:** Optional rounded edges for a polished finish
* **Custom Logo Integration:** Automatically loads or generates an Instagram-style logo
* **Interactive Menu System:** Simple text interface to choose between modes
* **Customizable Text Area:** Adds your Instagram handle and “Scan to follow” prompt
* **High-Quality Output:** Exports crisp PNG images ready for web or print

---

## ⚙️ Quick Start

### Prerequisites

* Python 3.6 or higher
* Required Python packages:

```bash
pip install qrcode[pil] pillow
```

---

## 🚀 Installation

#### 1. Clone or download the script:

```bash
git clone <repository-url>
cd instagram-qr-generator
```

#### 2. Install dependencies:

```bash
pip install qrcode[pil] pillow
```

#### 3. (Optional) Add your own Instagram logo:

Place a file named `instagram_logo.png` in the same directory.
If missing, a fallback gradient logo will be auto-generated.

---

## 🧭 Usage

### Run the script:

```bash
python instagram_qr_generator.py
```

### Interactive menu options:

1. **Color Gradient QR Code** — vibrant Instagram multi-color gradient
2. **Smooth Gradient QR Code** — soft gradient transitions
3. **Black & White QR Code** — simple professional look
4. **Generate All Versions** — automatically creates all three variants

### Additional options:

* Choose whether to add **rounded corners**
* Adjust **corner radius** (default: 40)

---

## 🧩 Modes Overview

### 🌈 1. Color Gradient Mode (`create_instagram_qr_with_local_logo`)

* Uses 10 signature Instagram colors
* Each QR module receives a unique color for a vibrant result
* File output: `qr_instagram.png` or `qr_instagram_rounded.png`

### 🌤️ 2. Smooth Gradient Mode (`create_instagram_qr_smooth_gradient`)

* Blends five key Instagram colors for a smooth transition
* File output: `qr_instagram_smooth.png` or `qr_instagram_smooth_rounded.png`

### ⚫⚪ 3. Black & White Mode (`create_instagram_qr_black_white`)

* Generates a clean, minimalist monochrome QR code
* File output: `qr_instagram_bw.png` or `qr_instagram_bw_rounded.png`

---

## 🧠 Customization

### 🎨 Modify Gradient Colors

Discrete gradient palette:

```python
INSTAGRAM_GRADIENT = [
    "#405DE6", "#5851DB", "#833AB4", "#C13584",
    "#E1306C", "#FD1D1D", "#F56040", "#F77737",
    "#FCAF45", "#FFDC80"
]
```

Smooth gradient palette:

```python
GRADIENT_COLORS = ["#405DE6", "#833AB4", "#E1306C", "#F77737", "#FFDC80"]
```

---

### 🧱 Adjust QR Code Parameters

```python
qr = qrcode.QRCode(
    version=1,  # Size of the QR code (1–40)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
    box_size=12,  # Size of each module in pixels
    border=4,  # Border width in modules
)
```

---

### 🖋️ Font Customization

```python
font_large = ImageFont.truetype("arialbd.ttf", 26)  # Bold username font
font_small = ImageFont.truetype("arial.ttf", 18)    # Subtitle text font
```

If unavailable, system default fonts are used automatically.

---

### 🌀 Rounded Corners

Add or adjust rounded edges:

```python
final_img = add_rounded_corners(final_img, corner_radius=40)
```

---

## 📁 File Structure

```bash
instagram-qr-generator/
├── instagram_qr_generator.py         # Main script
├── instagram_logo.png                # Optional custom logo
├── qr_instagram.png                  # Gradient version
├── qr_instagram_smooth.png           # Smooth gradient version
├── qr_instagram_bw.png               # Black & white version
└── README.md                         # This file
```

---

## 📸 Output Examples

Generated QR codes include:

* Centered Instagram logo (custom or auto-generated)
* Colored or monochrome QR pattern
* Username handle with gradient text
* “Scan to follow” caption
* Gradient or black footer bar
* Optional rounded corners for a modern feel

---

## 🛠️ Technical Details

* **Libraries:** `qrcode`, `PIL/Pillow`, `random`
* **Error Correction:** Level H for maximum scan reliability
* **Fallback Handling:**

  * Missing logo → auto-generated gradient icon
  * Missing fonts → system default substitution
  * Invalid input → safe fallback defaults

---

## 🤝 Contributing

Contributions are welcome!
You can improve or extend this project by adding:

* New gradient algorithms
* Animated QR versions
* Custom font or color presets
* Dark/light theme compatibility

---

## 📄 License

This project is licensed under the **MIT License** — see the LICENSE file for details.

---

## ⚠️ Notes

* Make sure your Instagram profile is **public** for scan access
* Test generated QR codes with multiple scanners
* Higher error correction → larger but more reliable QR codes
* PNG output preserves transparency and quality

---

## 🐛 Troubleshooting

### QR Code Doesn’t Scan

* Increase `box_size`
* Check for sufficient color contrast
* Avoid overly busy backgrounds

### Logo Missing

* Ensure `instagram_logo.png` is in the working directory
* Use a **transparent PNG** for best results

### Font Errors

* Install `Arial` or edit paths to available fonts
* Defaults will apply automatically if fonts are missing
