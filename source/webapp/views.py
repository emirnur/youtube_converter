import sys
from datetime import datetime
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.forms import DownloadForm
from webapp.models import Download
from .tasks import convert_load, mail_sending


def index(request):
    if request.POST:
        form = DownloadForm(request.POST)
        if form.is_valid():
            video_url = str(form.cleaned_data.get('link'))
            email = form.cleaned_data.get('email')
            try:
                name = convert_load(video_url)
                mail_sending(email, name)
                f = Download(url=video_url, email=email)
                f.save()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Type:{} Filename:{} Line:{}ERROR: {}'.
                      format(exc_type, fname, exc_tb.tb_lineno, e))

            return HttpResponseRedirect('/')
    else:
        form = DownloadForm()
    return render(request, 'index.html', {'form': form})







