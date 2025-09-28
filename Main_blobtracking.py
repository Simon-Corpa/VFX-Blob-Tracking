import cv2
import numpy as np
import pandas as pd
import random
import os
from PIL import Image, ImageDraw, ImageFont
from itertools import combinations
import textwrap

def compute_canny_difference(frame1, frame2, low_threshold=50, high_threshold=150):
    if frame1 is None or frame2 is None:
        return None

    edges1 = cv2.Canny(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY), low_threshold, high_threshold)
    edges2 = cv2.Canny(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), low_threshold, high_threshold)
    difference = cv2.absdiff(edges1, edges2)
    return difference

def apply_blur_and_threshold(image, blur_ksize=5, thresh_value=127):
    if image is None:
        return None

    blurred = cv2.GaussianBlur(image, (blur_ksize, blur_ksize), 0)
    _, thresholded = cv2.threshold(blurred, thresh_value, 255, cv2.THRESH_BINARY)
    return thresholded


def process_white_pixels(image, d=5, alpha=None):
    if image is None:
        return []

    assert len(image.shape) == 2, "Input image must be grayscale/binary."

    if alpha is not None:
        assert len(alpha.shape) == 2, "`alpha` must be a 2D binary image."

        # Instead of asserting, provide more specific error messages
        if alpha.shape != image.shape:
            raise ValueError(f"Dimension mismatch: image shape {image.shape} != alpha shape {alpha.shape}")

    processed_image = image.copy()
    white_points = []

    # Get all white pixel indices from the input image
    white_pixel_indices = np.argwhere(processed_image == 255)

    for x, y in white_pixel_indices:
        # Check the `alpha` mask if provided
        if alpha is not None and alpha[x, y] == 255:
            continue  # Skip this point, as it's masked out by `alpha`

        if processed_image[x, y] == 255:
            white_points.append((x, y))
            # Black out pixels within radius `d` around this pixel
            cv2.circle(processed_image, (y, x), int(d), (0), thickness=-1)

    return white_points


