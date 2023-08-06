from json import loads
from json.decoder import JSONDecodeError
from warnings import warn

from boto3 import Session
from botocore.exceptions import ClientError
from microcosm.metadata import Metadata


class InvalidMetadata(Exception):
    pass


class SecretsManagerLoader:
    def __init__(self,
                 environment=None,
                 profile_name=None,
                 region=None):

        self.environment = environment
        self.profile_name = profile_name
        self.region = region

    def __call__(self, metadata, version=None):
        if not isinstance(metadata, Metadata):
            raise InvalidMetadata("Wrong argument metadata passed into SecretsManagerLoader")

        service = metadata.name
        return self.get_secret_value(service, version)

    def get_secret_value(self, service, version=None):
        keyname = self.keyname(service)
        client = self.make_client(service)

        get_args = dict(
            SecretId=keyname,
        )

        if version:
            get_args.update(
                VersionStage=version,
            )

        try:
            response = client.get_secret_value(
                **get_args,
            )

        except ClientError:
            warn(f"Unable to query configuration for {keyname}: version: {version}")
            raise
        else:
            if "SecretString" in response:
                try:
                    # It's not always valid json.
                    # We initialize with valid JSON but Amazon might send None
                    return loads(response["SecretString"]).get("config", {})
                except JSONDecodeError as e:
                    warn(f"Unable to parse secrets JSON for {keyname}: version: {version}. {e}")
                    raise

    def keyname(self, service):
        """keyname
        Return a key name for secrets manager based on the service
        the service is sometimes underscored for python consistency,
        however for AWS naming we use hyphens

        We want to return the hyphened type here

        :param service:
        """
        _service_name = service.replace("_", "-")
        return f"secrets/{self.environment}/{_service_name}"

    def make_client(self, service):
        session = Session(profile_name=self.profile_name)
        return session.client("secretsmanager")
