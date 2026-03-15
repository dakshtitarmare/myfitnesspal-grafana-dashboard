from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import io
import os
import firebase_admin
from firebase_admin import credentials, db

from ..csv_parser import parse_myfitnesspal_csv, CSVValidationError  # existing CSV parsing logic

router = APIRouter(prefix="/upload", tags=["upload"])


# Initialize Firebase Admin SDK once
if not firebase_admin._apps:
    firebase_credentials_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    firebase_db_url = os.getenv("FIREBASE_DATABASE_URL")

    if not firebase_credentials_path or not firebase_db_url:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT_PATH and FIREBASE_DATABASE_URL must be set in the environment."
        )

    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred, {"databaseURL": firebase_db_url})


class UploadResponse(BaseModel):
    message: str
    entries_saved: int
    path: str


@router.post("/csv", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    user_id: Optional[str] = None,
):
    """Upload a MyFitnessPal CSV, parse it, and store entries in Firebase Realtime DB.

    Expects a Firebase-authenticated user id (uid) passed as `user_id` for now.
    In a production setup, you would verify a Firebase ID token and extract the uid.
    """
    if user_id is None:
        raise HTTPException(status_code=400, detail="user_id query parameter is required")

    if file.content_type not in ("text/csv", "application/vnd.ms-excel"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

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
