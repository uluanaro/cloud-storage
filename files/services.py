import boto3
from botocore.exceptions import ClientError
from decouple import config

BUCKET_NAME = "user-files"

s3_client = boto3.client('s3',
                         endpoint_url=config('MINIO_ENDPOINT'),
                         aws_access_key_id=config('MINIO_ACCESS_KEY'),
                         aws_secret_access_key=config('MINIO_SECRET_KEY')
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

def upload_file(user_id, path, file):
    key = get_user_folder(user_id)+ path + file.name
    s3_client.upload_fileobj(file, BUCKET_NAME, key)

def delete_file(user_id, key):
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)

def create_folder(user_id, path, folder_name):
    key = get_user_folder(user_id)+ path + folder_name + "/"
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=b"")

def get_download_url(key, expires=3600):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
        ExpiresIn=expires
    )
    return url


