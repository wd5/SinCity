from django.core.management import setup_environ
import settings

from urllib import urlopen

from StringIO import StringIO

from django.core.files.uploadedfile import UploadedFile

setup_environ(settings)

from core.models import Profile

class F(StringIO):
	pass

for photo in Profile.objects.all():
    try:
        if photo.photo and not photo.portrait:
            url = "http://sincity2012.ru/media/%s" % photo.photo
            print photo.id, url

            content = urlopen(url).read()

            file = F(content)
            file.name = str(photo.photo)
            file.size = 1
            file.file = content

            photo.portrait.save('image', file)
            photo.save()
    except:
        pass
