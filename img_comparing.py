import face_recognition
from db_queries.db_functions import *
import base64
import io
from datetime import datetime


def create_attendance_report(class_name, curr_date):
    """

    :param class_name:
    :param curr_date:


    :return:
    """
    print('STARTING THE REPORT ')
    information_for_db = {}
    unknown_images = create_encoding_unknown_imgs(class_name, curr_date)
    array_of_kids_details = gather_kids_objects_to_array(class_name)
    print("DONE FETCHING IMAGES FOR THE REPORT ")
    for kid in array_of_kids_details:
        print(f"===={kid['first_name']}=====")
        clean_kid_array = create_encoding_kid_imgs(kid)
        attendence_result, index_to_pop = compare_images(clean_kid_array, unknown_images)
        information_for_db[kid["_id"]] = attendence_result
        if attendence_result:
            # if there was a match to this image, remove it from the array
            # in order to prevent further tests on this image.
            unknown_images.pop(index_to_pop)
    now = datetime.now()
    values_to_insert = {"last_update": now, "attendence_report": information_for_db}
    test = update_one(collection='attendance', query={"class_name": class_name, "date": curr_date},
                      newValues=values_to_insert)
    # information_for_db["last_update"] = now
    # test = update_one(collection='attendance', query={"class_name": class_name, "date": curr_date},
    #                   newValues=information_for_db)


def compare_images(kid_images, unknown_images):
    """
    :param kid_images: known images
    :param unknown_images: picture to compare to
    :return: if there was a match -> return True and the index of matched image in unknown_images.
             if there wasn't a match -> return False and none.
    """
    for index, unknown_image in enumerate(unknown_images):
        results = face_recognition.compare_faces(kid_images, unknown_image, tolerance=0.5)
        print(results)
        if any(results):
            print('matched')
            return True, index
    return False, None





def create_encoding_kid_imgs(kid_obj):
    """
    the array the function returns will contain only valid pictures
    where face-recognition library found any face location.

    for each picture of a kid:
        1.decode it from base 64 back to bytes array
        2.transform to numpy array using face-recognition library
        3.decode the face locations using face-recognition library
        4.push it to the clean array

    :param kid_obj: curr kid details to extract pictures from
    :return: clean array containing 128-dimension face encoding for each valid picture.
    """
    curr_encoding_kid_imgs = []
    for i in range(1, 11):
        kid_picture = base64.b64decode(kid_obj[f"picture-{i}"]["img_bytes"])
        file = io.BytesIO(kid_picture)
        known_image = face_recognition.load_image_file(file)
        known_encoding = face_recognition.face_encodings(known_image)
        if len(known_encoding):
            # if the method recognized at least one face
            curr_encoding_kid_imgs.append(known_encoding[0])
    return curr_encoding_kid_imgs


def create_encoding_unknown_imgs(class_name, curr_date):
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
        file = io.BytesIO(image)
        un_known_image = face_recognition.load_image_file(file)
        un_known_encoding = face_recognition.face_encodings(un_known_image)
        if len(un_known_encoding):
            # if the method recognized at least one face
            encoding_today_imgs.append(un_known_encoding[0])
    return encoding_today_imgs


# create_attendance_report('NY morning', "08/05/2022")





