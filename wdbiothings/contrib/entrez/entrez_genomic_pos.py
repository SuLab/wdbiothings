import glob
import os.path
from biothings.utils.common import (dump, loadobj, get_timestamp)
from biothings.utils.dataload import (tab2list, load_start, load_done)
import biothings.dataload.uploader as uploader

class EntrezGenomicPosEukUploader(uploader.MergerSourceUploader):
    name = "entrez_genomic_pos_euk"
    main_source = "entrez"

    def load_data(self, data_folder):
        """

        """

        files = glob.glob(os.path.join(data_folder, "*.genomic_pos"))

        for file in files:
            parse_file


def parse_file(file):
    d = {}
    f = open(file)
    for line in f:
        entrez_id = line.split(";", 1)[0].strip()
        d[entrez_id] = [dict(zip(['AnnotationRelease', 'AssemblyAccVer', 'ChrAccVer', 'ChrStart', 'ChrStop'], release.strip().split('\t'))) for release in line.split(';')[1:]]