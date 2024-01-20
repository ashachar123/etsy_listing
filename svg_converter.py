import sys
import time
from datetime import datetime
from PIL import Image, ImageFile
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY
import os
from scipy.interpolate import splprep, splev
import numpy as np
from svgpathtools import svg2paths, wsvg, Path, Line
import re
from shapely.geometry import LineString, Point
import scipy
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import threading


class png2svg:
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path
        ImageFile.LOAD_TRUNCATED_IMAGES = True
    def smooth_path(self, points, smoothing_factor=3):
        # Ensure each element in points is a pair (x, y)
        points_array = np.array([(point.x, point.y) for point in points])

        # Perform spline interpolation
        tck, u = splprep([points_array[:, 0], points_array[:, 1]], s=smoothing_factor)
        u_new = np.linspace(u.min(), u.max(), 1000)  # Adjust the number of points
        x_new, y_new = splev(u_new, tck)
        return list(zip(x_new, y_new))

    @staticmethod
    def parse_svg_path_part(part):
        # Extract the command letter and the rest of the string
        command = part[0]
        coords_string = part[1:]

        # Split the coordinates string into pairs using regular expressions
        coords_pairs = re.findall(r'(\d+\.\d+)', coords_string)

        # Create points from the extracted pairs
        points = []
        for i in range(0, len(coords_pairs), 2):
            x, y = float(coords_pairs[i]), float(coords_pairs[i + 1])
            points.append(Point(x, y))

        return points

    @staticmethod
    def find_latest_file(path, extension):
        list_of_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(extension)]
        return max(list_of_files, key=os.path.getctime) if list_of_files else None
    def simplify_path(self, parts, tolerance=1.0):
        simplified_parts = []
        for part in parts:
            # Parse the SVG path part to get points
            points = self.parse_svg_path_part(part)
            line = LineString([(point.x, point.y) for point in points])
            simplified_line = line.simplify(tolerance)

            # Construct the simplified path part
            simplified_part = f"{part[0]}" + " ".join(f"{x:.2f},{y:.2f}" for x, y in simplified_line.coords)
            simplified_parts.append(simplified_part)
        return simplified_parts

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
        tmp_svg = f"{str(datetime.now()).replace(':', '.').replace(' ', '')}tmp.svg"
        final_svg = f"{str(datetime.now()).replace(':', '.').replace(' ', '')}final.svg"
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
        if image.mode == 'RGBA':
            # Use the alpha channel of the image as a mask
            background.paste(image, (0, 0), image.split()[3])
        else:
            # No transparency, so no mask needed
            background.paste(image, (0, 0))

        bm = Bitmap(background, blacklevel=0.5)
        # bm.invert()
        plist = bm.trace(
            turdsize=10,
            turnpolicy=POTRACE_TURNPOLICY_MINORITY,
            alphamax=0.01,
            opticurve=True,
            opttolerance=8,
        )

        with open(f"outputs/{tmp_svg}", "w") as fp:
            fp.write(
                '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="4000" height="4000" viewBox="0 0 4000 4000">'''
            )
            parts = []
            for curve in plist:
                fs = curve.start_point
                segment_parts = [f"M{fs.x},{fs.y}"]
                for segment in curve.segments:
                    if segment.is_corner:
                        a = segment.c
                        b = segment.end_point
                        segment_parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
                    else:
                        a = segment.c1
                        b = segment.c2
                        c = segment.end_point
                        segment_parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
                segment_parts.append("z")
                parts.append(" ".join(segment_parts))

            # Simplify the paths
            tolerance = 2# Adjust this value to get the desired simplification
            simplified_parts = self.simplify_path(parts, tolerance)
            smoothed_parts = []
            for part in simplified_parts:
                points = self.parse_svg_path_part(part)
                smoothed_points = self.smooth_path(points)
                smoothed_part = f"M" + " ".join(f"{x:.2f},{y:.2f}" for x, y in smoothed_points)
                smoothed_parts.append(smoothed_part)
            with open(f"outputs/{tmp_svg}", "w") as fp:
                fp.write(
                    '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="4000" height="4000" viewBox="0 0 4000 4000">'''
                )
                fp.write(f'<path stroke="none" fill="black" fill-rule="evenodd" d="{"".join(simplified_parts)}"/>')
                fp.write("</svg>")
                fp.close()

            print("Generated temp svg")
            return tmp_svg


    def file_to_svg(self):
        tmp_svg = self.create_temp_svg()
        self.create_png_and_svg(f"outputs/{tmp_svg}")

    # output_filename = r"C:\Users\Amit Shachar\Documents\etsy\Mosaic Flowers\Stock\output.svg"

if __name__ == '__main__':
    input_filename = r"/Users/amitshachar/Documents/etsy/43/Stock/DALL0_1.png"

    png2svg(input_filename, "outputs").file_to_svg()
