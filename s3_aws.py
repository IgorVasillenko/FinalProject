import boto3
import io
import pickle


s3 = boto3.client(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id='AKIA4ORIKOGWWWIRAUTS',
    aws_secret_access_key='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'
)


def add_kid_files(kid_images, kid_id, class_name):
    for k, v in kid_images.items():
        v.seek(0)
        in_memory_file = io.BytesIO(v.read())
        file_name = v.filename
        s3.upload_fileobj(in_memory_file, 'classes-images', f"{class_name}/{kid_id}/{file_name}")


def delete_kid_from_s3(kid_id, class_name):
    s3.delete_object(Bucket='classes-images', Key=f'{class_name}/{kid_id}')


def edit_kid_images(kid_images, kid_id, class_name):
    delete_kid_from_s3(kid_id, class_name)
    add_kid_files(kid_images, kid_id, class_name)


def load_model(key):
    pickle_object = s3.get_object(Bucket="pickle-files-models", Key=key)['Body'].read()
    model = pickle.loads(pickle_object)

    return model


