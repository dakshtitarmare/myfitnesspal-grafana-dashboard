from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import io
import os
import firebase_admin
from firebase_admin import credentials, db

from ..csv_parser import CSVValidationError, parse_myfitnesspal_csv
from ..database import get_db
from ..models import FoodLog

router = APIRouter(tags=["uploads"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a valid .csv file.")

    try:
        contents = await file.read()
        try:
            df = parse_myfitnesspal_csv(contents)
        except CSVValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

        parsed_entries = df.to_dict(orient="records")
        if not parsed_entries:
            raise HTTPException(status_code=400, detail="No valid entries found in CSV file.")

        # Save to Firebase under /users/{uid}/entries
        ref = db.reference(f"/users/{user_id}/entries")

        # We can push entries in bulk by setting a dict with generated keys
        updates = {}
        for entry in parsed_entries:
            new_key = ref.push().key
            updates[new_key] = entry

        ref.update(updates)

        return UploadResponse(
            message="CSV uploaded and processed successfully.",
            entries_saved=len(parsed_entries),
            path=f"/users/{user_id}/entries",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {e}")
