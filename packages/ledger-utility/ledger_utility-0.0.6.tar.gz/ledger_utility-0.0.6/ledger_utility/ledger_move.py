import glob
import os
import pathlib
import shutil
import subprocess
import sys

import toml
from appdirs import *
from helputils.core import format_exception, mkdir_p

appname = "ledger_utility"
appauthor = "ledger_utility"
toml_file = os.path.join(user_data_dir(appname, appauthor), "ledger-utility.toml")
mkdir_p(user_data_dir(appname, appauthor))



def create_example_config():
    example_config = (
        '# DL_DIR = "/home/user/dl"\n'
        '# 1822DIREKT_CSV = "/home/user/all/doc/fin/bank/1822direkt/csv/"\n'
        '# COMDIRECT_CSV = "/home/user/all/doc/fin/bank/comdirect/csv/"\n'
        '# SANTANDER_ARCH = "/home/user/all/doc/fin/bank/santander/pdf/arch"\n'
        '# SANTANDER_PDF = "/home/user/all/doc/fin/bank/santander/pdf/all-statements.pdf"\n'
        '# SANTANDER_NEW = "/home/user/all/doc/fin/bank/santander/pdf/new"\n'
        '# SANTANDER_TMP_PDF = "/home/user/all/doc/fin/bank/santander/pdf/tmp.pdf"'
    )
    if not os.path.isfile(toml_file):
        print("(Create) example config in %s" % toml_file)
        print("(Info) Please edit the config file, then run ledger-mv")
        with open(toml_file, "w") as _file:
            _file.write(example_config)


create_example_config()
try:
    conf = toml.loads(pathlib.Path(toml_file).read_text())
except Exception as e:
    print("(Error) Please edit the config file, then run ledger-mv %s" % toml_file)
    print(format_exception(e))
    sys.exit()


def environment():
    """(Create) directory"""
    for x in (
        conf["1822DIREKT_CSV"],
        conf["COMDIRECT_CSV"],
        conf["SANTANDER_ARCH"],
        conf["SANTANDER_NEW"]
    ): 
        mkdir_p(x)


def _1822direkt():
    """(Move) CSV download to 1822DIREKT_CSV"""
    for x in pathlib.Path(conf["DL_DIR"]).glob("umsaetze-*-*_*.csv"):
        if os.path.isfile(os.path.join(conf["1822DIREKT_CSV"], x.name)):
            print("(Skip | 1822direkt) %s exist already" % x.name)
            x.unlink()
        else:
            print("(New | 1822direkt) %s to %s" % (x.absolute(), conf["1822DIREKT_CSV"]))
            shutil.move(str(x), conf["1822DIREKT_CSV"])
    print("(Nothing | 1822direkt) Nothing new")


def comdirect():
    """(Move) CSV download to COMDIRECT_CSV"""
    for x in pathlib.Path(conf["DL_DIR"]).glob("umsaetze_*_*-*.csv"):
        if os.path.isfile(os.path.join(conf["COMDIRECT_CSV"], x.name)):
            print("(Skip | Comdirect) %s exist already" % x.name)
            x.unlink()
        else:
            shutil.move(str(x), conf["COMDIRECT_CSV"])
            print("(New | Comdirect) %s to %s" % (x.name, conf["COMDIRECT_CSV"],))
            # shutil.move
    print("(Nothing | Comdirect) Nothing new")


def santander():
    """(Move/Add) PDF to SANTANDER_ARCH and add PDF to unified PDF"""
    # (Remove) duplicated downloads
    for p in pathlib.Path(conf["DL_DIR"]).glob("*CARD_STATEMENT_1PLUS*\(*\).pdf"):
        print("(Remove | Santander) %s" % p.name)
        p.unlink()
    # (Copy) downloaded PDF to SANTANDER_NEW if not in SANTANDER_ARCH
    for p in pathlib.Path(conf["DL_DIR"]).glob("*CARD_STATEMENT_1PLUS*.pdf"):
        if not os.path.isfile(os.path.join(conf["SANTANDER_ARCH"], p.name)):
            shutil.move(str(p), conf["SANTANDER_NEW"])
            print("(Copy | Santander) %s to %s" % (p.name, conf["SANTANDER_NEW"]))
            # shutil.move
        else:
            os.remove(str(p))
            print("(Skip | Santander) %s already in %s" % (p.name, conf["SANTANDER_ARCH"]))
    # (Create) PDF
    add_new_pdf = sorted([str(p) for p in pathlib.Path(conf["SANTANDER_NEW"]).glob("*.pdf")], reverse=True)
    if add_new_pdf:
        if os.path.isfile(conf["SANTANDER_PDF"]):
            p1 = subprocess.Popen(["pdfunite"] + add_new_pdf + [conf["SANTANDER_PDF"]] + [conf["SANTANDER_TMP_PDF"]])
            print("(Add | Santander) to Santander PDF %s" % conf["SANTANDER_PDF"])
        else:
            p1 = subprocess.Popen(["pdfunite"] + add_new_pdf + [conf["SANTANDER_TMP_PDF"]])
            print("(New | Santander) Santander PDF %s" % conf["SANTANDER_PDF"])
        out, err = p1.communicate()
        if out:
            print("(pdfunite | Santander)", out)
        if err:
            print("(pdfunite | Santander)", err)
        shutil.move(conf["SANTANDER_TMP_PDF"], conf["SANTANDER_PDF"])
        # (Move) new statements to archive
        for f in pathlib.Path(conf["SANTANDER_NEW"]).glob("*"):
            if not os.path.isfile(os.path.join(conf["SANTANDER_ARCH"], f.name)):
                shutil.move(str(f), conf["SANTANDER_ARCH"])
            else:
                os.remove(str(f))
    else:
        print("(Nothing | Santander) Nothing new")


def main():
    environment()
    _1822direkt()
    comdirect()
    santander()
