from fastapi import FastAPI
import uvicorn


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.app.hotels import router as hotel_router
from src.config import settings


print(f"settings.DB_NAME={settings.DB_NAME}")


app = FastAPI()


@app.get("/")
def func():
    return {"message": "Wellcome to the HOTELS!"}


app.include_router(hotel_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)