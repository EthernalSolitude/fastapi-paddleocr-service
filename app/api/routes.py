import os
import io
import fitz  
import numpy as np
import uuid
from PIL import Image
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Request

from app.services.ocr import ocr_engine
from app.services.visualizer import create_side_by_side_image, append_image_to_pdf

router = APIRouter()

RESULTS_DIR = "static/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

@router.post("/process_link", summary="OCR документа")
async def process_document_link(
    request: Request,
    file: UploadFile = File(...)
):
    original_filename = file.filename
    name_without_ext, ext = os.path.splitext(original_filename)
    file_ext = ext.lower()
    
    if file_ext not in [".pdf", ".jpg", ".jpeg", ".png", ".bmp"]:
        raise HTTPException(status_code=400, detail="Формат файла не поддерживается")

    content = await file.read()
    output_pdf = fitz.open()
    
    try:
        tasks = []
        if file_ext == ".pdf":
            with fitz.open(stream=content, filetype="pdf") as doc:
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    mat = fitz.Matrix(2, 2)
                    pix = page.get_pixmap(matrix=mat)
                    img_pil = Image.open(io.BytesIO(pix.tobytes("ppm"))).convert('RGB')
                    tasks.append(np.array(img_pil))
        else:
            img_pil = Image.open(io.BytesIO(content)).convert('RGB')
            tasks.append(np.array(img_pil))

        for img_np in tasks:
            boxes, texts, scores = ocr_engine.predict(img_np)
            result_img = create_side_by_side_image(img_np, boxes, texts, scores)
            append_image_to_pdf(output_pdf, result_img)
            del img_np, result_img

        unique_name = f"RESULT_{uuid.uuid4().hex[:8]}_{name_without_ext}.pdf"
        output_path = os.path.join(RESULTS_DIR, unique_name)
        
        if len(output_pdf) > 0:
            output_pdf.save(output_path)
        else:
            output_pdf.new_page()
            output_pdf.save(output_path)
            
        output_pdf.close()
        
        #Формируем ссылку для скачивания
        download_url = f"{request.base_url}static/results/{unique_name}"
        
        #Возвращаем JSON
        return {
            "status": "success",
            "message": "File processed successfully",
            "filename": unique_name,
            "download_url": download_url
        }

    except Exception as e:
        output_pdf.close()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
