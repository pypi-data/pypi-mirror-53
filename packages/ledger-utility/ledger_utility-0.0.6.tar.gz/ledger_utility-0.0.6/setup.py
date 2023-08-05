import re
from distutils.core import setup
from setuptools import find_packages

VERSIONFILE="ledger_utility/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="ledger_utility",
    version=verstr,
    author="eayin2",
    author_email="eayin2@gmail.com",
    packages=find_packages(),
    url="",
    description="Ledger utility",
    install_requires=[
        "helputils"
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ledger-mv = ledger_utility.ledger_move:main",
            "ledger-calc = ledger_utility.ledger_calc:main"
        ],
    },
)
