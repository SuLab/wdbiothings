import argparse
import datetime
import os

import biothings
from biothings.dataload.dumper import HTTPDumper
from wdbiothings import config
from wdbiothings.config import DATA_ARCHIVE_ROOT

biothings.config_for_app(config)

"""
updated every week
Last updated listed here: https://www.ebi.ac.uk/QuickGO/Dataset.html

"""

# todo: get the taxa to download from wikidata
"""
def get_all_taxa():
    # get all taxa with a uniprot protein
    # http://tinyurl.com/hkdwzq9
    query = \"""SELECT ?t
    {	?a	wdt:P352	?p	; wdt:P703	?t}
    GROUP BY ?t
    \"""
    result = wdi_core.WDItemEngine.execute_sparql_query(query=query)
    taxa = set([x['t']['value'].replace("http://www.wikidata.org/entity/","")  for x in result['results']['bindings']])
    return taxa
"""


class HTTPPostDumper(HTTPDumper):
    """
    subclass httpdumper so I can make a POST request
    """
    data = {}

    def download(self, remoteurl, localfile, headers={}):
        """kwargs will be passed to requests.Session.get()"""
        self.prepare_local_folders(localfile)
        self.logger.debug("Downloading '%s'" % remoteurl)
        res = self.client.post(remoteurl, stream=True, headers=headers, data=self.data)
        fout = open(localfile, 'wb')
        for chunk in res.iter_content(chunk_size=512 * 1024):
            if chunk:
                fout.write(chunk)
        fout.close()


class QuickgoDumper(HTTPPostDumper):
    SRC_NAME = "quickgo"
    SCHEDULE = "0 2 * * 2"  # “At 02:00 on Tuesday.”
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)
    all_taxa = '9606,10090,10116,9545,749927,224911,100226,243090,246196,394,266834,366394,559292,272560,160488,1125630,223283,208964,716541,226900,281309,386585,205918,1133852,1028307,585056,243160,223926,226186,568707,585057,295405,685038,251221,220341,99287,272943,214092,1208660,190485,224308,211586,380703,511145,36809,198214,393305,83332,233413,324602,269796,312309,272562,272563,189518,190650,300267,871585,882,243231,243277,257313,226185,169963,243230,333849,272624,309807,243275,441771,93061,5833,220668,176299,176280,197221,264732,402612,388919,300852,194439,413999,272623,208435,289376,365659,190304,210007,568814,122586,167539,243274,272621,227377,171101,206672,160490,242231,177416,71421,192222,272631,224324,196627,85962,321967,525284,224326,115713,272632,362948,272561,471472,702459,272947,265311,260799,272634,107806,198094'
    data = {'tax': all_taxa, 'format': 'tsv', 'gz': 'true', 'limit': '-1'}

    def create_todump_list(self, force=False):
        self.release = datetime.datetime.now().strftime("%Y%m%d")
        self.to_dump = [{"remote": 'https://www.ebi.ac.uk/QuickGO/GAnnotation',
                         "local": os.path.join(self.new_data_folder, "quickgo.tsv.gz")}]


def main(force=False):
    dumper = QuickgoDumper()
    dumper.dump(force=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run quickgo dumper')
    parser.add_argument('--force', action='store_true', help='force new download')
    args = parser.parse_args()
    main(force=args.force)
