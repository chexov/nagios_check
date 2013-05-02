#!/usr/bin/env python
import sys
import subprocess
try:
    #py2
    import ConfigParser as configparser
except:
    #py3
    import configparser

"""
Plugin Return Code  Service State   Host State
0   OK  UP
1   WARNING UP or DOWN/UNREACHABLE*
2   CRITICAL    DOWN/UNREACHABLE
3   UNKNOWN DOWN/UNREACHABLE

now=`date +%s`
commandfile='/usr/local/nagios/var/rw/nagios.cmd'

/bin/printf "[%lu] PROCESS_HOST_CHECK_RESULT;host1;0;Host appears to be UP\n" $now > $commandfile
/bin/printf "[%lu] PROCESS_SERVICE_CHECK_RESULT;host1;service1;0;OK- Everything Looks Great\n" $now > $commandfile

#
PROCESS_HOST_CHECK_RESULT=87
PROCESS_SERVICE_CHECK_RESULT=30
curl -v -X POST -d cmd_mod=2 -d cmd_typ=${PROCESS_SERVICE_CHECK_RESULT} \
        -d host=transcoder -d service="J2K Storage" -d plugin_state=0 -d plugin_output="OK" \
        http://nagiosadmin:pass@bigbrother/cgi-bin/nagios3/cmd.cgi

"""
SECTION_STATUS = "status"
SECTION_CHECKS = "checks"


if len(sys.argv) != 2:
    print ("Usage: {0} <nagios_check.cfg".format(sys.argv[0]))
    sys.exit(1)

config_fn = sys.argv[1]

cp = configparser.ConfigParser()
cp.read(config_fn)
if not SECTION_STATUS in cp.sections():
    cp.add_section(SECTION_STATUS)

for check, cmd in cp.items(SECTION_CHECKS):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    e = p.wait()
    try:
        old_e = cp.getint(SECTION_STATUS, check+"_e")
    except ConfigParser.NoOptionError:
        old_e = -1

    cp.set(SECTION_STATUS, check, out.splitlines()[0])
    cp.set(SECTION_STATUS, check+"_e", e)

    if old_e != e:
        print ("XXX: send notification email")

    print (old_e, e, check, cmd, out.splitlines()[0])

cp.write(open(config_fn, 'w'))

