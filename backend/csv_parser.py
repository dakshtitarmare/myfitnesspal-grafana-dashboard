from __future__ import annotations

from io import BytesIO
import re

import pandas as pd

REQUIRED_COLUMNS = {"date", "meal", "food", "calories", "carbs", "protein", "fat"}
COLUMN_ALIASES = {
    "carbohydrates": "carbs",
    "carb": "carbs",
    "meal_type": "meal",
    "entry_date": "date",
    "item": "food",
}
NUMERIC_COLUMNS = ["calories", "carbs", "protein", "fat"]
TEXT_COLUMNS = ["meal", "food"]


class CSVValidationError(ValueError):
    pass


def normalize_column_name(name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower()).strip("_")
    return COLUMN_ALIASES.get(normalized, normalized)


def parse_myfitnesspal_csv(file_bytes: bytes) -> pd.DataFrame:
    if not file_bytes:
        raise CSVValidationError("The uploaded file is empty.")

    try:
        frame = pd.read_csv(BytesIO(file_bytes))
    except Exception as exc:
        raise CSVValidationError("The uploaded file could not be parsed as CSV.") from exc

    if frame.empty:
        raise CSVValidationError("The uploaded file does not contain any rows.")

    frame.columns = [normalize_column_name(column) for column in frame.columns]
    frame = frame.dropna(how="all")

    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise CSVValidationError(f"Missing required columns: {missing_list}.")

    frame = frame[["date", "meal", "food", "calories", "carbs", "protein", "fat"]].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.date

    for column in TEXT_COLUMNS:
        frame[column] = frame[column].fillna("").astype(str).str.strip()

    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)

    frame = frame.dropna(subset=["date"])
    frame = frame[frame["food"] != ""]
    frame.loc[frame["meal"] == "", "meal"] = "Unspecified"
    frame = frame.drop_duplicates(
        subset=["date", "meal", "food", "calories", "carbs", "protein", "fat"]
    )
    frame = frame.reset_index(drop=True)

    if frame.empty:
        raise CSVValidationError(
            "No valid food log rows remained after preprocessing. Check date and food columns."
        )

    return frame
