import numpy as np
from paddleocr import PaddleOCR
from app.core.config import settings
import logging

logging.getLogger("ppocr").setLevel(logging.ERROR)

class OCREngine:
    def __init__(self):
        print("Загрузка модели PaddleOCR... Подождите...")
        self.ocr = PaddleOCR(
            lang=settings.OCR_LANG,
            use_textline_orientation=True,
            enable_mkldnn=False,
            ocr_version='PP-OCRv3',
            det_limit_side_len=settings.DET_LIMIT_SIDE_LEN,
            det_db_thresh=0.2,
            det_db_box_thresh=0.5,
            det_db_unclip_ratio=1.6
        )
        print("Модель PaddleOCR готова к работе!")

    def predict(self, img_np: np.ndarray):
        results = self.ocr.predict(img_np)
        
        if not results or results[0] is None:
            return [], [], []
            
        res = results[0]
        # Универсальный парсинг
        boxes = res.get('dt_polys', []) if isinstance(res, dict) else getattr(res, 'dt_polys', [])
        texts = res.get('rec_texts', []) if isinstance(res, dict) else getattr(res, 'rec_texts', [])
        scores = res.get('rec_scores', []) if isinstance(res, dict) else getattr(res, 'rec_scores', [])
        
        return boxes, texts, scores

# Singleton
ocr_engine = OCREngine()
