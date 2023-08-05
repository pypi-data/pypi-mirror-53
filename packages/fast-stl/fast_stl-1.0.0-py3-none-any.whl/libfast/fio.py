# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-09-29.
# Copyright (c) 2019 3KWan.
# Description :
import os
import shutil

from libfast.flog import log


def copy_files(res: str, target: str) -> bool:
    """
    拷贝文件或文件夹
    :param res: 源文件或源文件夹路径
    :param target: 目标路径
    :return: 是否成功
    """
    try:
        if os.path.isfile(res):
            shutil.copy(res, target)
            return True
        else:
            shutil.copytree(res, target)
            return True
    except Exception as e:
        log(e)
        return False


def remove_files(target: str) -> bool:
    """
    删除文件或文件夹
    :param target: 目标文件或文件夹路径
    :return: 是否成功
    """
    try:
        if os.path.isfile(target):
            os.remove(target)
            return True
        else:
            shutil.rmtree(target)
            return True
    except Exception as e:
        log(e)
        return False


def replace_file_content(res: str, old_tag: str, new_tag: str) -> bool:
    """
    修改可读文件中预定义的标记值
    :param res: 文件路径
    :param old_tag: 预定义的标记
    :param new_tag: 需要替换的标记
    :return: 是否成功
    """
    try:
        with open(res, "r", encoding="utf-8") as f:
            content = f.read().replace(old_tag, new_tag)
        with open(res, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        log(e)
        return False
