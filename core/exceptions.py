class AIServiceUnavailableError(Exception):
    """Raised when the AI provider is temporarily unavailable."""


class AIQuotaExceededError(Exception):
    """Raised when the AI provider quota has been exceeded."""