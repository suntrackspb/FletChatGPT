import boto3


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

    def put(self, key: str, body: bytes):
        return self.client.put_object(Bucket=self.s3_bucket, Key=key, Body=body, ContentType='image/png')

    def list(self):
        return self.client.list_objects(Bucket=self.s3_bucket)['Contents']

    def delete(self, key: str):
        return self.client.delete_object(Bucket=self.s3_bucket, Key=key)

    def upload(self, file_path: str, key: str):
        return self.client.upload_file(Filename=file_path, Bucket=self.s3_bucket, Key=key)
