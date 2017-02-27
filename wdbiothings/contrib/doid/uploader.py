"""
This solely triggers jenkins job. No parsing, mongo, anything is done here
"""
import biothings.dataload.uploader as uploader
import requests
from local import JENKINS_TOKEN, JENKINS_URL


class DoidUploader(uploader.BaseSourceUploader):
    name = "doid"
    main_source = "doid"
    keep_archive = 1

    def load_data(self, data_folder):
        yield {'_id': 'nothing'}

    def post_update_data(self, *args, **kwargs):
        super().post_update_data(*args, **kwargs)
        release = self.src_doc['release']
        self.logger.info("done uploading doid: {}".format(release))
        print("done uploading doid: {}".format(release))

        job = 'Disease_Ontology'
        params = {'token': JENKINS_TOKEN, 'job': job,
                  'OWL': "http://purl.obolibrary.org/obo/doid/releases/{}/doid.owl".format(release)}
        url = JENKINS_URL + "buildByToken/buildWithParameters"
        r = requests.get(url, params=params)
        self.logger.info("job {} triggered: {}".format(job, r.text))

    @classmethod
    def get_mapping(self):
        return {}
