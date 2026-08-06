from datetime import datetime

from pydantic import BaseModel


class CurrentSubscriptionResponse(BaseModel):

    plan_id: int
    plan_name: str

    status: str

    start_date: datetime
    renewal_date: datetime | None
    end_date: datetime

    credit_balance: int

    class Config:
        from_attributes = True