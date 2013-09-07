import os
import re
import subprocess


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def skip_check(check_type):
    base_dir = system('git', 'rev-parse', '--show-toplevel').strip()
    skip_file = os.path.join(base_dir, "skip_%s" % check_type)
    if os.path.exists(skip_file):
        os.remove(skip_file)
        return True


def get_modified_files(file_ext):
    modified = re.compile('^(?P<name>.*\.%s)$' % file_ext, re.MULTILINE)
    files = system('git', 'diff', '--staged', '--name-only', '--diff-filter=ACMRTUXB')
    return modified.findall(files)
