from rest_framework.response import Response


class APIResponse(Response):

    def __init__(
        self, data=None, message="", success=True, status_code=200, errors=None
    ):
        formatted_response = {
            "success": success,
            "message": message,
            "errors": errors or {"code": None, "message": None, "errors": []},
            "data": data or {},
        }
        super().__init__(data=formatted_response, status=status_code)

