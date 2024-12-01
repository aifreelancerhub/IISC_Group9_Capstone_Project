from fastapi import HTTPException, File, UploadFile,APIRouter
import openai

from fastapi.responses import JSONResponse
import os 
# Configure OpenAI API Key
openai.api_key = "your_api_key"
router = APIRouter()

@router.post("/transcribe/")

async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Create a temporary file to save the uploaded audio
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())
        
        # Use OpenAI's Whisper to transcribe the audio
        with open(file.filename, "rb") as audio_file:
            transcription = openai.Audio.transcribe("whisper-1", audio_file,language="en")
        
        # Remove the temporary file
        os.remove(file.filename)
        
        # Return the transcribed text
        return JSONResponse(content={
            "transcription": transcription.text,
            "status": "success"
        })
    
    except Exception as e:
        # Remove the temporary file in case of an error
        if os.path.exists(file.filename):
            os.remove(file.filename)
        
        # Return an error response
        raise HTTPException(status_code=500, detail=str(e))