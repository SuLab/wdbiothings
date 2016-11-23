import biothings.dataload.uploader as uploader
import requests
from wdbiothings import config

from .parser import parse_interpro_xml, parse_release_info, parse_protein_ipr
from wdbiothings.local import JENKINS_TOKEN, JENKINS_URL

DEBUG = False

class InterproUploader(uploader.BaseSourceUploader):
    name = "interpro"
    main_source = "interpro"

    def load_data(self, data_folder):
        self.data_folder = data_folder
        return parse_interpro_xml(data_folder)

    def post_update_data(self):
        print("done uploading interpro")

    @classmethod
    def get_mapping(cls):
        return {}


class InterproProteinUploader(uploader.BaseSourceUploader):
    name = "interpro_protein"
    main_source = "interpro"

    def load_data(self, data_folder):
        self.data_folder = data_folder
        ipr_items = parse_interpro_xml(data_folder)
        ipr_items = {x['_id']: x for x in ipr_items}
        p = parse_protein_ipr(data_folder, ipr_items, debug=DEBUG)
        return p

    def post_update_data(self):
        print("done uploading interpro_protein")
        release_info = list(parse_release_info(self.data_folder))
        interpro_release_info = [x for x in release_info if x['_id'] == "INTERPRO"][0]
        date = interpro_release_info['file_date']
        version = interpro_release_info['version']

        # TODO: check that interpro upload is completed

        params = {'token': JENKINS_TOKEN,
                  'INTERPROVERSION': version,
                  'INTERPRODATE': date,
                  'job': 'interpro'
                  }
        url = JENKINS_URL + "buildByToken/buildWithParameters"
        r = requests.get(url, params=params)

    @classmethod
    def get_mapping(cls):
        return {}


def upload_log(file_path):
    import requests
    url = "http://{}:{}/uploadPOST/".format(config.LOGGING_HOST, config.LOGGING_PORT)
    data = open(file_path).read()
    r = requests.post(url, data=data)