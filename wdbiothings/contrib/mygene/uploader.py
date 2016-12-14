import json
import os

import biothings.dataload.uploader as uploader
import requests


class MyGeneUploader(uploader.BaseSourceUploader):
    name = "mygene"
    main_source = "mygene"

    def load_data(self, data_folder):
        with open(os.path.join(data_folder, "mygene.json")) as f:
            d = json.load(f)
            for doc in d['hits']:
                yield doc

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
