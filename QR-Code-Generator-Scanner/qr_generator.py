#!/usr/bin/env python3

import qrcode
import argparse
import sys
import os
from PIL import Image
from pyzbar import pyzbar
from typing import Optional, List


class QRCodeGenerator:
    
    def __init__(self, box_size: int = 10, border: int = 4):
        self.box_size = box_size
        self.border = border
    
    def generate_qr_code(self, data: str, error_correction: str = 'M') -> qrcode.QRCode:
        error_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_levels.get(error_correction.upper(), 
                                            qrcode.constants.ERROR_CORRECT_M),
            box_size=self.box_size,
            border=self.border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr
    
    def save_qr_code(self, qr_code: qrcode.QRCode, filename: str, 
                     fill_color: str = 'black', back_color: str = 'white') -> bool:
        try:
            img = qr_code.make_image(fill_color=fill_color, back_color=back_color)
            img.save(filename)
            return True
        except Exception as e:
            print(f"Oops! Couldn't save the QR code: {e}")
            return False
    
    def generate_and_save(self, data: str, filename: str, 
                         error_correction: str = 'M',
                         fill_color: str = 'black', 
                         back_color: str = 'white') -> bool:
        qr_code = self.generate_qr_code(data, error_correction)
        return self.save_qr_code(qr_code, filename, fill_color, back_color)


class QRCodeScanner:
    
    @staticmethod
    def scan_qr_code(image_path: str) -> List[str]:
        try:
            image = Image.open(image_path)
            qr_codes = pyzbar.decode(image)
            
            decoded_data = []
            for qr_code in qr_codes:
                data = qr_code.data.decode('utf-8')
                decoded_data.append(data)
            
            return decoded_data
            
        except FileNotFoundError:
            print(f"Hmm, can't find the image '{image_path}'. Double-check the path?")
            return []
        except Exception as e:
            print(f"Something went wrong while scanning: {e}")
            return []
    
    @staticmethod
    def scan_and_display(image_path: str) -> None:
        decoded_data = QRCodeScanner.scan_qr_code(image_path)
        
        if decoded_data:
            print(f"Great! Found {len(decoded_data)} QR code(s) in '{image_path}':")
            for i, data in enumerate(decoded_data, 1):
                print(f"  {i}. {data}")
        else:
            print(f"No QR codes found in '{image_path}'. Maybe try a different image?")


def main():
    parser = argparse.ArgumentParser(
        description='QR Code Generator and Scanner - Make QR codes easily!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate QR code:
    python qr_generator.py generate "Hello, World!" -o hello.png
    python qr_generator.py generate "https://github.com" -o github.png -e H
    
  Scan QR code:
    python qr_generator.py scan hello.png
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='What do you want to do?')
    
    generate_parser = subparsers.add_parser('generate', help='Create a QR code')
    generate_parser.add_argument('data', help='What text or URL to put in the QR code')
    generate_parser.add_argument('-o', '--output', default='qrcode.png',
                               help='Where to save it (default: qrcode.png)')
    generate_parser.add_argument('-e', '--error-correction', 
                               choices=['L', 'M', 'Q', 'H'], default='M',
                               help='How much error correction? L=low, M=medium, Q=good, H=high')
    generate_parser.add_argument('--fill-color', default='black',
                               help='QR code color')
    generate_parser.add_argument('--back-color', default='white',
                               help='Background color')
    generate_parser.add_argument('--box-size', type=int, default=10,
                               help='How big should each square be?')
    generate_parser.add_argument('--border', type=int, default=4,
                               help='Border thickness')
    
    scan_parser = subparsers.add_parser('scan', help='Read a QR code from an image')
    scan_parser.add_argument('image', help='Path to your image file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'generate':
        generator = QRCodeGenerator(box_size=args.box_size, border=args.border)
        
        success = generator.generate_and_save(
            data=args.data,
            filename=args.output,
            error_correction=args.error_correction,
            fill_color=args.fill_color,
            back_color=args.back_color
        )
        
        if success:
            print(f"✅ Your QR code is ready! Saved as: {args.output}")
            print(f"📝 Contains: {args.data}")
        else:
            print("❌ Something went wrong creating your QR code")
            sys.exit(1)
    
    elif args.command == 'scan':
        if not os.path.exists(args.image):
            print(f"❌ Can't find '{args.image}'. Make sure the file exists!")
            sys.exit(1)
        
        QRCodeScanner.scan_and_display(args.image)


if __name__ == '__main__':
    main()
