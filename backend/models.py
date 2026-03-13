from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class FoodLog(Base):
    __tablename__ = "food_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    meal: Mapped[str] = mapped_column(String(100), nullable=False, default="Unspecified")
    food: Mapped[str] = mapped_column(String(255), nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    carbs: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    protein: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    fat: Mapped[float] = mapped_column(Float, nullable=False, default=0)
