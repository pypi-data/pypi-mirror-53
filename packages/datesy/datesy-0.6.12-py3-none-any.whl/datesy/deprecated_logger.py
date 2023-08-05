from loguru import logger
import sys


def basic_log(log_level=5):
    # ToDo add thread name to style
    # Todo create different styles (one with threading one without)
    style = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
        "<magenta>{name}</magenta>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.remove()
    logger.add(sys.stderr, level=log_level, format=style)
    return logger


print(
    f"{n + number_to_show}: "
    f"{round(ordered_most_similar[entry_a][n + number_to_show], 3, ):1.3f} "
    f"| {entry_a} - "
    f"{most_similar[entry_a][ordered_most_similar[entry_a][n + number_to_show]]}: fit? "
)
