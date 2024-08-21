import cv2
import librosa
from moviepy.editor import VideoFileClip

class VideoAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.clip = VideoFileClip(video_path)

        if not self.cap.isOpened():
            raise ValueError("Video cannot be opened. Check the path.")

    # def extract_text_from_frame(self, frame):
    #     # Tesseract OCR ile metni çıkarın
    #     text = pytesseract.image_to_string(frame)
    #     return text.strip()

    # def analyze_frame(self, frame):
    #     """
    #     Bir karedeki metni bul ve döndür.
    #     """
    #     return self.extract_text_from_frame(frame)

    # def analyze_video_texts(self):
    #     """
    #     Video boyunca her karedeki metinleri analiz eder.
    #     """
    #     texts = {}
    #     frame_count = 0
    #     fps = self.cap.get(cv2.CAP_PROP_FPS)

    #     while self.cap.isOpened():
    #         ret, frame = self.cap.read()
    #         if not ret:
    #             break

    #         text = self.analyze_frame(frame)
    #         if text:
    #             second = frame_count / fps
    #             texts[second] = text

    #         frame_count += 1

    #     self.cap.release()
    #     return texts

    def analyze_audio(self):
        """
        Videodan sesi çıkar ve boşlukları veya gereksiz sesleri analiz et.
        """
        audio_path = "temp_audio.wav"
        self.clip.audio.write_audiofile(audio_path)

        y, sr = librosa.load(audio_path)
        non_silent_intervals = librosa.effects.split(y, top_db=30)

        silent_intervals = []
        for i in range(len(non_silent_intervals) - 1):
            start = non_silent_intervals[i][1] / sr
            end = non_silent_intervals[i + 1][0] / sr
            silent_intervals.append((start, end))

        return silent_intervals

    def get_video_info(self):
        """
        Video hakkında temel bilgileri döndürür.
        """
        return {
            "duration": self.clip.duration,
            "fps": self.clip.fps,
            "size": self.clip.size,
        }

    def analyze_video(self):
        """
        Video ve ses analizlerini gerçekleştirir ve sonuçları döndürür.
        """
        # Video bilgilerini almak
        video_info = self.get_video_info()

        # Video üzerindeki metinleri analiz etmek
        # texts = self.analyze_video_texts()

        # Ses analizini yapmak
        silent_intervals = self.analyze_audio()

        # Sonuçları bir sözlük olarak döndürmek
        return {
            "video_info": video_info,
            # "detected_texts": texts,
            "silent_intervals": silent_intervals,
        }

if __name__ == "__main__":
    # Kullanım örneği
    video_path = "path_to_your_video.mp4"  # Video dosyanızın yolunu buraya girin
    analyzer = VideoAnalyzer(video_path)
    result = analyzer.analyze_video()

    # Sonuçları yazdırma
    print(f"Video Info: {result['video_info']}")
    print("Detected Texts with Timestamps:")
    for second, text in result['detected_texts'].items():
        print(f"{second:.2f}s: {text}")

    print("Silent Intervals (start, end):")
    for start, end in result['silent_intervals']:
        print(f"{start:.2f}s - {end:.2f}s")
