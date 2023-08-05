#!/usr/bin/env python

"""just another mod for printing strings in color."""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys 
import signal
import os
import json
import subprocess
from columnar import columnar
import pkg_resources


import stringcolor.ops as ops


COLORS = ops.Color.colors
cs = ops.Color


def sort_by_alpha():
    """sort dictionary by name alphabetically"""
    newobj = {}
    for key, value in COLORS.items():
        name = value["name"]
        newobj[name] = value
    return dict(sorted(newobj.items()))


def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def main():
    '''just another mod for printing strings in color.'''
    version = pkg_resources.require("string-color")[0].version
    parser = argparse.ArgumentParser(
        description=f"just another mod for{cs(' printing ', 'Chartreuse2', 'DeepPink4')}strings in{cs(' color.', 'green', 'navyblue')}",
        prog='string-color',
        formatter_class=rawtxt
    )
    
    #
    # COMMAND LINE ARGUMENTS
    #parser.print_help()
    #
    parser.add_argument(
        "color",
        help=f"""show info for a specific color:
$ string-color {cs("red", "red")}
$ string-color {cs("'#ffff87'", "#ffff87")}
$ string-color {cs("*grey*", "grey")} # wildcards acceptable""",

        nargs='?',
        default='none'
    )
    parser.add_argument('-x', '--hex', action='store_true', help='show hex values')
    parser.add_argument('-r', '--rgb', action='store_true', help='show rgb values')
    parser.add_argument('--hsl', action='store_true', help='show hsl values')
    parser.add_argument('-a', '--alpha', action='store_true', help='sort by name')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    color = args.color
    show_hex = args.hex
    show_rgb = args.rgb
    show_hsl = args.hsl
    sort_alpha = args.alpha
    if color == "none":
        if sort_alpha:
            sortedc = sort_by_alpha()
        else:
            sortedc = COLORS
        data = []
        subdata = []
        cols = 8
        x = 0
        for key, value in sortedc.items():
            display = " "+value["name"]+" "
            if show_hex:
                display = " "+value["hex"]+" "
            if show_rgb:
                display = " "+value["rgb"]+" "
            if show_hsl:
                display = " "+value["hsl"]+" "

            rgb = value["rgb"].replace("rgb(", "")
            rgb = rgb.replace(")", "")
            rgb_arr = rgb.split(",")
            if int(rgb_arr[0])*0.299 + int(rgb_arr[1])*0.587 + int(rgb_arr[2])*0.114 > 140:
                black = "black"
            else:
                black = "white"
            if x < cols:
                subdata.append(cs(display, black, value["term"]))
            else:
                x = 0
                data.append(subdata)
                subdata = []
                subdata.append(cs(display, black, value["term"]))
            x += 1
        data.append(subdata)
        headers = ["","","","","","","",""]
        table = columnar(data, headers, no_borders=True, justify='c')
        print(table)
    else:
        sortedc = sort_by_alpha()
        for key, value in sortedc.items():
            rgb = value["rgb"].replace("rgb(", "") 
            rgb = rgb.replace(")", "") 
            rgb_arr = rgb.split(",")
            if int(rgb_arr[0])*0.299 + int(rgb_arr[1])*0.587 + int(rgb_arr[2])*0.114 > 140:
                black = "black"
            else:
                black = "white"
            if "*" in color:
                if color.endswith("*") and color.startswith("*"):
                    searchcolor = color.replace("*", "")
                    if searchcolor.lower() in value["name"].lower():
                        print(cs(" "+value["name"]+" "+value["hex"]+" "+value["rgb"]+" "+value["hsl"]+" ", black, value["term"]))
                else:
                    if color.endswith("*"):
                        searchcolor = color.replace("*", "")
                        if value["name"].lower().startswith(searchcolor.lower()):
                            print(cs(" "+value["name"]+" "+value["hex"]+" "+value["rgb"]+" "+value["hsl"]+" ", black, value["term"]))
                    if color.startswith("*"):
                        searchcolor = color.replace("*", "")
                        if value["name"].lower().endswith(searchcolor.lower()):
                            print(cs(" "+value["name"]+" "+value["hex"]+" "+value["rgb"]+" "+value["hsl"]+" ", black, value["term"]))
            else:
                if color.lower() == value["name"].lower() or color == value["hex"] or color == value["term"]:
                    print(cs(" "+value["name"]+" "+value["hex"]+" "+value["rgb"]+" "+value["hsl"]+" ", black, value["term"]))
    exit()

if __name__ == "__main__":
    main()
