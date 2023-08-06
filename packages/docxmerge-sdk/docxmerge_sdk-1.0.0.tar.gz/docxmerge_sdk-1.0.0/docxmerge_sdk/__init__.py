import json

import requests


class Docxmerge:
    def __init__(self, apikey="", tenant="default", host="https://api.docxmerge.com"):
        self.api_key = apikey
        self.base_url = host
        self.http_client = requests.Session()
        self.http_client.headers["api-key"] = apikey
        self.http_client.headers["x-tenant"] = tenant

    def render_template(self, template_name, data, conversion_type, version=""):
        render_template_url = self.base_url + '/api/v1/Admin/RenderTemplate'
        response = self.http_client.post(render_template_url, json={
            'version': version,
            'conversionType': conversion_type,
            'data': data,
            'template': template_name
        })
        if response.status_code == 404:
            raise Exception("Template %s not found" % template_name)
        if response.status_code != 200:
            raise Exception("Bad status code %d" % response.status_code)
        return response.content

    def render_file(self, file, data, conversion_type):
        render_file_url = self.base_url + '/api/v1/Admin/RenderFile'
        dumps = json.dumps(data)
        response = self.http_client.post(render_file_url,
                                         data={
                                             'data': dumps,
                                             'conversionType': conversion_type,
                                         },
                                         files={'file': file}
                                         )
        if response.status_code != 200:
            raise Exception("Bad status code %d" % response.status_code)
        return response.content
