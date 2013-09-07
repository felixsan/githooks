#!/usr/bin/env python

# Pep 8 githook modified from Kevin McConnell's version at http://tech.myemma.com/python-pep8-git-hooks/

import os
import shutil
import sys
import tempfile

from common import skip_check, get_modified_files, system

DISPLAY_NAME = "Pep8"
FILE_EXT = "py"


def main():
    if skip_check(DISPLAY_NAME):
        print "* Skipping %s check..." % DISPLAY_NAME
        return
    files = get_modified_files(FILE_EXT)
    if files:
        print "* Running %s check..." % DISPLAY_NAME
        tempdir = tempfile.mkdtemp()
        for name in files:
            filename = os.path.join(tempdir, name)
            filepath = os.path.dirname(filename)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            with file(filename, 'w') as f:
                system('git', 'show', ':%s' % name, stdout=f)
        output = system('pep8', '--show-source', '--statistics', '--ignore=E501,E121,E125,E126,E128', '.', cwd=tempdir)
        shutil.rmtree(tempdir)
        if output:
            print "Not committing since there are %s errors.\n" % DISPLAY_NAME
            print output,
            print
            sys.exit(1)


if __name__ == '__main__':
    main()
