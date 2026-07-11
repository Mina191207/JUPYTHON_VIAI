from enum import Enum


class PaymentType(str, Enum):
    CREDIT = "CREDIT"
    SUBSCRIPTION = "SUBSCRIPTION"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"