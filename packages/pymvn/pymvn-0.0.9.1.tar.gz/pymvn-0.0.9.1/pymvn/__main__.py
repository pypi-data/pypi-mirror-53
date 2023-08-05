import sys

from pymvn.init import *
from pymvn.integrate import *


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("please input: init, package, clear...")
        sys.exit(-1)
    opt = {"init": init,
           "package": package,
           "clear": clear}
    param = str(sys.argv[1]).strip()
    try:
        opt[param]()
    except KeyError as e:
        logger.error(f"unknown param: {param}, please input: init, package, clear")
        sys.exit(-1)

