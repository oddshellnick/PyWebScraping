class BadUserAgent(Exception):
    """
    Custom exception raised when the user agent is invalid.

    :Usage:
        raise BadUserAgent("Invalid user agent string provided.")
    """

    def __init__(self, message: str):
        """
        Initializes the BadUserAgent exception.

        Args:
            message (str): The error message for the exception.
        """
        super().__init__(message)
