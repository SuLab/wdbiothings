import argparse
import datetime
import os

import biothings
from biothings.dataload.dumper import FTPDumper
from wdbiothings import config
from wdbiothings.config import DATA_ARCHIVE_ROOT

biothings.config_for_app(config)

"""
updated every week
Last updated listed here: https://www.ebi.ac.uk/QuickGO/Dataset.html

"""

class QuickgoDumper(FTPDumper):
    SRC_NAME = "quickgo"
    FTP_HOST = "ftp.ebi.ac.uk"
    CWD_DIR = 'pub/databases/GO/goa/UNIPROT'
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    SCHEDULE = "0 2 * * 2"  # “At 02:00 on Tuesday.”


    def create_todump_list(self, force=False):
        self.release = datetime.datetime.now().strftime("%Y%m%d")
        self.to_dump = [{"remote": "goa_uniprot_all.gaf.gz",
                         "local": os.path.join(self.new_data_folder, "goa_uniprot_all.gaf.gz")}]


def main(force=False):
    dumper = QuickgoDumper()
    dumper.create_todump_list()
    dumper.dump(force=force)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run quickgo dumper')
    parser.add_argument('--force', action='store_true', help='force new download')
    args = parser.parse_args()
    main(force=args.force)
