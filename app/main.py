import logging
from fastapi import  Request, FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import create_router, Read_router, staff_router, update_router, delete_router, search_router
from app.MODEL.data_class.validation_data_class import RequestValidationError

app= FastAPI()
app.include_router(create_router.router)
app.include_router(Read_router.router)
app.include_router(update_router.router)
app.include_router(delete_router.router)
app.include_router(staff_router.router)
app.include_router(search_router.router)
# app.add_middleware(LogRequestMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("app/static/HTML/sign_in.html", media_type="text/html")

@app.get("/staffIndex", include_in_schema=False)
async def staff(request: Request):
	return FileResponse("app/static/HTML/staffIndex.html", media_type="text/html")

@app.get("/insert", include_in_schema=False)
async def insertPage(request: Request):
	return FileResponse("app/static/HTML/insert.html", media_type="text/html")

@app.get("/search", include_in_schema=False)
async def insertPage(request: Request):
	return FileResponse("app/static/HTML/search.html", media_type="text/html")

"request validation set"
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=400,
# 				content=jsonable_encoder({
# 					"error": True,
# 					"message": f"type: {exc.errors()[0]['msg']}, loction: {exc.errors()[0]['loc']}"}),
#     )

"exception validation set"
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
# 		print(f"OMG! An HTTP error!: {repr(exc)}")
# 		return await http_exception_handler(request, exc)
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "error": True,
#             "message": str(exc.detail)
#         }
# 			