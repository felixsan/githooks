#!/usr/bin/env python

import os
import shutil
import sys
import tempfile


from common import skip_check, get_modified_files, system

DISPLAY_NAME = "PyFlakes"
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
        output = system('pyflakes', '.', cwd=tempdir)

        shutil.rmtree(tempdir)
        if output:
            print "Not committing since there are %s errors.\n" % DISPLAY_NAME
            print output,
            print
            sys.exit(1)


if __name__ == '__main__':
    main()
