class ResponseBody:
    @staticmethod
    def success(data=None, message: str = "Success"):
        return {
            "success": True,
            "data": data,
            "message": message
        }

    @staticmethod
    def failed(data=None, message: str = "Failed"):
        return {
            "success": False,
            "data": data,
            "message": message
        }

    @staticmethod
    def error(status_code: int, message: str):
        return {
            "success": False,
            "message": message,
            "status_code": status_code
        }
