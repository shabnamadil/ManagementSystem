import cv2
# import easyocr

class ImageAnalyzer:
    def __init__(self, image_path):
        """
        Initializes the image analyzer.

        Args:
            image_path (str): The file path of the image to be analyzed.
        """
        self.image_path = image_path
        self.image = cv2.imread(image_path)

        if self.image is None:
            raise ValueError("Image could not be opened. Check the file path.")

    def get_image_info(self):
        """
        Returns basic information about the image.

        Returns:
            dict: A dictionary containing information such as the image's dimensions,
                  number of color channels, and data type.
        """
        height, width, channels = self.image.shape
        data_type = self.image.dtype

        return {
            "height": height,
            "width": width,
            "channels": channels,
            "data_type": data_type,
        }

    def convert_to_grayscale(self):
        """
        Converts the image to grayscale.

        Returns:
            numpy.ndarray: The grayscale image.
        """
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def resize_image(self, new_width, new_height):
        """
        Resizes the image.

        Args:
            new_width (int): The new width.
            new_height (int): The new height.

        Returns:
            numpy.ndarray: The resized image.
        """
        return cv2.resize(self.image, (new_width, new_height))

    def detect_edges(self):
        """
        Detects edges in the image.

        Returns:
            numpy.ndarray: The image with edges highlighted.
        """
        gray_image = self.convert_to_grayscale()
        return cv2.Canny(gray_image, 100, 200)

    def extract_text_from_image(self, languages=['en']):  # Default to English
        """
        Extracts text from the image.

        Args:
            languages (list): A list of languages to use for text extraction.

        Returns:
            list: A list containing detected text and their bounding boxes.
        """
        # reader = easyocr.Reader(languages)
        # results = reader.readtext(self.image)
        results = ["test", "yazi"]
        return results

if __name__ == "__main__":
    # Example usage
    image_path = "your_image.jpg"  # Replace with your image file path
    analyzer = ImageAnalyzer(image_path)

    # Get image information
    image_info = analyzer.get_image_info()
    print(f"Image Information: {image_info}")

    # Convert to grayscale
    gray_image = analyzer.convert_to_grayscale()
    cv2.imshow("Grayscale Image", gray_image)
    cv2.waitKey(0)

    # Resize the image
    resized_image = analyzer.resize_image(300, 200)
    cv2.imshow("Resized Image", resized_image)
    cv2.waitKey(0)

    # Detect edges
    edge_image = analyzer.detect_edges()
    cv2.imshow("Edges", edge_image)
    cv2.waitKey(0)

    # Extract text (default to English)
    extracted_text = analyzer.extract_text_from_image()
    print("Extracted Text:")
    for detection in extracted_text:
        print(detection[1])  # Print only the detected text

    # Extract Turkish text
    extracted_turkish_text = analyzer.extract_text_from_image(languages=['tr'])
    print("\nExtracted Turkish Text:")
    for detection in extracted_turkish_text:
        print(detection[1])

    cv2.destroyAllWindows()
