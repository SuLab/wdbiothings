import os

import biothings.dataload.uploader as uploader
import pandas as pd
import requests
from wdbiothings.local import JENKINS_TOKEN, JENKINS_URL

DEBUG = False
"""
to upload manually
gstupp @ gregLaptop ~ $ ssh guest@localhost -p 8022
Welcome to wikidata hub, guest!
hub> i = um.create_instance(um['quickgo'][0])
hub>
hub> i.post_update_data()

"""
from itertools import chain

# TODO: autogenerate this from WD
all_taxa = '9606,10090,10116,9545,749927,224911,100226,243090,246196,394,266834,366394,559292,272560,160488,1125630,223283,208964,716541,226900,281309,386585,205918,1133852,1028307,585056,243160,223926,226186,568707,585057,295405,685038,251221,220341,99287,272943,214092,1208660,190485,224308,211586,380703,511145,36809,198214,393305,83332,233413,324602,269796,312309,272562,272563,189518,190650,300267,871585,882,243231,243277,257313,226185,169963,243230,333849,272624,309807,243275,441771,93061,5833,220668,176299,176280,197221,264732,402612,388919,300852,194439,413999,272623,208435,289376,365659,190304,210007,568814,122586,167539,243274,272621,227377,171101,206672,160490,242231,177416,71421,192222,272631,224324,196627,85962,321967,525284,224326,115713,272632,362948,272561,471472,702459,272947,265311,260799,272634,107806,198094'
all_taxa = set(['taxon:' + x for x in all_taxa.split(",")])

class QuickgoUploader(uploader.BaseSourceUploader):
    name = "quickgo"
    main_source = "quickgo"
    keep_archive = 1

    def load_data(self, data_folder):
        self.data_folder = data_folder
        # no header... sigh
        names = ['DB', 'ID', 'DB_Object_Symbol', 'Qualifier', 'GO ID', 'Reference', 'Evidence',
                 'With (or) From', 'Aspect', 'DB_Object_Name', 'DB_Object_Synonym', 'DB_Object_Type',
                 'Taxon', 'Date', 'Source', 'Annotation_Extension', 'Gene_Product_Form_ID']
        df_iter = pd.read_csv(os.path.join(data_folder, "goa_uniprot_all.gaf.gz"), sep='\t',
                              iterator=True, chunksize=100000, comment="!", names=names)
        for df in df_iter:
            df = df.query("Evidence != 'ND'")
            df = df[df.Taxon.isin(all_taxa)]
            del df['With (or) From']
            del df['DB_Object_Symbol']
            del df['DB_Object_Name']
            del df['DB_Object_Synonym']
            del df['DB_Object_Type']
            del df['Annotation_Extension']
            del df['Gene_Product_Form_ID']
            del df['Date']
            for _, x in df.iterrows():
                yield x.to_dict()

    def post_update_data(self, *args, **kwargs):
        super().post_update_data(*args, **kwargs)
        self.logger.info("done uploading quickgo")
        src_doc = self.src_dump.find_one({'_id': "quickgo"})
        release = src_doc.get("release", "")

        params = {'token': JENKINS_TOKEN,
                  'job': 'GOProtein_Bot',
                  'RETRIEVED': release
                  }
        url = JENKINS_URL + "buildByToken/buildWithParameters"
        r = requests.get(url, params=params)

        self.logger.info("job triggered: {}".format(r.text))

    @classmethod
    def get_mapping(cls):
        return {}
