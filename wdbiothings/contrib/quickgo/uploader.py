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


class QuickgoUploader(uploader.BaseSourceUploader):
    name = "quickgo"
    main_source = "quickgo"

    def load_data(self, data_folder):
        self.data_folder = data_folder
        df_iter = pd.read_csv(os.path.join(data_folder, "quickgo.tsv.gz"), sep='\t', iterator=True, chunksize=10000)
        for df in df_iter:
            df = df.query("Evidence != 'ND'")
            del df['With']
            del df['Symbol']
            del df['GO Name']
            del df['Date']
            for _, x in df.iterrows():
                yield x.to_dict()

    def post_update_data(self):
        print("done uploading quickgo")
        src_doc = self.src_dump.find_one({'_id': "quickgo"})
        release = src_doc.get("release", "")
        print(release)

        params = {'token': JENKINS_TOKEN,
                  'job': 'quickgo',
                  'release': release
                  }
        url = JENKINS_URL + "buildByToken/buildWithParameters"
        r = requests.get(url, params=params)

    @classmethod
    def get_mapping(cls):
        return {}
