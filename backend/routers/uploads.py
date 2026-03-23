from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..csv_parser import CSVValidationError, parse_myfitnesspal_csv
from ..database import get_db
from ..models import FoodLog

router = APIRouter(tags=["uploads"])


class UploadResponse(BaseModel):
    message: str
    recordsInserted: int


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a valid .csv file.")

    try:
        contents = await file.read()
        frame = parse_myfitnesspal_csv(contents)

        records: List[FoodLog] = [
            FoodLog(
                date=row["date"],
                meal=row["meal"],
                food=row["food"],
                calories=float(row["calories"]),
                carbs=float(row["carbs"]),
                protein=float(row["protein"]),
                fat=float(row["fat"]),
            )
            for row in frame.to_dict(orient="records")
        ]

        if not records:
            raise HTTPException(status_code=400, detail="No valid entries found in CSV file.")

        db.add_all(records)
        db.commit()

        return UploadResponse(
            message="CSV uploaded and processed successfully.",
            recordsInserted=len(records),
        )
    except CSVValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {exc}") from exc
