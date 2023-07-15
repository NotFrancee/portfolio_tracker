class MissingRequiredParams(Exception):
    """Error when some params are missings"""

    def __init__(self, required_params: set, given_params: set) -> None:
        missing_params = required_params.difference(given_params)
        error_msg = ["you did not provide some required params: "]
        error_msg += missing_params

        s = " ".join(error_msg)

        super().__init__(s)
