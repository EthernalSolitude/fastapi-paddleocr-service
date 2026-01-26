import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["PADDLE_NO_GPU"] = "1"

from paddleocr import PaddleOCR

print("Pre-downloading PaddleOCR models...")

ocr = PaddleOCR(lang='ru')
print("Models downloaded successfully!")
