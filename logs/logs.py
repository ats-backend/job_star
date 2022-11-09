import logging


def log_writter(action):

    # if logging.DEBUG:
    #     logging.basicConfig(
    #         filename="log.txt",
    #         level=logging.DEBUG,
    #         format="%(asctime)s %(message)s"
    #     )
    #     return logging

    return logging.info(f"{action}")

