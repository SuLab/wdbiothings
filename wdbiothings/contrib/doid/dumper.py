"""
Checks github for a new release. If exists, triggers jenkins job passing the release data (string) as a param
Doesn't do anything else
"""
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
    """

    :return: str
    """
    url = "https://api.github.com/repos/DiseaseOntology/HumanDiseaseOntology/contents/src/ontology/releases"
    res = requests.get(url).json()
    latest_release = max(res, key=lambda x: datetime.strptime(x['name'], '%Y-%m-%d'))['name']
    return latest_release


class DoidDumper(HTTPDumper):
    SRC_NAME = "doid"
    SRC_ROOT_FOLDER = DATA_ARCHIVE_ROOT
    SCHEDULE = "0 4 * * 0"

    def __init__(self, src_name=None, src_root_folder=None, no_confirm=True, archive=True):
        super().__init__(src_name, src_root_folder, no_confirm, archive)
        self.latest_release = get_latest_release()
        self.curr_release = self.src_doc.get("release", "")

    def create_todump_list(self, force=False):
        if force or (self.latest_release != self.curr_release):
            print("Downloading DOID: {}".format(self.latest_release))
            self.logger.info("Downloading DOID: {}".format(self.latest_release))
            self.release = self.latest_release
            self.to_dump = [{'remote': 'http://purl.obolibrary.org/obo/doid/releases/{}/doid.owl'.format(self.latest_release),
                             'local': os.path.join(self.new_data_folder, "doid/doid.owl")}]
        else:
            print("Skipping DOID: {}".format(self.latest_release))
            self.logger.info("Skipping DOID: {}".format(self.latest_release))


def main(force=False):
    dumper = DoidDumper()
    dumper.dump(force=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run doid dumper')
    parser.add_argument('--force', action='store_true', help='force new download')
    args = parser.parse_args()
    main(force=args.force)
