#!/usr/bin/env python

# Pep 8 githook based on Kevin McConnell's version at http://tech.myemma.com/python-pep8-git-hooks/

import os
import re
import shutil
import subprocess
import sys
import tempfile


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def skip_check():
    base_dir = system('git', 'rev-parse', '--show-toplevel').strip()
    skip_file = os.path.join(base_dir, "skip_pep8")
    if os.path.exists(skip_file):
        os.remove(skip_file)
        return True


def get_modified_files():
    modified = re.compile('^(?P<name>.*\.py)$', re.MULTILINE)
    files = system('git', 'diff', '--staged', '--name-only', '--diff-filter=ACMRTUXB')
    return modified.findall(files)


def main():
    if skip_check():
        print "* Skipping Pep8 check..."
        return
    print "* Running Pep8 check..."
    files = get_modified_files()
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
        print "Not committing since there are Pep8 errors.\n"
        print output,
        print
        sys.exit(1)


if __name__ == '__main__':
    main()
