# Instagram QR Code Generator

A Python script that creates beautiful, gradient-styled QR codes for Instagram profiles with custom branding and visual effects.



## Features

- **Instagram Gradient Styling:** QR codes feature Instagram's iconic gradient colors
- **Custom Logo Integration:** Add your Instagram logo or use auto-generated fallback
- **Gradient Text Effects:** Username displays with colorful gradient styling
- **Professional Layout:** Clean design with "Scan to follow" text and gradient bars
- **Two Generation Modes:** Choose between discrete or smooth gradient effects
- **High Quality Output:** Export as high-resolution PNG images

## Quick Start

### Prerequisites

- Python 3.6 or higher
- Required Python packages:
```bash
pip install qrcode[pil] pillow
```

## Installation

#### 1. Clone or download the script:
```bash
git clone <repository-url>
cd instagram-qr-generator
```

#### 2. Ensure you have the required dependencies:
```bash
pip install qrcode[pil] pillow
```

#### 3. (Optional) Place your Instagram logo as instagram_logo.png in the same directory


## Basic Usage

### Run the script and follow the prompts:
```bash
python instagram_qr_generator.py
```

#### The script will:
1. Ask for your Instagram profile URL
2. Request your Instagram handle (with @)
3. Generate a beautifully styled QR code
4. Save it as `qr_instagram.png`

## Customization Options

### Two Generation Modes

1. Discrete Gradient (`create_instagram_qr_with_local_logo`)
    - Uses Instagram's 10-color gradient palette
    - Each QR module gets a distinct gradient color
    - More vibrant and colorful appearance
2. Smooth Gradient (`create_instagram_qr_smooth_gradient`)
    - Blends between 5 main Instagram colors
    - Creates smoother color transitions
    - More subtle and professional look

## 📁 File Structure

```bash
instagram-qr-generator/
├── instagram_qr_generator.py  # Main script
├── instagram_logo.png         # Optional custom logo
├── qr_instagram.png           # Generated QR code
└── README.md                  # This file
```

## 🔧 Advanced Usage

#### Modifying Colors

Edit the gradient color arrays in the functions:
```python
# For discrete gradient
INSTAGRAM_GRADIENT = [
    "#405DE6", "#5851DB", "#833AB4", "#C13584",
    "#E1306C", "#FD1D1D", "#F56040", "#F77737",
    "#FCAF45", "#FFDC80"
]

# For smooth gradient
GRADIENT_COLORS = ["#405DE6", "#833AB4", "#E1306C", "#F77737", "#FFDC80"]
```
#### Changing QR Code Parameters

```python
qr = qrcode.QRCode(
    version=1,                    # Controls size (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction level
    box_size=12,                  # Pixel size of each box
    border=4,                     # Border size in boxes
)
```

#### Custom Fonts

```python
font_large = ImageFont.truetype("arialbd.ttf", 26)  # Bold for username
font_small = ImageFont.truetype("arial.ttf", 18)    # Regular for subtitle
```

## 📸 Output Example

The generated QR code includes:
  - Instagram-gradient colored QR pattern
  - Centered logo (custom or generated)
  - Gradient-styled username handle
  - "Scan to follow" instruction text
  - Instagram gradient color bar at the bottom


## 🛠️ Technical Details

#### Dependencies
  - `qrcode`: QR code generation
  - `PIL/Pillow`: Image processing and manipulation
  - `random`: Color selection randomization

#### Error Handling
  - Logo Not Found: Automatically generates a fallback Instagram-style icon
  - Font Issues: Falls back to system default fonts if specified fonts unavailable
  - QR Code Generation: Uses high error correction for better scan reliability


## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests for:
  - Additional styling options
  - Improved gradient algorithms
  - Better font handling
  - Performance optimizations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Notes

- Ensure your Instagram profile is public for the QR code to work effectively
- Test the generated QR code with multiple QR scanners
- Higher error correction levels create more complex but reliable QR codes
- The script currently supports PNG output format

## 🐛 Troubleshooting

#### QR Code Doesn't Scan:
  - Try increasing the box_size parameter
  - Ensure adequate contrast between QR code and background
  - Test with different QR scanner apps

#### Logo Not Appearing:
  - Verify instagram_logo.png is in the correct directory
  - Check that the logo file is a valid image format
  - Ensure the logo has appropriate transparency (PNG recommended)

#### Font Issues:
  - Install the required fonts on your system
  - Modify the font paths in the script to use available fonts
