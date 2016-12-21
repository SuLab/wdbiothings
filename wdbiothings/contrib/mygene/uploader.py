import json
import os

import biothings.dataload.uploader as uploader
import requests
from wdbiothings.local import JENKINS_TOKEN, JENKINS_URL

class MyGeneUploader(uploader.BaseSourceUploader):
    name = "mygene"
    main_source = "mygene"

    def load_data(self, data_folder):
        with open(os.path.join(data_folder, "mygene.json")) as f:
            d = json.load(f)
            for doc in d:
                yield doc

    def post_update_data(self):
        print("done uploading mygene")

        params = {'token': JENKINS_TOKEN,
                  'job': 'GeneBot_yeast'
                  }
        url = JENKINS_URL + "buildByToken/buildWithParameters"
        r = requests.get(url, params=params)

        # TODO add other jobs
        print("job triggered")

    @classmethod
    def get_mapping(cls):
        return {}


class MyGeneSourcesUploader(uploader.BaseSourceUploader):
    name = "mygene_sources"
    main_source = "mygene"

    def load_data(self, data_folder):
        d = requests.get("http://mygene.info/v2/metadata").json()
        for doc in [d['src_version']]:
            yield doc

    @classmethod
    def get_mapping(cls):
        return {}
