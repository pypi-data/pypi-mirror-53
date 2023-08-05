# 解析.pymvn文件
# ：主函数
import os
import sys
from typing import Set, Tuple

from loguru import logger

from pymvn.dependence import get_root_dependence_path

_root_path = None
_main_func = None
_site_packages_path: str = None
_excludes: Set[str] = None


def get_root_path():
    global _root_path
    if not _root_path:
        _root_path = os.path.split(os.path.split(__file__)[0])[0]
    return _root_path


def get_main_func_path():
    global _main_func, _site_packages_path
    if not _main_func or not _site_packages_path:
        parsepybuild()
    return _main_func


def get_site_packages_path() -> Tuple[str, Set[str]]:
    global _main_func, _site_packages_path
    if not _main_func or not _site_packages_path or not _excludes:
        parsepybuild()
    return _site_packages_path, _excludes


def parse_lst_2_set(lst_str: str) -> Set[str]:
    lst_str = lst_str.strip()
    # 去除 [ ]
    lst_str = lst_str[1: len(lst_str) - 1]
    items = [item.strip() for item in lst_str.split(",")]
    return set(items)


# 解析参数main_func,site_packages_path
def parsepybuild():
    global _main_func, _site_packages_path, _excludes
    _site_packages_path = get_root_dependence_path()
    pybuild_file = f"{os.getcwd()}/.pymvn"
    if not os.path.exists(pybuild_file):
        with open(pybuild_file, mode="w", encoding="utf-8") as f:
            pass
    if not os.path.exists(pybuild_file):
        raise Exception("the .pymvn file not in the project root path")
    with open(pybuild_file, mode="r", encoding="utf-8") as f:
        for line in f:
            if not line:
                continue
            else:
                k, v = line.strip().split("=")
                k = k.strip()
                v = v.strip()
                if k not in {"main_func", "excludes"}:
                    raise KeyError(f".pymvn key error, don't known {k}, please config 'main_func', 'excludes'")
                if not v:
                    raise ValueError(f"nothing for {k}")
                if k == "main_func":
                    _main_func = v
                elif k == "excludes":
                    try:
                        _excludes = parse_lst_2_set(v)
                    except Exception as e:
                        logger.exception(e)
                        sys.exit(-1)



