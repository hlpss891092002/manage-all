import logging
from fastapi import  Request, FastAPI, HTTPException, WebSocketException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import  HTTPException as StarletteHTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.routers import add_router, staff_router, update_router, delete_router, search_router
from app.MODEL.DB_method.common_method import optimize_index
from app.MODEL.data_class.response_class import databaseException
# from app.MODEL.data_class.validation_data_class import RequestValidationError

app= FastAPI()
app.include_router(add_router.router)
app.include_router(update_router.router)
app.include_router(delete_router.router)
app.include_router(staff_router.router)
app.include_router(search_router.router)
# app.add_middleware(LogRequestMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")



@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
		return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": f"type: {exc.detail}",
						
        }
		)

# "request validation set"
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
				content=jsonable_encoder({
					"error": True,
                    "message": f"type: {exc.errors()[0]['msg']}",
						"location": {exc.errors()[0]['loc']}
						}),
    )



@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("app/static/HTML/sign_in.html", media_type="text/html")

@app.get("/staffIndex", include_in_schema=False)
async def staff(request: Request):
	return FileResponse("app/static/HTML/staffIndex.html", media_type="text/html")

@app.get("/add", include_in_schema=False)
async def insertPage(request: Request):
	return FileResponse("app/static/HTML/add.html", media_type="text/html")

@app.get("/search", include_in_schema=False)
async def insertPage(request: Request):
	return FileResponse("app/static/HTML/search.html", media_type="text/html")


def main():
	def optimize_midnight():
		optimize_index()
		print("optimize complete")
	def optimize_midday():
		optimize_index()
		print("optimize complete")

	schedular = BackgroundScheduler()
	trigger_mn =  CronTrigger(hour = 23, minute = 59)
	trigger_md =  CronTrigger(hour = 12, minute = 30)
	schedular.add_job(optimize_midnight, trigger_mn)
	schedular.add_job(optimize_midday, trigger_md)
	print("optimize")
	schedular.start()


main()