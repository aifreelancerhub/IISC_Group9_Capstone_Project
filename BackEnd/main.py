import uvicorn
from fastapi import FastAPI
from IISC_Group9_Capstone_Project.BackEnd.api.chat_router import router as chat_router

app = FastAPI()

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
