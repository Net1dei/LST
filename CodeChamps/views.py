import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from CodeChamps.utils_cv.model import *
from CodeChamps.utils_cv.args import *
import os
import shutil


def send_email(to_email, subject, message):
    from_email = 'carddeck111@outlook.com'
    email_password = 'D20022009D'
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    server.login(from_email, email_password)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server.sendmail(from_email, to_email, msg.as_string())

    server.quit()
    
def show_images():
    image_folder = PATH_TO_SAVE_PREDICTIONS + '/images/'
    image_files = [file for file in os.listdir(image_folder) if file.endswith('.jpg')]
    return image_files

def show_video(request):
    video_file = request.FILES['video_file']
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    filename = fs.save(video_file.name, video_file)
    video_url = fs.path(filename)
    return (video_url, filename)

def zip_images():
    path_folder = PATH_TO_SAVE_PREDICTIONS + '/images/'
    path_zip = PATH_ZIP
    shutil.make_archive(path_zip, 'zip', path_folder)

@ensure_csrf_cookie
def main(request):
    if (len(request.POST.get('rtsp_url', ''))>3) and ('file' in request.POST):
        rtsp_url = request.POST.get('rtsp_url', '')
        analise_stream(rtsp_url)
        images = show_images()
        zip_images()
        return render(request, 'index.html', {'images': images})
    elif 'file' in request.POST:
        video_url, filename = show_video(request)
        analise_video2(video_url)
        images = show_images()
        zip_images()
        if len(images)>0:
            user_email = request.POST.get('user_email', '')
            if len(user_email)==0:
                user_email = 'example@outlook.com'
            subject = 'Обнаружена незаконная продажа'
            message = 'Обнаружена незаконная продажа'
            send_email(user_email, subject, message)
        return render(request, 'index.html', {'filename': filename, 'images': images})
    return render(request, 'index.html')