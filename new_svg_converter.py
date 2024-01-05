import os

# Path to your input vector file (replace with your actual file path)
input_vector_file = "outputs/input.svg"

# Path to output PNG and SVG files
output_png_file = "outputs/output_image.png"
output_svg_file = "outputs/output_image.svg"

# Define the Inkscape command
inkscape_command = (
    f'inkscape {input_vector_file} '
    f'--export-filename={output_png_file} '
    f'--export-dpi=300 '
    f'--export-width=4000 '
    f'--export-height=4000 '
    f'--export-background-opacity=0'
)

# Execute the Inkscape command using os.system
os.system(inkscape_command)

inkscape_command = (
    f'inkscape {input_vector_file} '
    f'--export-filename={output_svg_file} '
    f'--export-dpi=300 '
    f'--export-width=4000 '
    f'--export-height=4000 '
    f'--export-background-opacity=0'
)

# Execute the Inkscape command using os.system
os.system(inkscape_command)


print(f"Files exported: {output_png_file}, {output_svg_file}")