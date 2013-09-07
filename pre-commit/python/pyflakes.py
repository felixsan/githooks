#!/usr/bin/env python

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
    skip_file = os.path.join(base_dir, "skip_pyflakes")
    if os.path.exists(skip_file):
        os.remove(skip_file)
        return True


def get_modified_files():
    modified = re.compile('^(?P<name>.*\.py)$', re.MULTILINE)
    files = system('git', 'diff', '--staged', '--name-only', '--diff-filter=ACMRTUXB')
    return modified.findall(files)


def main():
    if skip_check():
        print "* Skipping PyFlakes check..."
        return
    print "* Running PyFlakes check..."
    files = get_modified_files()
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
        print "Not committing since there are PyFlakes errors.\n"
        print output,
        print
        sys.exit(1)


if __name__ == '__main__':
    main()
