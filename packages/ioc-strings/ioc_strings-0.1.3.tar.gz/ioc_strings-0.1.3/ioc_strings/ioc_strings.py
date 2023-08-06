import os
import sys
import subprocess
import argparse
import string
import requests
import json
import multiprocessing

import iocextract
import validators


global CPU_COUNT
global LOCK
CPU_COUNT = multiprocessing.cpu_count()
LOCK = multiprocessing.Lock()


class IOC:

    def __init__(self, ioc, args):
        self.ioc = ioc.strip()
        self.ioc_types = []

        self.tld_path = "tlds-alpha-by-domain.txt"
        self.tld_url = "http://data.iana.org/TLD/{}".format(self.tld_path)
        self.tlds = self.init_tld()
        self.shared_ioc_attributes()

        check_functions = [
            self.check_ip,
            self.check_domain,
            self.check_file,
            self.check_hash,
            self.check_url,
            self.check_email
        ]

        for check in check_functions:
            result = check(ioc)
            if result:
                self.ioc_types.append(result)

        self.data = {self.ioc: self.ioc_types}

        if args["filter"]:
            if not args["filter"] in self.ioc_types:
                return

        with LOCK:
            if args["t"] and self.is_ioc():
                print(json.dumps(self.data))
            elif not args["t"] and self.is_ioc():
                print(self.ioc)

    def init_tld(self):
        try:
            resp = requests.get(self.tld_url)
        except:
            return False

        tld_data = resp.text

        # Filter out commented lines
        tlds = []
        for tld in tld_data.split("\n"):
            if len(tld) == 0:
                continue

            if tld[0] == "#":
                continue

            tld = tld.strip().lower()
            tlds.append(tld)

        return tlds

    def shared_ioc_attributes(self):
        self.ioc_tld = self.ioc.split(".")[-1]

    def is_ioc(self):
        if len(self.ioc_types) != 0:
            return True
        else:
            return False

    def check_domain(self, ioc):

        # Must contain "."
        if "." not in ioc:
            return False

        # No two dots allowed in row
        if ".." in ioc:
            return False

        if len(ioc.split(".")[0]) == 0:
            return False

        # Check it containts only allowed chars
        allowed_chars = string.ascii_lowercase + string.digits + ".-"
        for char in ioc:
            if char not in allowed_chars:
                return False

        # check if ioc tld is included in all existing tlds
        if self.tlds and self.ioc_tld not in self.tlds:
            return False

        return "domain"

    def check_email(self, ioc):
        ioc = ioc.lower()

        if self.tlds and self.ioc_tld not in self.tlds:
            return False

        result1 = validators.email(ioc)

        if not result1:
            return False

        result2 = iocextract.extract_emails(ioc, refang=True)

        if not result2:
            return False

        return "email"

    def check_ip(self, ioc):
        ioc = ioc.lower()

        result4_1 = validators.ip_address.ipv4(ioc)
        result6_1 = validators.ip_address.ipv6(ioc)

        if not result4_1 and not result6_1:
            return False

        result4_2 = list(iocextract.extract_ipv4s(ioc, refang=True))
        result6_2 = list(iocextract.extract_ipv6s(ioc))

        if not result4_2 and not result6_2:
            return False

        return "ip"

    def check_url(self, ioc):
        result1 = validators.url(ioc)

        if not result1:
            return False

        result2 = list(iocextract.extract_urls(ioc, refang=True))

        if not result2:
            return False

        return "url"

    def check_file(self, ioc):
        if os.path.isfile(ioc):
            return "file"
        
        return False

    def check_hash(self, ioc):
        ioc = ioc.lower()

        if len(ioc) % 8 != 0:
            return False

        # Check it containts only allowed hexadecimal chars
        allowed_chars = "0123456789abcdef"
        for char in ioc:
            if char not in allowed_chars:
                return False

        if not any(char in ioc for char in allowed_chars):
            return False

        result = list(iocextract.extract_hashes(ioc))

        if not result:
            return False

        return "hash"
        

def run_strings(args, filepath):
    strings = subprocess.check_output(["strings", "-n", str(args["n"]), filepath])
    strings = str(strings, "utf-8").split("\n")

    strings_by_whitespace = []
    for s in strings:
        for s_by_whitespace in s.split():
            if len(s_by_whitespace) >= args["n"]:
                strings_by_whitespace.append(s_by_whitespace)

    return strings_by_whitespace


def handle_filepath(args, filepath):
    strings = run_strings(args, filepath)
    for s in strings:
        s = s.strip()
        ioc = IOC(s, args)


def main():
    parser = argparse.ArgumentParser(description="Get IOC types from file")
    parser.add_argument("filepath", help="Path to file or folder containing files")
    parser.add_argument("-n", help="Locate & print any NUL-terminated sequence of at least [number] characters (default 10)", default=10)
    parser.add_argument("-t", help="Output as JSON with IOC types", action="store_true", default=False)
    parser.add_argument("--filter", help="Filter by type (ip, domain, url, file, hash, email)")
    parser.add_argument("--singleprocess", help="Use single process instead of multiprocessing", action="store_true", default=False)
    args = vars(parser.parse_args())

    if not os.path.exists(args["filepath"]):
        print("Path {} does not exist.".format(args["filepath"]))
        exit()

    if os.path.isfile(args["filepath"]):
        filepaths = [args["filepath"]]
    else:
        filepaths = []
        for root, subdir, filenames in os.walk(args["filepath"]):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                filepaths.append(filepath)

    if not args["singleprocess"]:
        file_count = 0
        filepaths_amount = len(filepaths)
        while True:
            if file_count == filepaths_amount and len(multiprocessing.active_children()) == 0:
                break

            if len(multiprocessing.active_children()) < CPU_COUNT and file_count != filepaths_amount:
                filepath = filepaths[file_count]
                p = multiprocessing.Process(target=handle_filepath, args=(args, filepath))
                p.start()
                file_count += 1
    else:
        for filepath in filepaths:
            handle_filepath(args, filepath)


if __name__ == "__main__":
    main()