def visualize_points_with_text(image, points, csv_path, text_params):
    """
    Visualizes points by rendering text from a CSV above each point and optionally drawing connecting lines.
    The function will create an image with an alpha channel (transparency), displaying only the drawn elements.
    The `alpha_mask` can be used to mask out areas of the overlay where the mask is white.
    """

    # Create a transparent background (RGBA) image with the same size as the input image
    height, width = image.shape[:2]
    overlay = np.zeros((height, width, 4), dtype=np.uint8)  # 4 channels: RGBA

    # Convert the OpenCV image (BGR) to a Pillow image (RGBA) to draw text
    pil_image = Image.fromarray(overlay, 'RGBA')
    draw = ImageDraw.Draw(pil_image)

    # Extract text parameters from the dictionary
    font_list = text_params.get('font_list', [])
    size_list = text_params.get('size_list', [])
    color_list = text_params.get('color_list', [])
    char_limit = text_params.get('char_limit', 150)  # Max pixel width for text
    square_size_list = text_params.get('square_size_list', [10])
    char_spacing = text_params.get('char_spacing', 2)
    lines_param = text_params.get('lines', "no")
    deletion_factor = text_params.get('deletion_factor', 0)  # Default to no deletion

    # Reduce the list of points based on the deletion factor
    if 0 <= deletion_factor <= 1:
        points = random.sample(points, int(len(points) * (1 - deletion_factor)))

    # Read the CSV into a pandas DataFrame
    text_data = pd.read_csv(csv_path)
    rows = text_data.values.tolist()

    # Draw lines if lines_param is a valid ratio
    if isinstance(lines_param, (float, int)) and 0 <= lines_param <= 1:
        # Calculate all possible pairs of points
        point_pairs = list(combinations(points, 2))

        # Select a subset of the connections based on the ratio
        num_lines = int(lines_param * len(point_pairs))
        chosen_lines = random.sample(point_pairs, num_lines)

        # Draw the selected lines
        for (x1, y1), (x2, y2) in chosen_lines:
            line_color = random.choice(color_list)  # Random line color
            # Draw the line directly on the RGBA image (alpha channel is unaffected)
            draw.line([y1, x1, y2, x2], fill=line_color, width=1)

    for x, y in points:
        # Randomly choose a row from the CSV
        chosen_row = random.choice(rows)
        text_lines = []

        # Randomly select font, size, color, and square size
        font_path = random.choice(font_list)
        font_size = random.choice(size_list)
        font_color = random.choice(color_list)
        square_size = random.choice(square_size_list)

        # Load the font using Pillow
        font = ImageFont.truetype(font_path, font_size)

        # Process each column in the row
        for col in chosen_row:
            if pd.notna(col) and str(col).strip():  # Skip empty or NaN values
                col_text = str(col)

                # Break text into lines that fit within the char_limit
                wrapped_lines = textwrap.wrap(col_text, width=char_limit)
                for line in wrapped_lines:
                    text_lines.append(line)

        # If there is no text to display for this row, skip this point
        if not text_lines:
            continue

        # Calculate the bounding box height of each line, including character spacing
        total_text_height = 0
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)  # Get bounding box of text
            line_height = bbox[3] - bbox[1]  # Height of the text
            total_text_height += line_height + char_spacing

        # Determine where to start rendering text (above the square)
        text_start_y = x - square_size - total_text_height
        if text_start_y < 0:
            text_start_y = 0  # Ensure text doesn't go off the top of the image

        # Draw an empty square at the point (outline only) using RGBA
        draw.rectangle(
            [y - square_size // 2, x - square_size // 2, y + square_size // 2, x + square_size // 2],
            outline=font_color,
            width=1
        )

        # Render each line of text using Pillow
        current_y = text_start_y
        tracking = text_params.get('tracking', 2)  # Default tracking is 0 (no extra spacing)

        for line in text_lines:
            current_x = y  # Start X position for the line
            for char in line:
                # Draw each character individually with tracking
                draw.text((current_x, current_y), char, font=font, fill=font_color)

                # Calculate the width of the character and add tracking
                char_width = draw.textbbox((0, 0), char, font=font)[2]
                current_x += char_width + tracking  # Move to the next character position

            # Move to the next line
            bbox = draw.textbbox((0, 0), line, font=font)  # Get bounding box of the whole line
            line_height = bbox[3] - bbox[1]
            current_y += line_height + char_spacing

    # Convert the Pillow image back to OpenCV format (BGRA) to keep transparency
    overlay_bgra = np.array(pil_image)
    overlay_bgra = cv2.cvtColor(overlay_bgra, cv2.COLOR_BGR2BGRA)

    return overlay_bgra


def process_video(video_path, output_folder, csv_path, interpret_params, text_params, alpha_vid_path = None):

    n = text_params.get('n', 1)
    low_threshold = interpret_params.get('low_threshold', 50)
    high_threshold = interpret_params.get('high_threshold', 150)
    blur_ksize = interpret_params.get('blur_ksize', 5)
    thresh_value = interpret_params.get('thresh_value', 127)
    d = interpret_params.get('d', 20)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    alpha = alpha_vid_path is not None
    if alpha:
        cap_alpha = cv2.VideoCapture(alpha_vid_path)
        if not cap_alpha.isOpened():
            print("Error opening alpha video.")
            return []

    # Check if the video was successfully opened
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    prev_frame = None
    frame_count = 0

    while True:
        ret, current_frame = cap.read()
        if alpha:
            ret_alpha, current_alpha = cap_alpha.read()

        if not ret:
            break

        # Process every nth frame
        if frame_count % n == 0:
            if prev_frame is not None:
                # Compute Canny edges difference
                difference = compute_canny_difference(prev_frame, current_frame, low_threshold, high_threshold)

                # Apply Gaussian blur and threshold to the difference
                thresholded = apply_blur_and_threshold(difference, blur_ksize, thresh_value)

                # Convert alpha to grayscale if it's provided
                if alpha and ret_alpha:
                    # Convert the alpha frame to grayscale (just take the first channel if it is already black & white in RGB format)
                    current_alpha_gray = cv2.cvtColor(current_alpha, cv2.COLOR_BGR2GRAY)
                    white_points = process_white_pixels(thresholded, d, current_alpha_gray)
                else:
                    white_points = process_white_pixels(thresholded, d)

                # Generate overlay with text
                overlay = visualize_points_with_text(current_frame, white_points, csv_path, text_params)
                output_image_path = os.path.join(output_folder, f"{frame_count:04d}.png")
                cv2.imwrite(output_image_path, overlay)

                # Update the previous frame
            prev_frame = current_frame

        frame_count += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()





def process_images(img1_path, img2_path, csv_path, low_threshold=50, high_threshold=150, blur_ksize=5,
                   thresh_value=127, d=20, deletion_factor=0.5, font_list=None, size_list=None, color_list=None,
                   char_limit=15):

    if font_list is None:
        font_list = [cv2.FONT_HERSHEY_SIMPLEX]
    if size_list is None:
        size_list = [0.3]
    if color_list is None:
        color_list = [(255, 255, 255)]

    # Read the images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("Error: Cannot open images.")
        return

    # Compute Canny edges difference
    difference = compute_canny_difference(img1, img2, low_threshold, high_threshold)

    # Apply Gaussian blur and threshold to the difference
    thresholded = apply_blur_and_threshold(difference, blur_ksize, thresh_value)

    # Process white pixels (black out area within radius `d`)
    white_points = process_white_pixels(thresholded, d)

    # Generate overlay with text
    overlay = visualize_points_with_text(img2, white_points, csv_path, deletion_factor, font_list, size_list, color_list, char_limit)

    # Blend the overlay with the original image
    blended_image = cv2.addWeighted(img2, 1, overlay, 0.3, 0)

    # Save the blended image
    cv2.imshow("imagen procesada", blended_image)
    cv2.waitKey(0)


print("librerias cargadas del chill")






#blobtracking tensa

interpret_tensa = {
    'n': 1,
    'low_threshold': 20,
    'high_threshold': 50,
    'blur_ksize': 9,
    'thresh_value': 150,
    'd': 70,
}

text_tensa = {
    'font_list': [r'C:\Users\simon\Desktop\DOCUMENTAL PERIFERIA CENTRO\Recursos\Orbitron-VariableFont_wght.ttf'],
    'size_list': [20],
    'color_list': [(255, 255, 255)],
    'char_limit': 12,
    'square_size_list': [3, 5, 10],
    'char_spacing': 8,
    'lines': 0.08,  # Draw 30% of possible lines
    'deletion_factor': 0.8  # Remove 20% of the points
}

csv_tensa = r"C:\Users\simon\Desktop\DOCUMENTAL PERIFERIA CENTRO\PythonProject\written_ddbbs\quepiensatensa.csv"  # Path to the CSV file containing text
video_tensa = r"C:\Users\simon\Desktop\DOCUMENTAL PERIFERIA CENTRO\PythonProject\Blob Tracking\Input_clips\blobtracking_tensa_color.mp4"
output_tensa = r"C:\Users\simon\Desktop\DOCUMENTAL PERIFERIA CENTRO\PythonProject\Blob Tracking\Output_clips\blobtracking_tensa_1"
alpha_vid_tensa = r"C:\Users\simon\Desktop\DOCUMENTAL PERIFERIA CENTRO\PythonProject\Blob Tracking\Input_clips\blobtracking_tensa_alpha.mp4"
process_video(video_tensa, output_tensa, csv_tensa, interpret_tensa, text_tensa, alpha_vid_tensa)