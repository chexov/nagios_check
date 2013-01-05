#!/usr/bin/env python
import sys
import subprocess
import ConfigParser

SECTION_STATUS = "status"
SECTION_CHECKS = "checks"

config_fn = sys.argv[1]

cp = ConfigParser.ConfigParser()
cp.read(config_fn)
if not SECTION_STATUS in cp.sections():
    cp.add_section(SECTION_STATUS)

for check, cmd in cp.items(SECTION_CHECKS):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    e = p.wait()
    cp.set(SECTION_STATUS, check, out.splitlines()[0])
    cp.set(SECTION_STATUS, check+"_e", e)

    print e, check, cmd, out.splitlines()[0]

cp.write(open(config_fn, 'w'))

