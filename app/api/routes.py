import os
import io
import fitz
import numpy as np
import tempfile
from PIL import Image
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from app.services.ocr import ocr_engine
from app.services.visualizer import create_side_by_side_image, append_image_to_pdf

router = APIRouter()

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

@router.post("/process", summary="OCR документа")
async def process_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # Проверка расширения
    filename = file.filename
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in [".pdf", ".jpg", ".jpeg", ".png", ".bmp"]:
        raise HTTPException(status_code=400, detail="Формат не поддерживается")

    content = await file.read()
    
    output_pdf = fitz.open()
    
    try:
        tasks = [] 

        if file_ext == ".pdf":
            # Читаем PDF из байтов
            with fitz.open(stream=content, filetype="pdf") as doc:
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    mat = fitz.Matrix(2, 2)
                    pix = page.get_pixmap(matrix=mat)
                    img_pil = Image.open(io.BytesIO(pix.tobytes("ppm"))).convert('RGB')
                    tasks.append(np.array(img_pil))
                    
        else: # Картинка
            img_pil = Image.open(io.BytesIO(content)).convert('RGB')
            tasks.append(np.array(img_pil))

        for idx, img_np in enumerate(tasks):
            print(f"Обработка страницы {idx + 1}/{len(tasks)}...")
            
            boxes, texts, scores = ocr_engine.predict(img_np)
            
            result_img = create_side_by_side_image(img_np, boxes, texts, scores)
            
            append_image_to_pdf(output_pdf, result_img)
            
            del img_np
            del result_img

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            output_path = tmp.name
        
        if len(output_pdf) > 0:
            output_pdf.save(output_path)
        else:
            output_pdf.new_page() 
            output_pdf.save(output_path)
            
        output_pdf.close()
        
        # Отдаем файл и ставим задачу на удаление
        background_tasks.add_task(cleanup_file, output_path)
        
        return FileResponse(
            output_path, 
            media_type="application/pdf", 
            filename=f"RESULT_{filename}.pdf"
        )

    except Exception as e:
        print(f"Ошибка: {e}")
        output_pdf.close()
        raise HTTPException(status_code=500, detail=str(e))
