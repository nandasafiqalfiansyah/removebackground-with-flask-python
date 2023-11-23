from flask import jsonify, request
import cv2
import numpy as np
import base64

def extract_foreground(img, rect):
    # Initialize mask as a matrix of zeros with the same dimensions as the image
    mask = np.zeros(img.shape[:2], np.uint8)
    
    # Initialize background model and foreground model as matrices of zeros
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Run the GrabCut algorithm using models and the initialized area
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Generate a binary mask: 0 for background and 1 for foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Create an alpha channel with the binary mask
    alpha_channel = np.ones(mask.shape, dtype=img.dtype) * 255
    alpha_channel = alpha_channel * mask2[:, :]

    # Add the alpha channel to the original image
    img_with_removed_bg = cv2.merge((img, alpha_channel))

    return img_with_removed_bg

def process_image():
    try:
        # Check if 'image' is present in request files
        if 'image' not in request.files:
            return jsonify({'Created_by':'nanda_safiq_alfiansyah','status':'404','result': 'error', 'error_message': 'No file part'})

        # Read the image from the POST request
        image_file = request.files['image']
        image_np = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Extract foreground (modify this part based on your needs)
        rect = (50, 50, 400, 400)
        img_with_removed_bg = extract_foreground(image_np, rect)

        # Separate BGR channels
        b, g, r, a = cv2.split(img_with_removed_bg)

        # Calculate the mean for each channel
        mean_r = np.mean(r)
        mean_g = np.mean(g)
        mean_b = np.mean(b)

        # Compile RGB values as numbers
        rgb_values = {'R': mean_r, 'G': mean_g, 'B': mean_b}

        # Encode both the original image and the image with removed background to base64
        _, img_encoded_original = cv2.imencode('.png', image_np)
        img_base64_original = base64.b64encode(img_encoded_original).decode('utf-8')

        _, img_encoded_removed_bg = cv2.imencode('.png', img_with_removed_bg)
        img_base64_removed_bg = base64.b64encode(img_encoded_removed_bg).decode('utf-8')

        return jsonify({
            'result': 'success',
            'rgb_values': rgb_values,
            'original_image': img_base64_original,
            'image_with_removed_bg': img_base64_removed_bg
        })

    except Exception as e:
        return jsonify({'result': 'error', 'error_message': str(e)})
