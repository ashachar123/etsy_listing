from PIL import Image
import potrace
import numpy as np

def png_to_svg(png_path, output_svg_path, output_png_path, resize_factor=2):
    # Open the PNG file with Pillow
    with Image.open(png_path) as img:
        # Convert image to grayscale (necessary for potrace)
        img_gray = img.convert('L')

        # Create a bitmap from the grayscale image
        bitmap = potrace.Bitmap(np.array(img_gray))
        # Trace the bitmap to a path
        path = bitmap.trace()

        # Export to SVG
        with open(output_svg_path, 'w') as f:
            path.write(f, 'SVG')

        # Resize image
        new_size = tuple([dimension * resize_factor for dimension in img.size])
        img_resized = img.resize(new_size, Image.ANTIALIAS)

        # Save the resized image as PNG
        img_resized.save(output_png_path)

def reduce_image_size(input_path, output_path, scale_factor=0.5):
    with Image.open(input_path) as img:
        # Calculate the new size
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        # Resize the image
        resized_img = img.resize(new_size)
        # Save the resized image
        resized_img.save(output_path)

# Example usage
reduce_image_size("test1.png", "reduced_input.png")

# Example usage
png_to_svg("reduced_input.png", "output.svg", "output.png", resize_factor=2)
