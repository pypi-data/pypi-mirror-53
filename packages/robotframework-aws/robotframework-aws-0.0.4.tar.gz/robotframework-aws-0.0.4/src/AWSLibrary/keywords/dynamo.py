from AWSLibrary.base.robotlibcore import keyword
from AWSLibrary.base import LibraryComponent, KeywordError, ContinuableError
from botocore.exceptions import ClientError
from robot.api import logger
import botocore


class DynamoDB(LibraryComponent):

    @keyword
    def dynamo_query(self, region, endpoint_url):
        resource = self.get_resource(region, 'dynamodb', endpoint_url)
        print(resource)