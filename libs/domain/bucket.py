import boto3
class Bucket():
    def __init__(self, access_key, secret_key, name, region='us-west-1'):
        self.access_key_id = access_key
        self.secret_access_key = secret_key
        self.bucket_name = name
        self.region_name = region


    def set_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name='us-west-1'
        )
    


