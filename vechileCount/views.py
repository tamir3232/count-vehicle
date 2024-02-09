from django.shortcuts import render
import cv2
from django.http import HttpResponse
import numpy as np
import glob
import base64
from vehicle_detector import VehicleDetector

def landing(request):
    return render(request, 'landingpage.html')

def daftar(request):
    return render(request, 'daftar.html')

def home(request):
    return render(request, 'home.html')

def history(request):
    data = [
        {'No': 1, 'Tanggal': '2022-02-09', 'Jam': '12:30', 'Status': 'Lancar'},
        {'No': 2, 'Tanggal': '2022-02-09', 'Jam': '13:45', 'Status': 'Padat'},
        # Add more data as needed
    ]

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

    return render(request, 'home.html', {'prediction': status, 'count': vehicle_count, 'image_data': image_data})
