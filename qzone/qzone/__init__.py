import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# ignore requests logs
import logging
logging.getLogger("requests").setLevel(logging.WARNING)