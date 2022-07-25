import boto3
import io
import os
import pickle


AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS = os.environ.get("AWS_SECRET_ACCESS")

s3 = boto3.client(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS
)


def add_kid_files(kid_images, kid_id, class_name):
    for k, v in kid_images.items():
        v.seek(0)
        in_memory_file = io.BytesIO(v.read())
        file_type = v.filename.split('.')[-1]
        s3.upload_fileobj(in_memory_file, 'classes-images', f"{class_name}/{kid_id}/{k}.{file_type}")


def delete_kid_from_s3(kid_id, class_name):
    objects_to_delete = s3.list_objects(Bucket="classes-images", Prefix=f"{class_name}/{kid_id}/")
    delete_keys = {'Objects': [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete['Contents']]]}
    s3.delete_objects(Bucket="classes-images", Delete=delete_keys)


def load_model(key):
    pickle_object = s3.get_object(Bucket="pickle-files-models", Key=key)['Body'].read()
    model = pickle.loads(pickle_object)
    return model


if __name__ == '__main__':
    pass

    # setx AWS_SECRET_ACCESS +8h6dHxrEq45v8fGGzqFEc2a+1qbU2qCnD7vTqQC