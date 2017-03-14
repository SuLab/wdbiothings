"""
This solely triggers jenkins job. No parsing, mongo or anything is done here
"""
import biothings.dataload.uploader as uploader
import requests
from local import JENKINS_TOKEN, JENKINS_URL


class PhenocartaGWASUploader(uploader.BaseSourceUploader):
    name = "phenocarta"
    main_source = "phenocarta"
    keep_archive = 1

    def load_data(self, data_folder):
        yield {'_id': 'nothing'}

    def post_update_data(self, *args, **kwargs):
        super().post_update_data(*args, **kwargs)
        release = self.src_doc['release']
        self.logger.info("done uploading phenocarta: {}".format(release))
        print("done uploading phenocarta: {}".format(release))

        job = 'GeneDiseaseBot'
        params = {'token': JENKINS_TOKEN, 'job': job}
        url = JENKINS_URL + "buildByToken/buildWithParameters"
        r = requests.get(url, params=params)
        self.logger.info("job {} triggered: {}".format(job, r.text))

    @classmethod
    def get_mapping(self):
        return {}