
from argparse import ArgumentParser
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def main(args):
    p = ArgumentParser("calls the getText API function for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--padinfo", default=".etherpump/settings.json", help="settings, default: .etherdump/settings.json")
    p.add_argument("--showurl", default=False, action="store_true")
    p.add_argument("--format", default="text", help="output format, can be: text, json; default: text")
    args = p.parse_args(args)

    with open(args.padinfo) as f:
        info = json.load(f)
    apiurl = info.get("apiurl")
    # apiurl = "{0[protocol]}://{0[hostname]}:{0[port]}{0[apiurl]}{0[apiversion]}/".format(info)
    data = {}
    data['apikey'] = info['apikey']
    data['padID'] = args.padid # is utf-8 encoded
    requesturl = apiurl+'deletePad?'+urlencode(data)
    if args.showurl:
        print (requesturl)
    else:
        results = json.load(urlopen(requesturl))
        if args.format == "json":
            print (json.dumps(results))
        else:
            if results['data']:
                print (results['data']['text'].encode("utf-8"))
