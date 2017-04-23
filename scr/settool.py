#!/usr/bin/env python

import os
import sys
import xml.etree.ElementTree as ET

from argparse import ArgumentParser
from distutils.spawn import find_executable


class Xmlparser():

    def __init__(self, root):
        self.root = root

    def __priv_find_versions__(self, version_list):
        versions = []
        for i2 in version_list:
            for i3 in [ x for x in i2 if x.tag == "ver" ]:
                versions.append(i3.attrib["name"])
        return versions

    def get_tool_versions(self, toolname):
        for i2 in self.root:
            if i2.attrib["name"] == toolname:
                version_list = [ x for x in i2 if x.tag == "versions" ]
                return self.__priv_find_versions__( version_list )

    def get_available_toolchains(self):
        toolchains = []
        for i2 in self.root:
            if i2.tag == "tool":
                toolchains.append(i2.attrib["name"])
        return toolchains




def ptp(msg):
    """ print this please

    """
    print(msg)


def run_settool():

    parser = ArgumentParser(description="Settool utility")
    parser.add_argument("toolchain")
    args = parser.parse_args()

    try:
        homebin = os.environ["HOMEBIN"]
    except:
        print("Error Environment variable HOMEBIN not specified")
        sys.exit()

    success = False

    tree = ET.parse('/home/addman/toolchains.xml')
    root = tree.getroot()

    xmlp = Xmlparser(root)
    print(xmlp.get_tool_versions("espresso"))
    print(xmlp.get_available_toolchains())


    #versions = []

    #for c2 in root:
    #    if c2.tag == "tool":
    #        if c2.attrib["name"] == sys.argv[1]:
    #            for c3 in c2:
    #                if c3.tag == "versions":
    #                    for c4 in c3:
    #                        if c4.tag == "ver":
    #                            versions.append(c4.attrib["name"])

    #if not success:
    #    print("Sorry there is no such thing as " + sys.argv[1])
    #print("Avaible version of " + sys.argv[1] + ":")
    #print("")

    #for ii, version in enumerate(versions):
    #    print(str(ii) + ": " + str(version))
    #print(str(len(versions)) + ": None")

    #print("")

    #try: input = raw_input
    #except NameError: pass

    #choice = input("choose option: ")

    #try:
    #    choice = int(choice)
    #    if choice == len(versions):
    #        version_name = "None"
    #    else:
    #        version_name = versions[choice]
    #except:
    #    print("Bad choice, exiting")
    #    sys.exit()

    #suffix = None

    #for c2 in root:
    #    if c2.tag == "tool":
    #        if sys.argv[1] == c2.attrib["name"]:
    #            executables = []
    #            executables_remove = []
    #            for c3 in c2:
    #                if c3.tag == "executables":
    #                    for c4 in c3:
    #                        if c4.tag == "item":
    #                            executables.append([None, c4.attrib["name"], c4.attrib["name"]])
    #                if c3.tag == "versions":
    #                    for c4 in c3:
    #                        if c4.tag == "ver":
    #                            if version_name == c4.attrib["name"]:
    #                                suffix = None
    #                                for c5 in c4:
    #                                    if c5.tag == "suffix":
    #                                        suffix = c5.text
    #                                    if c5.tag == "itemdir":
    #                                        for d, dn, fn in os.walk(c5.attrib["path"]):
    #                                            for file in fn:
    #                                                executables.append([c5.attrib["path"],file,file])
    #                                            break
    #                                    if c5.tag == "vername":
    #                                        for ii in range(len(executables)):
    #                                            if executables[ii][1] == c5.attrib["name"]:
    #                                                executables[ii][2] = c5.text
    #                                if "path" in c4.attrib.keys():
    #                                    for i in range(len(executables)):
    #                                        if executables[i][0] is None:
    #                                            executables[i][0] = c4.attrib["path"]
    #                            else:
    #                                for c5 in c4:
    #                                    if c5.tag == "itemdir":
    #                                        for d, dn, fn in os.walk(c5.attrib["path"]):
    #                                            for file in fn:
    #                                                if file not in executables_remove:
    #                                                    executables_remove.append(file)
    #                                            break


    #for path, exe, source_exe in executables:
    #    if exe in executables_remove:
    #        executables_remove.remove(exe)

    #for path, exe, source_exe in executables:
    #    if path is None:
    #        if suffix is None:
    #            suffix = ""
    #        source = find_executable(source_exe+suffix)
    #        if source is None:
    #            source = find_executable(source_exe+suffix.replace(".","-"))
    #        if source is not None:
    #            try:
    #                os.symlink(source,homebin+"/"+exe)
    #            except (OSError) as e:
    #                os.remove(homebin+"/"+exe)
    #                os.symlink(source,homebin+"/"+exe)
    #        else:
    #            try:
    #                os.remove(homebin+"/"+exe)
    #            except OSError:
    #                pass
    #    else:
    #        try:
    #            os.symlink(path+"/"+source_exe,homebin+"/"+exe)
    #        except (OSError) as e:
    #            os.remove(homebin+"/"+exe)
    #            os.symlink(path+"/"+source_exe,homebin+"/"+exe)

    #for remexe in executables_remove:
    #    try:
    #        os.remove(homebin+"/"+remexe)
    #    except OSError:
    #        pass


if __name__ == "__main__":
    run_settool()
