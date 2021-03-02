# AO#labels#AObject
import os
import json
from pathlib import Path

from .AParamDict import *
from . import fileui


class AObject(object):
    """AObject (class): This is a paarent class used to implement any comon serialization or typing we might want to do later
        Attributes:
            labels: dictionary of meta_data
            save, load, and clear funcs: these are hooks for functions that manage the object's data on disk.
    """

    AOBJECT_BASE_PATH = "."

    def __init__(self, path=None, **kwargs):
        self.initializeBlank()
        if path:
            self.setPath(file_path=path, **kwargs)

    def initializeBlank(self):
        self.a_info = {"AObjectType": self.AOBJECT_TYPE()}
        # self.a_data = AParamDict(owner=self, name='a_data')
        self.save_func = None
        self.load_func = None
        self.clear_func = None

    def setPath(self, file_path=None, **kwargs):
        if file_path:
            p = Path(file_path)
            self.a_info["file_path"] = p
            self.a_info["file_name"] = p.name
            self.a_info["directory_path"] = p.parent
            filename = self.a_info.get("file_name")
            if filename:
                self.a_info["file_base_name"] = p.stem
                self.a_info["file_ext"] = p.suffix
            base_path = kwargs.get("base_path")
            if base_path is None:
                base_path = AObject.AOBJECT_BASE_PATH
            self.a_info["base_path"] = Path(base_path)

    def getPath(self):
        if "file_path" in self.a_info:
            return Path(self.a_info["file_path"])
        else:
            return None

    def _showFile(self):
        if fileui.Show is not None:
            fileui.Show(self.getPath())

    def _open(self):
        if fileui.Open is not None:
            fileui.Open(self.getPath())

    def getRelativePath(self, base_path=None):
        base = base_path
        if base is None:
            base = self.a_info.get("base_path")
        if base is None:
            AWARN("Base path not set!")
        return str(self.getPath())

    def getFileName(self):
        if "file_name" in self.a_info:
            return self.a_info["file_name"]
        else:
            return None

    def getFileExtension(self):
        if "file_ext" in self.a_info:
            return self.a_info["file_ext"]
        else:
            return None

    def getDirectoryPath(self):
        return self.a_info.get("directory_path")

    def setInfo(self, label, value):
        self.a_info[label] = value

    def getInfo(self, label):
        return self.a_info.get(label)

    def loadFromJSON(self, json_path=None):
        if json_path:
            self.setPath(file_path=json_path)
        if "file_path" in self.a_info:
            json_text = open(self.a_info["file_path"]).read()
            d = json.loads(json_text)
            self.initFromDictionary(d)

    def writeToJSON(self, json_path=None):
        # with open(jsonpath+self.name+'.json', 'w') as outfile:
        if not json_path:
            json_path = self.a_info.get("file_path")
        if json_path:
            with open(json_path, "w") as outfile:
                json.dump(
                    self.toDictionary(),
                    outfile,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                    default=AObject.serializer
                )

    def serializeInfo(self):
        return self.a_info

    def save(self, features_to_save="all", overwrite=True, **kwargs):
        if self.save_func:
            self.save_func(
                self, features_to_save=features_to_save, overwrite=overwrite, **kwargs
            )
        else:
            AWARN(
                "SAVE FUNCTION HAS NOT BEEN PROVIDED FOR {} INSTANCE".format(
                    self.AOBJECT_TYPE()
                )
            )

    def load(self, features_to_load=None, **kwargs):
        if self.load_func:
            self.load_func(self, features_to_load=features_to_load, **kwargs)
        else:
            AWARN(
                "LOAD FUNCTION HAS NOT BEEN PROVIDED FOR {} INSTANCE".format(
                    self.AOBJECT_TYPE()
                )
            )

    ########### "VIRTUAL" FUNCTIONS #############
    @staticmethod
    def AOBJECT_TYPE():
        return "AObject"

    def toDictionary(self):
        d = {"a_info": self.serializeInfo()}
        return d

    def initFromDictionary(self, d):
        self.a_info = d.get("a_info")

    @staticmethod
    def serializer(obj):
        # Path objects do not natively serialize to JSON
        if isinstance(obj, Path):
            return os.fspath(obj)
        return obj

    # ##Example of how these functions should be written in a  subclass, here we call the subclass 'AssetManager'
    # def AOBJECT_TYPE(self):
    #     return 'AssetManager'
    #
    # def toDictionary(self):
    #     d = AObject.toDictionary(self)
    #     #serialize class specific members
    #     return d
    #
    # def initFromDictionary(self, d):
    #     AObject.initFromDictionary(self, d)
    #     #do class specific inits with d
