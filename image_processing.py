import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compare_images(original_path, altered_path, ssim_threshold=0.95, mse_threshold=50, mae_threshold=5, histogram_threshold=0.7):
    # Load the images
    original = cv2.imread(original_path)
    altered = cv2.imread(altered_path)

    # Check if images are loaded successfully
    if original is None or altered is None:
        raise ValueError("One of the images could not be loaded. Please check the file paths.")

    # Resize altered image to match original dimensions if necessary
    if original.shape != altered.shape:
        altered = cv2.resize(altered, (original.shape[1], original.shape[0]))

    # Convert images to grayscale for comparison
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    altered_gray = cv2.cvtColor(altered, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    ssim_score, _ = ssim(original_gray, altered_gray, full=True)

    # Compute Mean Squared Error (MSE)
    mse = np.mean((original_gray.astype("float") - altered_gray.astype("float")) ** 2)

    # Compute Mean Absolute Error (MAE)
    mae = np.mean(np.abs(original_gray.astype("float") - altered_gray.astype("float")))

    # Histogram Comparison
    hist_original = cv2.calcHist([original], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_altered = cv2.calcHist([altered], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    # Normalize the histograms
    hist_original = cv2.normalize(hist_original, hist_original).flatten()
    hist_altered = cv2.normalize(hist_altered, hist_altered).flatten()

    # Compare histograms using correlation
    histogram_correlation = cv2.compareHist(hist_original, hist_altered, cv2.HISTCMP_CORREL)

    # Debugging output
    print(f"SSIM Score: {ssim_score:.2f}, MSE: {mse:.2f}, MAE: {mae:.2f}, Histogram Correlation: {histogram_correlation:.2f}")

    # Determine if images are similar based on thresholds
    result = True  # Assume identical until proven otherwise

    if ssim_score < ssim_threshold:
        print("SSIM score indicates images are different.")
        result = False

    if mse > mse_threshold:
        print("MSE indicates images are different.")
        result = False

    if mae > mae_threshold:
        print("MAE indicates images are different.")
        result = False

    if histogram_correlation < histogram_threshold:
        print("Histogram correlation indicates images are different.")
        result = False

    if result:
        print("Images are identical.")
    else:
        print("Images are different.")

    return result  # Return the final result
