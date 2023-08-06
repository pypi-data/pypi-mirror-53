from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import logging
import boto3


class LibraryComponent(object):

    def __init__(self, state):
        self.state = state
        self.dev_logger = logging.getLogger(__name__)
        self.rb_logger = logger
        self._builtin = BuiltIn()

    def get_resource(self, region, service, endpoint_url):
        resource = boto3.resource(service,
            region_name=region,  # noqa: E128, E261
            endpoint_url=endpoint_url
        )
        return resource