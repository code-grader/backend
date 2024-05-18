from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any, Dict


def build_response(
    *, message: str, data: Dict[str, Any] = {}, success: bool = True
) -> Dict[str, Any]:
    return {
        "success": success,
        "message": message,
        "data": data,
    }


def create_response(
    *,
    message: str,
    data: Dict[str, Any] = {},
    success: bool = True,
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    return JSONResponse(
        content=build_response(message=message, data=data, success=success),
        status_code=status_code,
        headers={
            "content-type": "application/json",
        },
    )
