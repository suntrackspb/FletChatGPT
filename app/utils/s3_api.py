import os

import flet as ft

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


class S3Api:
    def __init__(self, page: ft.Page):
        self.page = page
        self.s3_region_name = self.page.client_storage.get('S3_REGION')
        self.s3_access_token = self.page.client_storage.get('S3_ACCESS')
        self.s3_secret_token = self.page.client_storage.get('S3_SECRET')
        self.s3_endpoint_url = self.page.client_storage.get('S3_ENDPOINT')
        self.s3_bucket_name = self.page.client_storage.get('S3_BUCKET')

        self.session = None
        self.client = None

        self.validate_config()

    def validate_config(self):
        if bool(self.s3_region_name) and bool(self.s3_access_token) and bool(self.s3_secret_token) and bool(
                self.s3_endpoint_url) and bool(self.s3_bucket_name):
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
            # print("CLIENT SETTINGS")
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
            # print("SERVER SETTINGS")

    def bucket_list(self):
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

    def put(self, key: str, body: bytes):
        return self.client.put_object(Bucket=self.s3_bucket_name, Key=key, Body=body, ContentType='image/png')

    def list(self):
        return self.client.list_objects(Bucket=self.s3_bucket_name)['Contents']

    def delete(self, key: str):
        return self.client.delete_object(Bucket=self.s3_bucket_name, Key=key)

    def upload(self, file_path: str, key: str):
        return self.client.upload_file(Filename=file_path, Bucket=self.s3_bucket_name, Key=key)
