import os
from datetime import datetime

import biothings
import requests
from biothings.dataload.dumper import HTTPDumper
from wdbiothings import config
from wdbiothings.config import DATA_ARCHIVE_ROOT

biothings.config_for_app(config)
"""
TODO: This is using v2 of mygene api which has a bug that doesn't cap the size limit...
Not sure if it'll work once I'm requesting 150 microbial genomes also
"""

class HTTPDumperParams(HTTPDumper):
    """
    subclass httpdumper so I can make a GET request with params
    """

    def download(self, remoteurl, localfile):
        self.prepare_local_folders(localfile)
        self.logger.debug("Downloading '%s'" % remoteurl)
        res = self.client.get(remoteurl, stream=True, params=self.params)
        fout = open(localfile, 'wb')
        for chunk in res.iter_content(chunk_size=512 * 1024):
            if chunk:
                fout.write(chunk)
        fout.close()


class MyGeneDumper(HTTPDumperParams):
    SRC_NAME = "mygene"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)
    SCHEDULE = "* 0 * * *"

    taxids = "559292,123,10090,9606"
    params = dict(q="__all__", species=taxids, entrezonly="true", size="1000000",
                  fields="entrezgene,ensembl,locus_tag,genomic_pos,name,symbol,uniprot,refseq,taxid," +
                         "type_of_gene,genomic_pos_hg19,MGI,SGD,HGNC")

    def __init__(self, src_name=None, src_root_folder=None, no_confirm=True, archive=True):
        super().__init__(src_name, src_root_folder, no_confirm, archive)
        print(self.src_doc)
        self.current_timestamp = self.src_doc["release"] if self.src_doc.get('release', False) else None
        print(self.current_timestamp)
        self.new_timestamp = None

    def create_todump_list(self, force=False):
        if force or self.remote_is_newer():
            self.release = datetime.now().strftime("%Y%m%d")
            self.to_dump = [{"remote": 'http://mygene.info/v2/query/',
                             "local": os.path.join(self.new_data_folder, "mygene.json")}]
            self.logger.info(
                "remote ({}) is newer than current ({})".format(self.new_timestamp, self.current_timestamp))
        else:
            self.logger.info(
                "remote ({}) is not newer than current ({})".format(self.new_timestamp, self.current_timestamp))

    def remote_is_newer(self):
        mygene_metadata = requests.get("http://mygene.info/v2/metadata").json()
        self.new_timestamp = mygene_metadata['timestamp']
        if self.current_timestamp is None or self.new_timestamp > self.current_timestamp:
            return True


def main():
    dumper = MyGeneDumper()
    dumper.dump()


if __name__ == "__main__":
    main()
