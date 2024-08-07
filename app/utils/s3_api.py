import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


class S3Api:
    def __init__(self,
                 region: str,
                 access_key: str,
                 secret_key: str,
                 endpoint: str,
                 bucket: str
                 ):
        self.session = boto3.Session(
            profile_name='default'
        )
        self.client = self.session.client(
            service_name='s3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint,
        )
        self.bucket = self.session
        self.s3_bucket = bucket

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
        return self.client.put_object(Bucket=self.s3_bucket, Key=key, Body=body, ContentType='image/png')

    def list(self):
        return self.client.list_objects(Bucket=self.s3_bucket)['Contents']

    def delete(self, key: str):
        return self.client.delete_object(Bucket=self.s3_bucket, Key=key)

    def upload(self, file_path: str, key: str):
        return self.client.upload_file(Filename=file_path, Bucket=self.s3_bucket, Key=key)
