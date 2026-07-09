from pydantic import BaseModel


class AddCreditRequest(BaseModel):
    amount: int
    reason: str


class CreditResponse(BaseModel):
    balance: int