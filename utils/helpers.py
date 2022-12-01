import requests

from jobs.models import Courses

endpoint = f"https://assessbk.afexats.com/api/assessment/application-type"

def course_create_assessment_server(course_title, course_desc, course_uid):
    data = {
        'title': course_title,
        'description': course_desc,
        'uid': course_uid
    }
    response = requests.post(url=endpoint, json=data)

def course_update_assessment_server(course_uid, course_title, course_desc):

    course_uid = self.kwargs['uid']
    data = {
        'uid': str(course_uid),
        'title': course_title,
        'description': course_desc
    }

    get_response = requests.put(url=endpoint + f"/{course_uid}", json=data)
    return get_response


def course_delete_assessment_server(is_deleted, course_uid):

    data = {
        'is_delete': is_deleted
    }
    application_type = requests.delete(url=endpoint + f"/{course_uid}", data=data)
    return application_type
