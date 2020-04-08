from base64 import b64encode
import logging
import datetime

def base64encode(username, password, domain):
    
    if username is None or password is None or domain is None:
        raise ValueError("Username, password or domain is not specified")
    
    data = f"{username}@{domain}:{password}"
    encodedBytes = b64encode(data.encode("utf-8"))
    
    return str(encodedBytes, "utf-8")

def api_url_joiner(url, path):
    fullUrl = '/'.join(s.strip('/') for s in [url, path])
    return fullUrl
    
def default_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    print()

    LOG_FILENAME = f"{name}_{datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S')}.log"
    fh = logging.FileHandler(LOG_FILENAME, mode='w')
    formatter = logging.Formatter('[%(levelname)s]: %(name)s - %(asctime)s: %(message)s')
    #formatter = logging.Formatter('%(asctime)s - %(name)s - : %(message)s')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

