from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
