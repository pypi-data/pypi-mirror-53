#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys

import pytest
from lxml import etree

os.environ["IN_PYTEST"] = "1"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(PROJECT_ROOT, 'README.md')):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
    if PROJECT_ROOT == '/':
        break
else:
    if PROJECT_ROOT not in sys.path:
        print('%s is added to sys.path by %s' % (PROJECT_ROOT, __file__))
        sys.path.insert(0, PROJECT_ROOT)

skip_pattern = [
    (re.compile(r'test/main\.py'), 9999)
]


def skip_files():
    # 读
    with open(os.path.join(PROJECT_ROOT, 'htmlcov', 'index.html'), 'rb') as ifile:
        text = ifile.read()

    # 遍历 tr，td
    root = etree.HTML(text)
    file_line = root.xpath('//*[@id="index"]/table/tbody/tr[@class="file"]')
    for line in file_line:
        cell = [x for x in line.xpath('./td//text()')]

        # 删除
        if cell[4] == '100%':
            line.xpath('..')[0].remove(line)
            continue

        # 匹配，删除
        for reg, limit in skip_pattern:
            if reg.match(cell[0]) and int(cell[2]) <= limit:
                if 'migrations' not in cell[0]:
                    print('skip %s' % cell[0])
                line.xpath('..')[0].remove(line)
                break

    # 写
    with open(os.path.join(PROJECT_ROOT, 'htmlcov', 'index.html'), 'wb') as ofile:
        ofile.write(etree.tostring(root).decode().replace('js"/>', 'js"></script>').encode())


def main():
    root = [os.path.join(PROJECT_ROOT, x) for x in ['test', 'wg_pyutils']]
    cov = ['--cov=%s' % x for x in root]

    pytest.main(root + ['--exitfirst'] + cov + ['--cov-report', 'html'])

    skip_files()


if '__main__' == __name__:
    main()
