try:
    from .local_settings import *
except:
    from .production import *