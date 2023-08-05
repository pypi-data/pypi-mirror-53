#!/usr/bin/python3 -u
"""
Setup script for PLIB3.STDLIB package
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information
"""

from plib.stdlib import __version__ as version

name = "plib3.stdlib"
description = "Useful packages and modules to extend the Python 3 standard library."

author = "Peter A. Donis"
author_email = "peterdonis@alum.mit.edu"

startline = 5
endspec = "The Zen of PLIB3"

dev_status = "Production/Stable"

license = "GPLv2"

data_dirs = ["examples"]

classifiers = """
Environment :: Console
Environment :: MacOS X
Environment :: Win32 (MS Windows)
Intended Audience :: Developers
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: POSIX :: Linux
Topic :: Software Development :: Libraries :: Python Modules
"""

post_install = ["plib3-setup-{}".format(s) for s in ("stdlib-examples",)]

rst_header_template = """**{basename}** for {name} {version}

:Author:        {author}
:Release Date:  {releasedate}
"""


if __name__ == '__main__':
    import sys
    import os
    from subprocess import call
    from distutils.core import setup
    from setuputils import convert_rst, current_date, setup_vars, long_description as make_long_description
    
    if "sdist" in sys.argv:
        convert_rst(rst_header_template,
            startline=2,
            name=name.upper(),
            version=version,
            author=author,
            releasedate=current_date("%d %b %Y")
        )
        call(['sed', '-i', 's/gitlab.com\/pdonis\/plib-/pypi.org\/project\/plib./', 'README'])
        call(['sed', '-i', 's/gitlab.com\/pdonis\/plib3-/pypi.org\/project\/plib3./', 'README'])
        call(['sed', '-i', 's/gitlab.com\/pdonis/pypi.org\/project/', 'README'])
    elif os.path.isfile("README.rst"):
        startline = 3
        long_description = make_long_description(globals(), filename="README.rst")
    setup(**setup_vars(globals()))
    if "install" in sys.argv:
        for scriptname in post_install:
            os.system(scriptname)
