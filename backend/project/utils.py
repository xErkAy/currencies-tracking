from logging import Logger


def _print(logger: Logger, message: str, is_error=False):
    print(message)
    logger.info(message) if not is_error else logger.error(message)