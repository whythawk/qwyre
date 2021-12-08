import boto3
from uuid import UUID
import base64
from typing import BinaryIO

from app.core.config import settings
from app.schema_types import ResourceType


class CRUDSpaces:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) DigitalOcean Spaces.

        # https://docs.digitalocean.com/products/spaces/resources/s3-sdk-examples/
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
        """
        self.space = boto3.resource(
            "s3",
            region_name=settings.SPACES_REGION_NAME,
            endpoint_url=settings.SPACES_ENDPOINT_URL,
            aws_access_key_id=settings.SPACES_ACCESS_KEY,
            aws_secret_access_key=settings.SPACES_SECRET_KEY,
        )
        self.bucket = self.space.Bucket(settings.SPACES_BUCKET)

    def get(self, *, filename: str, resource_type: ResourceType) -> BinaryIO:
        # https://stackoverflow.com/a/35376156/295606
        key = f"{resource_type}/{filename}"
        obj = self.bucket.Object(key)
        source = obj.get()["Body"].read().decode("utf-8")
        # Convert base64 to binary
        return base64.b64decode(source)

    def create(self, *, filename: str, resource_type: ResourceType, source: str) -> int:
        key = f"{resource_type}/{filename}"
        obj = self.bucket.Object(key)
        response = obj.put(Body=source)
        return response.get("ResponseMetadata", {}).get("HTTPStatusCode", 400)

    def update(self, *, filename: str, resource_type: ResourceType, source: str) -> int:
        return self.create(filename=filename, resource_type=resource_type, source=source)

    def remove(self, *, filename: str, resource_type: ResourceType) -> int:
        key = f"{resource_type}/{filename}"
        obj = self.bucket.Object(key)
        response = obj.delete()
        return response.get("ResponseMetadata", {}).get("HTTPStatusCode", 400)


spaces = CRUDSpaces()
