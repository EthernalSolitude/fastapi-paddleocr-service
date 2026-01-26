import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["PADDLE_NO_GPU"] = "1"
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_enable_pir_api"] = "0"

class Settings:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    FONT_PATH = os.path.join(BASE_DIR, "assets", "arial.ttf")
    
    # Параметры OCR
    OCR_LANG: str = "ru"
    DET_LIMIT_SIDE_LEN: int = 1280
    MIN_SCORE: float = 0.6  

settings = Settings()
