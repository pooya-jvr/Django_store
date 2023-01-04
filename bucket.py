import boto3
from django.conf import settings
import logging
from botocore.exceptions import ClientError


class Bucket:
    """CDN Bucket Manager


    init method creates connection.
    """
    def __init__ (self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name = settings.AWS_SERVICE_NAME,
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url = settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None



    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True


    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)


    def upload_object(self, key):
        logging.basicConfig(level=logging.INFO)

        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

        except Exception as exc:
            logging.error(exc)
        else:
            try:
                bucket = s3_resource.Bucket('bucket-name')
                file_path = 'the/abs/path/to/file.txt'
                object_name = 'file.txt'

                with open(file_path, "rb") as file:
                    bucket.put_object(
                        ACL='private',
                        Body=file,
                        Key=object_name
                    )
            except ClientError as e:
                logging.error(e)

bucket = Bucket()