from fastapi import APIRouter, Request

router = APIRouter()


@router.get(
    "/ping",
    tags=["Health Check"],
    description="Health check endpoint to verify if the server is running.",
    response_description="pong",
)
def ping(request: Request) -> str:
    return "pong"
