from pydantic import BaseModel


class AddCreditRequest(BaseModel):
    amount: int
    reason: str


class CreditResponse(BaseModel):
    message: str
    balance: int
    transaction: int | None = None

class CreditBalanceResponse(BaseModel):
    credit_balance: int