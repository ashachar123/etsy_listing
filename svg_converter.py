import sys
import time
from datetime import datetime
from PIL import Image
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import threading


class png2svg:
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path

    @staticmethod
    def find_latest_file(path, extension):
        list_of_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(extension)]
        return max(list_of_files, key=os.path.getctime) if list_of_files else None




    def create_png_and_svg(self, input_vector_file):
        inkscape_command_png = (
            f'inkscape {input_vector_file} '
            f'--export-type=png '
            f'--export-dpi=300 '
            f'--export-width=4000 '
            f'--export-height=4000 '
            f'--export-background-opacity=0'
        )
        os.system(inkscape_command_png)

        if exported_svg := self.find_latest_file("outputs", ".png"):
            filename = str(len(os.listdir(self.output_path)) + 1)
            base_export_path = self.output_path + "/" + filename
            os.rename(exported_svg, f'{base_export_path}.png')

        print(f"generated png at {base_export_path}")


        inkscape_command_svg = (
            f'inkscape {input_vector_file} '
            f'--export-type=svg '
            f'--export-dpi=300 '
            f'--export-width=4000 '
            f'--export-height=4000 '
            f'--export-background-opacity=0'
        )
        os.system(inkscape_command_svg)


        if exported_svg := self.find_latest_file("outputs", ".svg"):
            os.rename(exported_svg, f'{base_export_path}.svg')
        print(f"generated svg at {base_export_path}")

    def create_temp_svg(self):
        tmp_svg = f"{str(datetime.now()).replace(':', '.').replace(' ', '')}.svg"
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

        with open(f"outputs/{tmp_svg}", "w") as fp:
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
            fp.close()
        print("Generated temp svg")
        return tmp_svg


    def file_to_svg(self):
        tmp_svg = self.create_temp_svg()
        self.create_png_and_svg(f"outputs/{tmp_svg}")

    output_filename = r"C:\Users\Amit Shachar\Documents\etsy\Mosaic Flowers\Stock\output.svg"

if __name__ == '__main__':
    input_filename = r"C:\Users\Amit Shachar\Documents\etsy\test11\Stock\DALL·E 2024-01-06 14.40.22 - A hand-drawn, thick monoline illustration of butterflies flying towards the moon, suitable for laser cutting. The design features a variety of butterf.png"

    png2svg(input_filename, "outputs").file_to_svg()
