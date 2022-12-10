import os

import requests

ses = requests.Session()
ses.cookies.set("session", os.getenv("SESSION_TOKEN"))

__all__ = ["ses"]
