def format_response(success: bool, message: str = "", data=None, code: int = 200):
    if data is None:
        data = {}
    return {
        "success": success,
        "message": message,
        "data": data
    }, code


