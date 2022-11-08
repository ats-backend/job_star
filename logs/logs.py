import logging

logging.debug("Logging test...")
logging.info("The program is working as expected")
logging.warning("The program may not function properly")
logging.error("The program encountered an error")
logging.critical("The program crashed")


def log_writter():

    if logging.DEBUG:
        logging.basicConfig(
            filename="log.txt",
            level=logging.DEBUG,
            format="%(asctime)s %(message)s"
        )
        return logging
    elif logging.info:
        logging.basicConfig(
            filename="log.txt",
            level=logging.DEBUG,
            format="%(asctime)s %(message)s"
        )
        print(logging)
        return logging.info("The program is working as expected")

