import face_recognition
import base64
from db_queries.db_functions import find_one
import io
from s3_aws import load_model


def create_encoding_for_daily_uploads(class_name, curr_date):
    """
    fetch all of the pictures of today attendance for current class in current date.
    for each picture in curr_date attendance:
        1.decode it from base 64 back to bytes array
        2.transform to numpy array using face-recognition library
        3.decode the face locations using face-recognition library
        4.push it to the clean array

    :param class_name: name of the current class
    :param curr_date: the date to fetch
    :return: clean array containing 128-dimension face encoding for each valid picture.
    """
    today_pictures_array = find_one('attendance', {"class_name": class_name, "date": curr_date})["images"]
    encoding_today_imgs = []
    for img in today_pictures_array:
        image = base64.b64decode(img)
        un_known_image = face_recognition.load_image_file(io.BytesIO(image))
        un_known_encoding = face_recognition.face_encodings(un_known_image)
        if len(un_known_encoding):
            # if the method recognized at least one face
            encoding_today_imgs.append(un_known_encoding[0])
    return encoding_today_imgs


def get_today_positive_attendance(class_name, curr_date):
    daily_encoded_images = create_encoding_for_daily_uploads(class_name, curr_date)
    model = load_model(f'svm_pkl_{class_name}')
    known_ids_for_today = model.predict(daily_encoded_images)
    return list(set(known_ids_for_today))


print(get_today_positive_attendance('test1', '19/07/2022'))


