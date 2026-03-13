from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ..csv_parser import CSVValidationError, parse_myfitnesspal_csv
from ..database import get_db
from ..models import FoodLog

router = APIRouter(tags=["uploads"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a valid .csv file.")

    file_bytes = await file.read()

    try:
        frame = parse_myfitnesspal_csv(file_bytes)
    except CSVValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    records = [
        FoodLog(
            date=row.date,
            meal=row.meal,
            food=row.food,
            calories=float(row.calories),
            carbs=float(row.carbs),
            protein=float(row.protein),
            fat=float(row.fat),
        )
        for row in frame.itertuples(index=False)
    ]

    db.add_all(records)
    db.commit()

    return {
        "message": "Upload processed successfully.",
        "recordsInserted": len(records),
    }
