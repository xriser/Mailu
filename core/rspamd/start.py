#!/usr/bin/python3

import os
import glob
import logging as log
import sys
from socrate import system, conf

log.basicConfig(stream=sys.stderr, level=os.environ.get("LOG_LEVEL", "WARNING"))

# Actual startup script

os.environ["FRONT_ADDRESS"] = os.getenv("FRONT_ADDRESS", default="front")
os.environ["REDIS_ADDRESS"] = os.getenv("REDIS_ADDRESS", default="redis")

if os.environ.get("ANTIVIRUS") == 'clamav':
    os.environ["ANTIVIRUS_ADDRESS"] = os.getenv("ANTIVIRUS_ADDRESS", default="antivirus:3310")

for rspamd_file in glob.glob("/conf/*"):
    conf.jinja(rspamd_file, os.environ, os.path.join("/etc/rspamd/local.d", os.path.basename(rspamd_file)))

# Run rspamd
os.execv("/usr/sbin/rspamd", ["rspamd", "-i", "-f"])
