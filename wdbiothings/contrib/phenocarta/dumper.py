import argparse
import os
import os.path
from datetime import datetime

import biothings
import requests
from biothings.dataload.dumper import HTTPDumper

import config
from config import DATA_ARCHIVE_ROOT

biothings.config_for_app(config)


def get_latest_release():
    url = "https://gemma.msl.ubc.ca/rest/phenotypes/dumps"
    res = requests.get(url).json()
    gwas = [x for x in res if x['name'] == 'GWAS_Catalog'][0]
    latest_release = gwas['modified'].split()[0]
    return latest_release


class PhenocartaGWASDumper(HTTPDumper):
    SRC_NAME = "phenocarta"
    SRC_ROOT_FOLDER = DATA_ARCHIVE_ROOT
    SCHEDULE = "0 4 * * 0"

    def __init__(self, src_name=None, src_root_folder=None, no_confirm=True, archive=True):
        super().__init__(src_name, src_root_folder, no_confirm, archive)
        self.latest_release = get_latest_release()
        self.curr_release = self.src_doc.get("release", "")

    def create_todump_list(self, force=False):
        if force or (self.latest_release != self.curr_release):
            print("Downloading Phenocarta GWAS: {}".format(self.latest_release))
            self.logger.info("Downloading Phenocarta GWAS: {}".format(self.latest_release))
            self.release = self.latest_release
            self.to_dump = [{'remote': 'https://gemma.msl.ubc.ca/phenocarta/LatestEvidenceExport/AnnotationsByDataset/GWAS_Catalog.tsv',
                             'local': os.path.join(self.new_data_folder, "phenocarta/GWAS_Catalog.tsv")}]
        else:
            print("Skipping Phenocarta GWAS: {}".format(self.latest_release))
            self.logger.info("Skipping Phenocarta GWAS: {}".format(self.latest_release))


def main(force=False):
    dumper = PhenocartaGWASDumper()
    dumper.dump(force=force)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run Phenocarta GWAS dumper')
    parser.add_argument('--force', action='store_true', help='force new download')
    args = parser.parse_args()
    main(force=args.force)
