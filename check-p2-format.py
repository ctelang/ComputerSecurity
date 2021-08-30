#!/usr/bin/python

import sys
import tempfile
import re
import tarfile
import urllib.request
import os

# Extract
def extract(fname):
    d = tempfile.TemporaryDirectory()
    try:
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(d.name)
        tar.close()
    except Exception as e:
        print('Error: could not extract files. Must be valid .tgz file')
        return None

    return d


def valid_fname(fname):
    p = re.compile(r'project2\.([a-zA-Z]{4}[0-9]{4})(?:-([a-zA-Z]{4}[0-9]{4}))?\.tgz')
    m = p.match(fname.split('/')[-1])
    if m is None:
        return False
    id1, id2 = m.groups()
    if id1 == 'erwu1234' or id1 is None:
        return False

    return True


def is_url(url):
    try:
        resp = urllib.request.urlopen(url)
        return True
    except Exception as e:
        raise e
        return False

# Checks for files and if they contain urls. Does not check if they work
def check_xss(temp_d):
    ret = True
    for i in range(4):
        xss = 'xss_%d.txt' % i
        fname = os.path.join(temp_d.name, xss)
        if not(os.path.isfile(fname)):
            print('Error: could not find %s' % xss)
            ret = False
            continue
        with open(fname, 'r') as f:
            url = f.read()
            if not(is_url(url)):
                print('Error: did not find a url in %s' % xss)
                ret = False
                continue

    # check for xss_payload.html
    fname = os.path.join(temp_d.name, 'xss_payload.html')
    if not(os.path.isfile(fname)):
        print('Error: could not find xss_payload.html')
        ret = False

    return ret


# Just checks for files...not gonna try to parse HTML
def check_csrf(temp_d):
    ret = True
    for i in range(2):
        csrf = 'csrf_%d.html' % i
        if not(os.path.isfile(os.path.join(temp_d.name, csrf))):
            print('Error: could not find %s' % csrf)
            ret = False
    return ret

def check_sql(temp_d):
    ret = True
    for i in range(3):
        sql = 'sql_%d.txt' % i
        fname = os.path.join(temp_d.name, sql)
        if not(os.path.isfile(fname)):
            print('Error: could not find %s' % sql)
            ret = False
            continue
        with open(fname, 'r') as f:
            line = f.read()
            if not(line.startswith('username=victim&password=')):
                print('Error: %s not in correct format' % sql)
                ret = False
    return ret


def check_files(temp_d):
    ret = check_xss(temp_d)
    ret &= check_csrf(temp_d)
    ret &= check_sql(temp_d)
    return ret




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Use:')
        print('   python3 %s project2.[identikey].tgz' % sys.argv[0])
        sys.exit(1)

    fname = sys.argv[1]

    if not(valid_fname(fname)):
        print('Error: invalid filename format. Must be "project2.[identikey(s)].tgz"')
        sys.exit(1)

    temp_d = extract(fname)
    if temp_d is None:
        sys.exit(1)


    if check_files(temp_d):
        print('============================')
        print('Passed format check, hooray!')
        print('============================')
        print('Note: this does NOT mean solutions are correct or guarantee a grade,')
        print('only that the format is correct. Please test that your solutions have')
        print('the intended behavior')
    else:
        print('Did not pass format check, please fix!')


