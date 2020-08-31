from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt


@csrf_exempt
def upload_image(request, dir_name):
    result = {"error": 1, "message": "upload error"}
    files = request.FILES.get("imgFile", None)
    if files:
        result = image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")


# create dir
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    url_part = dir_name + '/%d/%d/' % (today.year, today.month)
    dir_name = os.path.join(dir_name, str(today.year), str(today.month))
    print("*********", os.path.join(settings.MEDIA_ROOT, dir_name))
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dir_name)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, dir_name))
    return dir_name,url_part


# upload picture
def image_upload(files, dir_name):
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "the picture format is incorrect"}
    relative_path_file, url_part = upload_generation_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    print("&&&&path", path)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url =settings.MEDIA_URL + url_part +file_name
    open(path_file, 'wb').write(files.file.read())
    return {"error": 0, "url": file_url}
