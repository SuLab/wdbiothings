import argparse
import os
import os.path

import biothings
from biothings.dataload.dumper import HTTPDumper

from wdbiothings import config
from wdbiothings.config import DATA_ARCHIVE_ROOT

biothings.config_for_app(config)


class QuickgoDumper(HTTPDumper):
    SRC_NAME = "quickgo"
    SCHEDULE = "* 0 * * *"




def main(force=False):
    dumper = QuickgoDumper()
    dumper.dump(force=False)
    dumper.create_todump_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run interpro dumper')
    parser.add_argument('--force', action='store_true', help='force new download')
    args = parser.parse_args()
    main(force=args.force)
