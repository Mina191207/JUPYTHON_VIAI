from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.controllers.v1.base import new_router
from app.db.database import get_db
from app.db.models.payment import Payment
from app.services.v1.vnpay_service import verify_secure_hash

from app.constants.payment import PaymentStatus
from app.constants.payment import PaymentType

from app.services.v1.credit_service import credit_service
from app.services.v1.payment_service import payment_service
# from app.services.v1.subscription_service import subscription_service
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="", tags=["Payment"])

@router.get("/vnpay/return")
def vnpay_return(
    request: Request,
    db: Session = Depends(get_db),
):
    print("===== VNPAY RETURN =====")
    params = dict(request.query_params)

    print("=" * 50)
    print(params)
    print("=" * 50)

    # Kiểm tra chữ ký
    if not verify_secure_hash(params.copy()):
        raise HTTPException(
            status_code=400,
            detail="Invalid signature",
        )


    # Lấy payment
    payment_id = int(params["vnp_TxnRef"])

    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )
    response_code = params["vnp_ResponseCode"]

    vnp_amount = int(params["vnp_Amount"])

    if vnp_amount != payment.amount * 100:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment amount",
        )

    if response_code != "00":
        payment.status = PaymentStatus.FAILED.value
        db.commit()
        return {
            "message": "Payment failed",
            "response_code": response_code,
        }
    # Nếu đã xử lý rồi thì không xử lý nữa
    if payment.status == PaymentStatus.SUCCESS.value:
        return {
            "message": "Payment already completed"
        }
    
    transaction_no = params.get("vnp_TransactionNo")

    if transaction_no and transaction_no != "0":
        payment.transaction_id = transaction_no

    db.commit()
    
    payment_service.complete_payment(
        db=db,
        payment_id=payment.id,
        user_id=payment.user_id,
    )
    return RedirectResponse(
        url=f"http://localhost:3000/billing",
        status_code=302,
    )
