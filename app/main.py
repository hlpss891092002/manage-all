from pytz import timezone
from datetime import  date
from fastapi import  Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import  HTTPException as StarletteHTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.controller import staticPage
from app.routers import add_router, staff_router, update_router, delete_router, search_router

from app.model.db.common_method import optimize_index, recreate_produce_record
from app.model.data_class.response_class import databaseException
# from app.model.data_class.validation_data_class import RequestValidationError

scheduler = AsyncIOScheduler(timezone=timezone("ROC"))

scheduler = AsyncIOScheduler(timezone=timezone("ROC"))

app= FastAPI()
app.include_router(staticPage.router)
app.include_router(add_router.router)
app.include_router(update_router.router)
app.include_router(delete_router.router)
app.include_router(staff_router.router)
app.include_router(search_router.router)

# app.add_middleware(LogRequestMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

now_day = date.today()

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


@scheduler.scheduled_job("interval", days = 1, start_date=f"{now_day} 23:00:00")
async def optimize_table():
	optimize_index()
	#recreate 功能尚未做完
	# recreate_produce_record()

	

