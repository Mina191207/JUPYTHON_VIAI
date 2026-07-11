from pydantic import BaseModel


class PlanResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: int
    credit: int
    duration_days: int

    class Config:
        from_attributes = True