from fastapi import APIRouter, Request
from fastapi.responses import FileResponse


router = APIRouter()

@router.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("app/static/HTML/sign_in.html", media_type="text/html")

@router.get("/staffIndex", include_in_schema=False)
async def staff(request: Request):
	return FileResponse("app/static/HTML/staffIndex.html", media_type="text/html")

@router.get("/add", include_in_schema=False)
async def insertPage(request: Request):
	return FileResponse("app/static/HTML/add.html", media_type="text/html")

@router.get("/search", include_in_schema=False)
async def insertPage(request: Request):
	return FileResponse("app/static/HTML/search.html", media_type="text/html")

