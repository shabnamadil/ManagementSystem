import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import imagehash
from PIL import Image
import requests
from io import BytesIO

class MediaComparator:
    def compare_images(self, original_image_path, uploaded_image_url):
        # Load original image from local file
        original_img = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)

        # Load uploaded image from URL
        response = requests.get(uploaded_image_url)
        uploaded_img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_GRAYSCALE)

        # Ensure both images were loaded successfully
        if original_img is None or uploaded_img is None:
            return {
                'result_message': "Error loading images",
                'is_similar': False
            }

        # Resize uploaded image to match original dimensions
        dim = (original_img.shape[1], original_img.shape[0])
        uploaded_img_resized = cv2.resize(uploaded_img, dim)

        # Calculate histogram similarity
        hist1 = cv2.calcHist([original_img], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([uploaded_img_resized], [0], None, [256], [0, 256])
        hist_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

        # Calculate SSIM
        ssim_value = ssim(original_img, uploaded_img_resized)

        # Calculate perceptual hash difference
        hash1 = imagehash.average_hash(Image.open(original_image_path))
        hash2 = imagehash.average_hash(Image.fromarray(uploaded_img_resized)) 
        hash_difference = hash1 - hash2

        # Set thresholds for comparison
        hist_threshold = 0.9
        ssim_threshold = 0.9
        hash_threshold = 5

        # Determine similarity based on thresholds
        if hist_similarity > hist_threshold and ssim_value > ssim_threshold and hash_difference < hash_threshold:
            result_message = "Images are similar."
            is_similar = True
        else:
            result_message = "Images are not similar."
            is_similar = False

        return {
            'hist_similarity': hist_similarity,
            'ssim_value': ssim_value,
            'hash_difference': hash_difference,
            'result_message': result_message,
            'is_similar': is_similar
        }

    def compare_videos(self, original_video_path, uploaded_video_url):
        # Load original video from local file
        original_cap = cv2.VideoCapture(original_video_path)

        # Load uploaded video from URL
        response = requests.get(uploaded_video_url, stream=True) 
        uploaded_cap = cv2.VideoCapture(response.raw) 

        # Ensure both videos were loaded successfully
        if not original_cap.isOpened() or not uploaded_cap.isOpened():
            return {
                'result_message': "Error loading videos",
                'is_similar': False
            }

        original_fps = original_cap.get(cv2.CAP_PROP_FPS)
        uploaded_fps = uploaded_cap.get(cv2.CAP_PROP_FPS)

        hist_threshold = 0.5
        ssim_threshold = 0.5

        frame_count = 0
        hist_similarities = []
        ssim_values = []

        while True:
            original_ret, original_frame = original_cap.read()
            uploaded_ret, uploaded_frame = uploaded_cap.read()

            if not original_ret or not uploaded_ret:
                break

            if frame_count % int(original_fps) == 0:
                original_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_frame, cv2.COLOR_BGR2GRAY)

                dim = (original_gray.shape[1], original_gray.shape[0])
                uploaded_gray_resized = cv2.resize(uploaded_gray, dim)

                hist1 = cv2.calcHist([original_gray], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([uploaded_gray_resized], [0], None, [256], [0, 256])
                hist_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                hist_similarities.append(hist_similarity)

                ssim_value = ssim(original_gray, uploaded_gray_resized)
                ssim_values.append(ssim_value)

            frame_count += 1

        original_cap.release()
        uploaded_cap.release()

        avg_hist_similarity = np.mean(hist_similarities)
        avg_ssim_value = np.mean(ssim_values)

        hist_below_threshold = sum(1 for h in hist_similarities if h < hist_threshold)
        ssim_below_threshold = sum(1 for s in ssim_values if s < ssim_threshold)

        if avg_hist_similarity > hist_threshold and avg_ssim_value > ssim_threshold:
            result_message = "Videolar büyük ölçüde benzer."
            is_similar = True
            difference_details = ""
        else:
            result_message = "Videolar benzer değil."
            is_similar = False
            difference_details = (
                f"Histogram benzerlik değeri {hist_below_threshold} karede eşik değerinin altında ({hist_threshold}). "
                f"SSIM değeri {ssim_below_threshold} karede eşik değerinin altında ({ssim_threshold})."
            )

        return {
            'avg_hist_similarity': avg_hist_similarity,
            'avg_ssim_value': avg_ssim_value,
            'hist_below_threshold': hist_below_threshold,
            'ssim_below_threshold': ssim_below_threshold,
            'result_message': result_message,
            'is_similar': is_similar,
            'difference_details': difference_details
        }