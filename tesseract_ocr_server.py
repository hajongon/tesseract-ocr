from fastapi import FastAPI, File, UploadFile, HTTPException
import pytesseract
from PIL import Image
import io
import os

# FastAPI 애플리케이션 초기화
app = FastAPI()

# Tesseract 설치 경로 설정 (OS에 따라 다를 수 있음)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# 이미지에서 텍스트 추출하는 엔드포인트
@app.post('/ocr')
async def ocr_image(image: UploadFile = File(...)):
    try:
        # 파일 검사
        if not image.filename:
            raise HTTPException(status_code=400, detail='No selected file')

        # 이미지를 PIL 형식으로 열기
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data))

        # Tesseract로 OCR 수행
        extracted_text = pytesseract.image_to_string(pil_image, lang="kor")

        # 추출된 텍스트를 JSON 형식으로 반환
        return {'extracted_text': extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 가상환경 설정 확인
venv_path = os.getenv('VIRTUAL_ENV')
if venv_path:
    print(f'Virtual environment detected: {venv_path}')
else:
    print('No virtual environment detected. Please activate a virtual environment before running the server.')

# 서버 실행
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level='debug')