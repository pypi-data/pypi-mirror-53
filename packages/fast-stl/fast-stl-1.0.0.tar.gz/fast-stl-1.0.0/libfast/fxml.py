# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-09-29.
# Copyright (c) 2019 3KWan.
# Description :
import os
from typing import Any

from libfast.flog import log

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree


class FManifest:
    __default_android_ns = "http://schemas.android.com/apk/res/android"
    __name = "{" + __default_android_ns + "}name"
    __value = "{" + __default_android_ns + "}value"
    __res = ""
    __tree = None
    __root = None

    def __init__(self):
        pass

    def parse(self, res: str) -> None:

        """
        解析xml文件
        :param res: 源文件路径
        """

        elementTree.register_namespace("android", self.__default_android_ns)

        if os.path.exists(res):
            self.__res = res
            self.__tree = elementTree.parse(res)
            self.__root = self.__tree.getroot()
        else:
            log("source file does not exist")

    def save(self, res: str = None):
        if res is None or res.strip() == "":
            self.__tree.write(self.__res, "utf-8")
        else:
            self.__tree.write(res, "utf-8")

    # ====== activity ======

    def get_activity_list(self) -> list:
        """
        获取xml中Application节点下所有的activity
        :return: activity列表
        """
        if self.__root is not None:
            return self.__root.find(".//application").findall("activity")
        else:
            log("root is None")

    def find_activity(self, name) -> Any:
        """
        查找指定的activity
        :param name: activity名称
        :return: activity的Element对象
        """
        if name is None or name.strip() == "":
            log("target name is None or length is 0")
            return None
        activity_list = self.get_activity_list()
        if activity_list is not None and len(activity_list) != 0:
            for activity in activity_list:
                if activity.get(self.__name) == name:
                    return activity
        else:
            log("activity list is None or length is 0")

    def del_activity(self, name: str) -> bool:
        """
        删除指定的activity
        :param name: activity名称
        :return: 是否删除成功
        """
        if name is None or name.strip() == "":
            log("name is None or length is 0")
            return False
        activity = self.find_activity(name)
        if activity is not None:
            self.__root.find(".//application").remove(activity)
            # __save_xml(res, __parse_xml(res))
            return True
        else:
            log("target activity is None")
            return False

    # ====== activity ======

    # ====== meta-data ======

    def get_meta_data_list(self) -> list:
        """
        获取xml中Application节点下所有的meta-data
        :return: meta-data列表
        """
        if self.__root is not None:
            return self.__root.find(".//application").findall("meta-data")
        else:
            log("root is None")

    def find_meta_data(self, name: str) -> Any:
        """
        查找指定的meta-data
        :param name: meta-data名称
        :return: meta-data的Element对象
        """
        if name is None or name.strip() == "":
            log("target name is None or length is 0")
            return None
        meta_data_list = self.get_meta_data_list()
        if meta_data_list is not None and len(meta_data_list) != 0:
            for meta_data in meta_data_list:
                if meta_data.get(self.__name) == name:
                    return meta_data
        else:
            log("meta-data list is None or length is 0")

    def modify_meta_data_value(self, name: str, value: str) -> bool:
        """
        修改meta-data中value
        :param name: meta-data名称
        :param value: meta-data值
        :return: 是否修改成功
        """
        if name is None or name.strip() == "":
            log("name is None or length is 0")
            return False
        if value is None or value.strip() == "":
            log("value is None or length is 0")
            return False
        self.find_meta_data(name).set(self.__value, value)
        return True

    def del_meta_data(self, name: str) -> bool:
        """
        删除指定的meta-data
        :param name: meta-data名称
        :return: 是否删除成功
        """
        if name is None or name.strip() == "":
            log("name is None or length is 0")
            return False
        meta_data = self.find_meta_data(name)
        if meta_data is not None:
            self.__root.find(".//application").remove(meta_data)
            return True
        else:
            log("target meta-data is None")
            return False

    def add_meta_data(self, name: str, value: str) -> bool:
        """
        增加新的meta-data节点
        :param name: meta-data名称
        :param value: meta-data值
        :return: 是否增加成功
        """
        if name is None or name.strip() == "":
            log("name is None or length is 0")
            return False
        if value is None or value.strip() == "":
            log("value is None or length is 0")
            return False
        elementTree.SubElement(self.__root.find(".//application"), "meta-data",
                               {self.__name: name, self.__value: value})
        return True

    # ====== meta-data ======


def parse(res: str) -> FManifest:
    """
    解析xml文件
    :param res: 源文件路径
    :return: FManifest对象
    """
    manifest = FManifest()
    manifest.parse(res)
    return manifest
