#!/usr/bin/env python

# Copyright (c) 2017 Ot(t)o Kohul\'{a}k *
# See included LICENSE file

# * Number of 't' in my first name may fluctuate over time

import os
import sys
import xml.etree.ElementTree as ET

from argparse import ArgumentParser
from distutils.spawn import find_executable

# The worst error message ever:
worst_error_msg = "Something bad happened, exiting"

# To make input python 2 / 3 compatible
try:
    input = raw_input
except NameError:
    pass


class Xmlparser():

    def __init__(self, root):
        self.root = root

    def __priv_find_versions__(self, version_list):
        versions = []
        for i2 in version_list:
            for i3 in [x for x in i2 if x.tag == "ver"]:
                versions.append(i3.attrib["name"])
        return versions

    def __priv_get_version(self, version_root, version_name):
        for vr in version_root:
            if vr.tag == "ver" and \
               vr.attrib["name"] == version_name:
                return vr
        return None

    def get_tool_versions(self, toolname):
        for i2 in self.root:
            if i2.attrib["name"] == toolname:
                version_list = [x for x in i2 if x.tag == "versions"]
                return self.__priv_find_versions__(version_list)
        return []

    def get_available_toolchains(self):
        toolchains = []
        for i2 in self.root:
            if i2.tag == "tool":
                toolchains.append(i2.attrib["name"])
        return toolchains

    def get_executables(self, toolname, version_name):
        ret = {}
        # ret["execs"][0] are sources and ...[1] are distinations
        ret["execs"] = [[], []] 
        ret["path"] = None
        ret["suffix"] = ""
        td = None
        for i2 in self.root:
            if i2.attrib["name"] == toolname:
                td = i2
        if td is None:
            ptp(worst_error_msg)
            sys.exit()
        for i3 in td:
            if i3.tag == "executables":
                sources = [x.attrib["name"] for x in i3 if x.tag == "item"]
                ret["execs"][0] = list(sources)
                ret["execs"][1] = list(sources)
            if i3.tag == "versions":
                vd = self.__priv_get_version(i3, version_name)
        if vd is None:
            ptp(worst_error_msg)
            sys.exit()
        for i4 in vd:
            if i4.tag == "itemdir":
                ret["path"] = i4.attrib["path"]
                ret["took_all"] = False
                # TODO figure out how to get rid of this indent
                if "all" in i4.attrib.keys():
                    all_value = i4.attrib["all"]
                    ret["took_all"] = True if all_value == "T" else False
            if i4.tag == "vername":
                index = ret["execs"][0].index(i4.attrib["name"])
                ret["execs"][0][index] = i4.text
            if i4.tag == "suffix":
                ret["suffix"] = i4.text
        return ret


def ptp(msg = ""):
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

    versions = xmlp.get_tool_versions(args.toolchain)

    # Check if toolchain exists
    if len(versions) == 0:
        ptp("There is no such thing as {}".format(args.toolchain))
        os.exit()

    ptp("Available version{} for {}:".format("" if len(versions) == 0 else "s",
                                             args.toolchain))
    ptp()
    for ii, version in enumerate(versions):
        ptp("# {}: {}".format(ii, version))

    choice = input("Choose option: ")

    try:
        choice = int(choice)
        version_name = versions[choice]
    except ValueError:
        ptp("Bad choice, exiting")
        os.exit()
    except IndexError:
        ptp("Bad choice, exiting")
        os.exit()
    except:
        ptp(worst_error_msg)
        os.exit()

    all_I_need = xmlp.get_executables(args.toolchain,version_name)

    if all_I_need["path"] is None:
        for source in all_I_need["sources"][0]:
            real_path = find_executable(source+all_I_need["suffix"])
            try:
                os.symlink(real_path,homebin+"/"+source)
            except (OSError) as e:
                os.remove(homebin+"/"+exe)
                os.symlink(real_path,homebin+"/"+source)
    elif all_I_need["tool_all"]:
        # TODO do your own generator
        for directory, dir_names, filenames in os.walk(all_I_need["path"]):
            for filename in filenames:
                try:
                    os.symlink(directory+filename,homebin+"/"+source)
                except (OSError) as e:
                    os.remove(homebin+"/"+source)
                    os.symlink(directory+filename,homebin+"/"+source)
    else:
        for ii in range(len(all_I_need["sources"][0])):
            pass



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
