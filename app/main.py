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
from app.model.db.common_method import recreate_produce_record, set_key_on_produce_record_created, set_indexed_on_produce_record_created



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
        print("recreate start")
        recreate_produce_record()
        set_key_on_produce_record_created()
        set_indexed_on_produce_record_created()
        print("recreate end")

	



	

