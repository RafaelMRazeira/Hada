import logging
import os
import sys


def setup_logger(name, save_dir, filename="log.txt", remove_old_log=False):
    """

    Parameters
    ----------
    name : str
        Logger name
    save_dir : str|path:
        dir to save log files
    filename :
         (Default value = "log.txt")
        file name for log files

    Returns
    -------
        Logger
            Logger object
    """

    log_path = os.path.join(save_dir, filename)
    if remove_old_log and os.path.exists(log_path):
        os.remove(log_path)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if save_dir:
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_logger(name):
    """

    Parameters
    ----------
    name : str
        Logger name

    Returns
    -------
        Logger
            Logger object
    """
    return logging.getLogger(name)
