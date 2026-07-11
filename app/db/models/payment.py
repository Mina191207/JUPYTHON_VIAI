from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from app.db.database import Base
from app.constants.payment import (
    PaymentStatus,
    PaymentType,
)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    plan_id = Column(
        Integer,
        ForeignKey("plans.id"),
        nullable=True,
    )

    payment_method_id = Column(
        Integer,
        ForeignKey("payment_methods.id"),
        nullable=False,
    )

    # CREDIT | SUBSCRIPTION
    payment_type = Column(
        String(30),
        nullable=False,
    )

    # Số tiền thanh toán (VND)
    amount = Column(
        Integer,
        nullable=False,
    )

    # Credit cộng thêm (chỉ dùng khi nạp credit)
    credit_added = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # PENDING | SUCCESS | FAILED
    status = Column(
        String(30),
        default=PaymentStatus.PENDING.value,
        nullable=False,
    )

    # Mã giao dịch từ cổng thanh toán
    transaction_id = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )