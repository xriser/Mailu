#!/usr/bin/python3

import os
import logging as log
import sys
from socrate import system, conf

args = os.environ.copy()

log.basicConfig(stream=sys.stderr, level=args.get("LOG_LEVEL", "WARNING"))

# Get the first DNS server
with open("/etc/resolv.conf") as handle:
    content = handle.read().split()
    args["RESOLVER"] = content[content.index("nameserver") + 1]

args["ADMIN_ADDRESS"] = os.getenv("ADMIN_ADDRESS", default="admin")
args["ANTISPAM_WEBUI_ADDRESS"] = os.getenv("ANTISPAM_WEBUI", default="antispam:11334")
if args["WEBMAIL"] != "none":
    args["WEBMAIL_ADDRESS"] = os.getenv("WEBMAIL_ADDRESS", default="webmail")
if args["WEBDAV"] != "none":
    args["WEBDAV_ADDRESS"] = os.getenv("WEBDAV_ADDRESS", default="webdav:5232")

# TLS configuration
cert_name = os.getenv("TLS_CERT_FILENAME", default="cert.pem")
keypair_name = os.getenv("TLS_KEYPAIR_FILENAME", default="key.pem")
args["TLS"] = {
    "cert": ("/certs/%s" % cert_name, "/certs/%s" % keypair_name),
    "letsencrypt": ("/certs/letsencrypt/live/mailu/fullchain.pem",
        "/certs/letsencrypt/live/mailu/privkey.pem"),
    "mail": ("/certs/%s" % cert_name, "/certs/%s" % keypair_name),
    "mail-letsencrypt": ("/certs/letsencrypt/live/mailu/fullchain.pem",
        "/certs/letsencrypt/live/mailu/privkey.pem"),
    "notls": None
}[args["TLS_FLAVOR"]]

if args["TLS"] and not all(os.path.exists(file_path) for file_path in args["TLS"]):
    print("Missing cert or key file, disabling TLS")
    args["TLS_ERROR"] = "yes"

# Build final configuration paths
conf.jinja("/conf/tls.conf", args, "/etc/nginx/tls.conf")
conf.jinja("/conf/proxy.conf", args, "/etc/nginx/proxy.conf")
conf.jinja("/conf/nginx.conf", args, "/etc/nginx/nginx.conf")
if os.path.exists("/var/run/nginx.pid"):
    os.system("nginx -s reload")
