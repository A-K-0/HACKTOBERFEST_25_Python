# QR Code Generator and Reader 📱

Simple command-line tool to create and scan QR codes.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make a QR code**
   ```bash
   python qr_generator.py generate "Hello World!" -o hello.png
   ```

3. **Scan a QR code** (optional - needs zbar)
   ```bash
   python qr_generator.py scan hello.png
   ```

## Examples

**Basic QR code:**
```bash
python qr_generator.py generate "Hello World!" -o hello.png
```

**Website link:**
```bash
python qr_generator.py generate "https://github.com" -o github.png
```

**Custom colors:**
```bash
python qr_generator.py generate "Colorful!" --fill-color blue --back-color yellow -o colorful.png
```

**WiFi sharing:**
```bash
python qr_generator.py generate "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;" -o wifi.png
```

## Options

- `-o, --output`: Output filename
- `-e, --error-correction`: L, M, Q, or H (default: M)
- `--fill-color`: QR code color
- `--back-color`: Background color
- `--box-size`: Size of each square
- `--border`: Border thickness

