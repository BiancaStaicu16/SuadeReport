from fastapi import FastAPI, HTTPException
from utils import validate_date, construct_report
from typing import Optional
from starlette import status

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_report/")
async def get_report(date: Optional[str] = None):
    if date and validate_date(date):
        return construct_report(date)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid date format",
                "message": "Date is in the wrong format, please retry with YYYY-MM-DD.",
                "example": "2023-01-31",
            },
        )
