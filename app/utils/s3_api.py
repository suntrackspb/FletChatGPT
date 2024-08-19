import os
from typing import Any, Dict, List, Optional, Union

import boto3
import flet as ft
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


class S3Api:
    """
    A class to interact with Amazon S3 using boto3, with configuration from Flet page storage or environment variables.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the S3Api object with configuration from the Flet page storage or environment variables.

        :param page: The Flet page object containing client storage for configuration.
        """
        self.page = page
        self.s3_region_name: Optional[str] = self.page.client_storage.get('S3_REGION')
        self.s3_access_token: Optional[str] = self.page.client_storage.get('S3_ACCESS')
        self.s3_secret_token: Optional[str] = self.page.client_storage.get('S3_SECRET')
        self.s3_endpoint_url: Optional[str] = self.page.client_storage.get('S3_ENDPOINT')
        self.s3_bucket_name: Optional[str] = self.page.client_storage.get('S3_BUCKET')

        self.session: Optional[boto3.Session] = None
        self.client: Optional[boto3.client] = None

        self.validate_config()

    def validate_config(self) -> None:
        """
        Validates and sets up the AWS S3 session and client using either the Flet page storage or environment variables.
        """
        if all([self.s3_region_name, self.s3_access_token, self.s3_secret_token, self.s3_endpoint_url,
                self.s3_bucket_name]):
            self.session = boto3.Session(
                profile_name='default',
                region_name=self.s3_region_name,
                aws_access_key_id=self.s3_access_token,
                aws_secret_access_key=self.s3_secret_token,
            )
            self.client = self.session.client(
                service_name='s3',
                endpoint_url=self.s3_endpoint_url,
            )
        else:
            self.session = boto3.Session(
                profile_name='default',
                region_name=os.getenv('S3_REGION_NAME'),
                aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
                aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
            )
            self.client = self.session.client(
                service_name='s3',
                endpoint_url=os.getenv('S3_ENDPOINT_URL'),
            )
            self.s3_endpoint_url = os.getenv('S3_ENDPOINT_URL')
            self.s3_bucket_name = os.getenv('S3_BUCKET_NAME')

    def bucket_list(self) -> Dict[str, Union[bool, List[str], str]]:
        """
        Lists all buckets in the S3 account.

        :return: A dictionary with success status and either the list of bucket names or an error message.
        """
        try:
            response = self.client.list_buckets()
            return {
                'success': True,
                'data': [x['Name'] for x in response['Buckets']]
            }
        except NoCredentialsError:
            return {
                'success': False,
                'message': 'No credentials found. Please configure your AWS credentials.'
            }
        except PartialCredentialsError:
            return {
                'success': False,
                'message': 'Incomplete credentials found. Please check your AWS credentials.'
            }
        except ClientError as e:
            return {
                'success': False,
                'message': f"Client error: {e}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"An error occurred: {e}"
            }

    def put(self, key: str, body: bytes) -> Dict[str, Any]:
        """
        Puts an object into the specified S3 bucket.

        :param key: The key under which the object will be stored.
        :param body: The content of the object to be stored.
        :return: The response from the S3 client.
        """
        return self.client.put_object(Bucket=self.s3_bucket_name, Key=key, Body=body, ContentType='image/png')

    def list(self) -> List[Dict[str, Any]]:
        """
        Lists objects in the specified S3 bucket.

        :return: The list of objects in the bucket.
        """
        return self.client.list_objects(Bucket=self.s3_bucket_name)['Contents']

    def delete(self, key: str) -> Dict[str, Any]:
        """
        Deletes an object from the specified S3 bucket.

        :param key: The key of the object to delete.
        :return: The response from the S3 client.
        """
        return self.client.delete_object(Bucket=self.s3_bucket_name, Key=key)

    def upload(self, file_path: str, key: str) -> None:
        """
        Uploads a file to the specified S3 bucket.

        :param file_path: The local path to the file to be uploaded.
        :param key: The key under which the file will be stored in the bucket.
        """
        self.client.upload_file(Filename=file_path, Bucket=self.s3_bucket_name, Key=key)
