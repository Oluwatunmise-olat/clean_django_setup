import json

from rest_framework.response import Response


class ResponseFormatter:
    def api_response(
        self,
        status_code: int,
        has_error: bool,
        message: str = "",
        data: dict = {},
        error_code=None,
    ):

        if has_error:
            if not error_code:
                raise ValueError("'error_code' field is required")

            response_data = self.__failure(error_code)
            response_data["data"] = data

            return Response(response_data, status=status_code)

        if not message:
            raise ValueError("'message' field is required")

        response_data = self.__success()
        response_data.setdefault("message", message)
        response_data.setdefault("data", data)

        return Response(response_data, status=status_code)

    def __success(self):
        return {"success": True}

    def __failure(self, error_code: int):

        message = self.__read_error_data().get(f"{error_code}", None)

        if not message:
            raise ValueError("Invalid Error Code")

        return {"success": False, "message": message, "error_code": error_code}

    def __read_error_data(self):
        with open("./error_codes.json") as error_data:
            return json.load(error_data)

    def push_notification_response(self):
        pass


ResponseInstance = ResponseFormatter()
