from fastapi import HTTPException, Request, Response
from clerk_backend_api import Clerk, AuthenticateRequestOptions, RequestState
from pydantic import BaseModel
import os

clerk_sdk: Clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def authenticate_and_get_user_details(request: Request | BaseModel):
    """
    authenticate_and_get_user_details
    :param request:
    :return:
    """
    try:
        request_state: RequestState = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173"],  # Replace with your frontend URL
                jwt_key=os.getenv("CLERK_JWT_KEY"),  # Replace with your JWT key
            )
        )
        if not request_state.is_authenticated:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )
        user_id = request_state.payload.get("sub")
        return {
            "user_id": user_id,  # Replace with your user ID
            "user_name": request_state.payload.get("name"),  # Replace with your username
            "user_image": request_state.payload.get("picture"),  # Replace with your user image
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )