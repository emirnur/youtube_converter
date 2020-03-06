from __future__ import unicode_literals

import urllib.parse

import youtube_dl
from django.core.mail import send_mail
from celery.task import task



@task
def convert_load(video_url):
    # Mp3 format options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'webapp/static/media/%(title)s.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


    with youtube_dl.YoutubeDL(ydl_opts) as yld:
        file_data = yld.extract_info(video_url)
        print(file_data)
        name = file_data['title']
        # email = file_data['email']

    # mail_sending(email, name)
    return name


# convert_load('https://www.youtube.com/watch?v=iOxzG3jjFkY')


@task
def mail_sending(email, name):
    send_mail(
        'Download link',
        'You can download file from this link: http://127.0.0.1:8000/static/media/{}.mp3'.format(urllib.parse.quote(name)),
        'nur.emirlan@gmail.com',
        [email],
        fail_silently=False
    )

