import hashlib
import hmac
from datetime import datetime
from urllib.parse import urlencode

from app.config.config import (
    VNP_TMN_CODE,
    VNP_HASH_SECRET,
    VNP_RETURN_URL,
    VNP_URL,
)


def hmac_sha512(key: str, data: str):
    return hmac.new(
        key.encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha512,
    ).hexdigest()


def create_payment_url(payment, ip_addr: str): 
    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": VNP_TMN_CODE,
        "vnp_Amount": payment.amount * 100,  # VNPay yêu cầu nhân 100
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
        "vnp_CurrCode": "VND",
        "vnp_IpAddr": ip_addr,
        "vnp_Locale": "vn",
        "vnp_OrderInfo": f"Thanh toan don hang {payment.id}",
        "vnp_OrderType": "other",
        "vnp_ReturnUrl": VNP_RETURN_URL,
        "vnp_TxnRef": str(payment.id),
    }

    sorted_params = dict(sorted(params.items()))

    query = urlencode(sorted_params)

    secure_hash = hmac_sha512(
        VNP_HASH_SECRET,
        query,
    )

    return f"{VNP_URL}?{query}&vnp_SecureHash={secure_hash}"

def verify_secure_hash(params: dict) -> bool:
    received_hash = params.pop("vnp_SecureHash", None)
    params.pop("vnp_SecureHashType", None)

    sorted_params = dict(sorted(params.items()))

    query = urlencode(sorted_params)

    calculated_hash = hmac_sha512(
        VNP_HASH_SECRET,
        query,
    )

    return calculated_hash == received_hash