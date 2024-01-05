import sys
from PIL import Image
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class png2svg:
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path

    def create_png(self, input_vector_file):
        filename = str(len(os.listdir(self.output_path)) + 1)
        inkscape_command = (
            f'inkscape {input_vector_file} '
            f'--export-filename={self.output_path}\\{filename}.png '
            f'--export-dpi=300 '
            f'--export-width=4000 '
            f'--export-height=4000 '
            f'--export-background-opacity=0'
        )

        # Execute the Inkscape command using os.system
        os.system(inkscape_command)

        inkscape_command = (
            f'inkscape {input_vector_file} '
            f'--export-filename={self.output_path}\\{filename}.svg '
            f'--export-dpi=300 '
            f'--export-width=4000 '
            f'--export-height=4000 '
            f'--export-background-opacity=0'
        )

        # Execute the Inkscape command using os.system
        os.system(inkscape_command)

    def file_to_svg(self):
        try:
            image = Image.open(self.input_file)
        except IOError:
            print(f"Image ({self.input_file}) could not be loaded.")
            return

        # Set the size of the image to 4000x4000 and DPI to 300
        image = image.resize((4000, 4000), resample=Image.LANCZOS)
        image.info['dpi'] = (300, 300)

        # Create a white background image with the same size
        background = Image.new('RGB', (4000, 4000), (255, 255, 255))
        background.paste(image, (0, 0), image)

        bm = Bitmap(background, blacklevel=0.5)
        # bm.invert()
        plist = bm.trace(
            turdsize=2,
            turnpolicy=POTRACE_TURNPOLICY_MINORITY,
            alphamax=1,
            opticurve=False,
            opttolerance=0.2,
        )

        with open("outputs\\tmp.svg", "w") as fp:
            fp.write(
                '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="4000" height="4000" viewBox="0 0 4000 4000">'''
            )
            parts = []
            for curve in plist:
                fs = curve.start_point
                parts.append(f"M{fs.x},{fs.y}")
                for segment in curve.segments:
                    if segment.is_corner:
                        a = segment.c
                        b = segment.end_point
                        parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
                    else:
                        a = segment.c1
                        b = segment.c2
                        c = segment.end_point
                        parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
                parts.append("z")
            fp.write(f'<path stroke="none" fill="black" fill-rule="evenodd" d="{"".join(parts)}"/>')
            fp.write("</svg>")
        self.create_png("outputs\\tmp.svg")


if __name__ == '__main__':
    input_filename = r"C:\Users\Amit Shachar\Documents\etsy\Mosaic Flowers\Stock\DALL·E 2024-01-03 20.48.33 - A thick lined, monoline image of a beautiful rose mosaic, depicted in black on a white background, suitable for laser cutting. The design features int.png"
    output_filename = r"C:\Users\Amit Shachar\Documents\etsy\Mosaic Flowers\Stock\output.svg"

    png2svg("outputs\\input.png", "outputs").file_to_svg()
