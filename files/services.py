import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "user-files"

s3_client = boto3.client('s3',
                         endpoint_url='http://localhost:9000',
                         aws_access_key_id='minioadmin',
                         aws_secret_access_key='minioadmin'
                         )
def init_storage():
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError:
        s3_client.create_bucket(Bucket=BUCKET_NAME)

def get_user_folder(user_id):
    return f"user-{user_id}-files/"

def list_files(get_id, path):
    prefix = get_user_folder(get_id) + path
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME,
                                         Prefix=prefix,
                                         Delimiter='/')
    folders = []
    files = []
    for prefix_obj in response.get('CommonPrefixes', []):
        folder_name = prefix_obj["Prefix"].replace(prefix, '').strip('/')
        folders.append(folder_name)
    for obj in response.get("Contents", []):
        file_key = obj["Key"]
        file_name = file_key.replace(prefix, "")
        if file_name:
            files.append({
                'name': file_name,
                'size':obj["Size"],
                "key": file_key
            })
    return folders, files