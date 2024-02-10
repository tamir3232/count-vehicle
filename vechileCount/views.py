from django.shortcuts import render,redirect
import cv2
from django.http import HttpResponse
import numpy as np
from datetime import date
import time
import pytz
import glob
import base64
from vehicle_detector import VehicleDetector
from .models import statuscount
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime

def landing(request):
    if request.method == "POST":
       try:
            data = User.objects.create_user(
                username = request.POST['username'],
                email   = request.POST['username'],
                first_name = request.POST['nama'],
                password = request.POST['password1'],
            )
            data.save()
       except IntegrityError:
            error_message = "Username sudah digunakan. Silakan gunakan username lain."
            return render(request, 'daftar.html', {'error_message': error_message})
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'landingpage.html')
    
   

def daftar(request):
    return render(request, 'daftar.html')


@login_required
def home(request):
    # if request.method == "POST" :
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username , password=password )
    #     print(user)
    #     if user is not None:
    #         login(request,user)
    #         return render(request, 'home.html')
    #     else:
    #         error_message = "Username atau Password Salah"
    #         return render(request, 'landingpage.html', {'error_message': error_message})
    # else:
    #     print(request.user)
    return render(request, 'home.html')
    
def base(request):
     if request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username , password=password )
        if user is not None:
            login(request,user)
            return render(request, 'home.html')
        else:
            error_message = "Username atau Password Salah"
            return render(request, 'landingpage.html', {'error_message': error_message})



def history(request):
    data = statuscount.objects.all()
    print(data)

    context = {'datas': data}

    return render(request, 'history.html', context)

def count(request):
    status = "Lancar"
    image_data = None

    # Load Vehicle Detector
    vd = VehicleDetector()

    # Load images from a folder
    image_file = request.FILES.get('image')
    if image_file:
        # Membaca data gambar
        images_data = image_file.read()

        # Menggunakan OpenCV untuk membaca gambar
        nparr = np.frombuffer(images_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Load Vehicle Detector
        vd = VehicleDetector()

        # Deteksi kendaraan pada gambar
        vehicle_boxes = vd.detect_vehicles(img)
        vehicle_count = len(vehicle_boxes)

        if vehicle_count > 10:
            status = "Padat"

        # Encode the image to base64
        _, buffer = cv2.imencode('.png', img)
        image_data = base64.b64encode(buffer).decode('utf-8')
        jakarta_timezone = pytz.timezone('Asia/Jakarta')
        # Ambil waktu saat ini dalam UTC
        utc_time = datetime.utcnow()
        # Konversi waktu UTC ke waktu di Jakarta
        jakarta_time = utc_time.replace(tzinfo=pytz.utc).astimezone(jakarta_timezone)
        # Format waktu dalam jam:menit:detik
        timee = jakarta_time.strftime("%H:%M:%S")
        
        today = date.today()
        formatted_date = today.strftime('%Y-%m-%d')
        data = statuscount.objects.create(
                Date    = formatted_date,
                Time    = timee,
                count   = vehicle_count,
                Status  = status,)
        
        return render(request, 'home.html', {'prediction': status, 'count': vehicle_count, 'image_data': image_data})

    



def logoutt(request):
    if request.method =="GET":
        logout(request)
        return redirect('landing')