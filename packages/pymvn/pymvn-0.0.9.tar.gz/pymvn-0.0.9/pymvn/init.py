# 初始化项目
import os


def init():
    root_path = os.getcwd()
    pybuild_path = f"{root_path}/.pymvn"
    if not os.path.exists(pybuild_path):
        with open(pybuild_path, mode="w", encoding="utf-8") as f:
            f.write("main_func = \n")
            f.write("excludes = []\n")

