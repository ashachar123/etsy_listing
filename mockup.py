import shutil

from PIL import Image
import cv2
import numpy as np
import os
import random


class Mockup:
    def __init__(self, mockup_path, product_path, output_path):
        self.mockup_path = mockup_path
        self.poduct_path = product_path
        self.output_path = output_path
        self.fps = 10
        self.frames_per_image = 3 * self.fps
        self.width = 2000
        self.height = 2000


    def get_files(self, path, is_png=False):
        if is_png:
            return [os.path.join(path, file) for file in os.listdir(path) if "png" in file]
        else:
            return [os.path.join(path, file) for file in os.listdir(path)]


    def copy_and_paste_region(self, image, x, y, w, h):
        """ Copy a region from right of the square and paste it over the square. """
        # Define the region to the right of the square
        right_x = x + w  # Start from the right edge of the square
        right_y = y
        right_w = w
        right_h = h

        # Check if the right region goes beyond the image boundary
        if right_x + right_w > image.shape[1]:
            # Adjust the width if it exceeds the image's width
            right_w = image.shape[1] - right_x

        # Copy the region from the right of the square
        copied_region = image[right_y:right_y + right_h, right_x:right_x + right_w].copy()

        # Paste the copied region over the square
        image[y:y + h, x:x + w] = cv2.resize(copied_region, (w, h))

    @staticmethod
    def define_purple(image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_purple = np.array([130, 50, 50])
        upper_purple = np.array([170, 255, 255])

        return cv2.inRange(hsv_image, lower_purple, upper_purple)

    def create_mockup(self):
        for mockup_index, mockup in enumerate(self.get_files(self.mockup_path)):

            image = cv2.imread(mockup)
            purple_mask = self.define_purple(image)
            contours, _ = cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            height = image.shape[0]
            width = image.shape[1]
            new_size = (width // 2 - 200, height // 2 - 200)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 10 < 30 and h > 10 < 30:
                    self.copy_and_paste_region(image, x, y, w + 5, h + 5)
            pillow_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            number = 0
            print(f"this is the self.poduct_path - {self.poduct_path}")

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 10 < 15 and h > 10 < 15:
                    images = self.get_files(self.poduct_path, is_png=True)
                    if mockup[-5] != '1':
                        print(f"this is index of mockup_index {mockup_index}")
                        print(f"this is images {images}")
                        png_image = Image.open(images[mockup_index -1])
                    else:
                        png_image = Image.open(images[number])
                        number += 1

                    #turn down new size to less than a quarter
                    png_image = png_image.resize(new_size)
                    center_x = x + w // 2
                    center_y = y + h // 2

                    paste_x = center_x - png_image.width // 2
                    paste_y = center_y - png_image.height // 2
                    region = pillow_image.crop((x, y, x + w, y + h))

                    pillow_image.paste(png_image, (paste_x, paste_y), png_image)


            output_image_path = f'{self.output_path}{mockup_index}.jpg'
            pillow_image.save(output_image_path)
            # pillow_image.show()
        self.generate_video()
        print(f"created mockups in {self.output_path}.jpg")

    def generate_video(self):
        output_video = cv2.VideoWriter(f'{self.output_path}/output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        image_paths = [f"{self.output_path}/{file}" for file in os.listdir(self.output_path) if ".jpg" in file]
        transition_frames = int(self.fps)
        for i in range(len(image_paths) - 1):
            img1 = cv2.imread(image_paths[i])
            img2 = cv2.imread(image_paths[i + 1])

            if img1 is not None and img2 is not None:
                # Resize images to match the video resolution
                img1 = cv2.resize(img1, (self.width, self.height))
                img2 = cv2.resize(img2, (self.width, self.height))

                # Determine the number of frames to allocate for each image
                frames_img1 = self.frames_per_image - transition_frames
                frames_img2 = self.frames_per_image - frames_img1

                # Add the first image with its allocated frames
                for _ in range(frames_img1):
                    output_video.write(img1)

                # Apply crossfade transition
                for alpha in range(0, transition_frames):
                    blended_frame = cv2.addWeighted(img1, 1 - alpha / float(transition_frames), img2,
                                                    alpha / float(transition_frames), 0)
                    output_video.write(blended_frame)

                # Add the second image with its allocated frames
                for _ in range(frames_img2):
                    output_video.write(img2)

        # Release the VideoWriter
        output_video.release()
        os.rename(f'{self.output_path}/output_video.mp4', f'{self.output_path}/output_video_rdy.mp4')




if __name__ == "__main__":
    Mockup(mockup_path="mockupa", product_path=r"etsy/4/Product", output_path=r"etsy/4/Mockup").create_mockup()
# Optionally, convert the Pillow image back to OpenCV format for further processing
# output_image_cv = cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)
