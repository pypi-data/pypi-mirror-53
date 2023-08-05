import os
import mkdocs
import requests

from mkdocs import utils as mkdocs_utils
from mkdocs.config.base import ValidationError
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options, Config


class VersionWarning(BasePlugin):
    BANNER_PLACEHOLDER = '### VERSION-WARNING-BANNER-PLACEHOLDER ###'

    config_scheme = (
        ('show_on_versions', mkdocs.config.config_options.Type((str, list), default=None)),
        ('project_id', config_options.Type(mkdocs_utils.string_types, default=None)),
    )

    def __init__(self):
        self.show_on_versions = None
        self.project_id = None
        self.latest_version = None

    def on_config(self, config):
        self.show_on_versions = self.config['show_on_versions'] or ['latest']
        self.project_id = self.config['project_id']

        if not self.project_id:
            raise ValidationError("No project_id specified.")

        if not isinstance(self.show_on_versions, list):
            self.show_on_versions = [self.show_on_versions]

        return config

    def on_post_page(self, output_content, **kwargs):
        if not self.banner_enabled():
            output_content = output_content.replace(self.BANNER_PLACEHOLDER, '')
            return output_content

        banner_html = """<div class="admonition warning">
            <p>
                <b>You are browsing the latest version of the documentation which is not released yet.
                See the current <a href="#" id="js-stable-version">stable version</a> instead.</b>
            </p>
        </div>
        <script>
            document.getElementById('js-stable-version').href = window.location.href.replace('/{}/', '/{}/');
        </script>
        """.format(os.environ.get("READTHEDOCS_VERSION"), self.get_latest_version())

        output_content = output_content.replace(self.BANNER_PLACEHOLDER, banner_html)

        return output_content

    def banner_enabled(self):
        if os.environ.get("READTHEDOCS") == "True" and os.environ.get("READTHEDOCS_VERSION") in self.show_on_versions:
            return True

        return False

    def get_latest_version(self):
        if self.latest_version:
            return self.latest_version

        api_url = 'https://readthedocs.org/api/v2/project/' + self.project_id + '/active_versions/'
        response = requests.get(api_url)

        json_response = response.json()['versions']

        self.latest_version = json_response[0].get('project').get('default_version')

        return self.latest_version
