""" setting up a logger for the multi-agent package """
from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL, Logger, getLogger, FileHandler, Formatter
from rich.logging import RichHandler

"""Note : Print Levels
1. CRITICAL
2. ERROR
3. WARNING
4. INFO
5. DEBUG
"""

def initialize_logging(name: str = __name__) -> Logger:
    """Initialize logger for logging system.

    Args:
        name (str, optional): Name of logging file.
            - Defaults to __name__.

    Returns:
        Logger: Logger to handle.
    """

    # logger settings
    FORMAT = "%(message)s"
    DATE_FORMAT = "%m/%d,%H:%M:%S.%f"
    basicConfig(
        level=INFO,
        format=FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = getLogger(name)

    return logger
