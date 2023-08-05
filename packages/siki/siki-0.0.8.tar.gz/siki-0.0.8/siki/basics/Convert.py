# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: May 31, 2018
# Modifi: May 31, 2018

def convert_raw2str(rawdata):
    return rawdata.decode("UTF8")


def convert_str2raw(strdata):
    return strdata.encode("UTF8")