from django.shortcuts import render
import cv2
from django.http import HttpResponse
import numpy as np
import glob
from vehicle_detector import VehicleDetector

def index(request):
    return render(request,'index.html')

def count(request):
    status = "Tidak Padat"

    # Load Veichle Detector
    vd = VehicleDetector()

    # Load images from a folder
    # images_data = request.files['image'].read() 
    image_file = request.FILES.get('image')
    if image_file:
            # Membaca data gambar
            images_data = image_file.read()

            # Menggunakan OpenCV untuk membaca gambar
            nparr = np.frombuffer(images_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Load Veichle Detector
            vd = VehicleDetector()

            # Deteksi kendaraan pada gambar
            vehicle_boxes = vd.detect_vehicles(img)
            vehicle_count = len(vehicle_boxes)
            
            if vehicle_count>10:
                status ="Padat"

            print("Total current count", vehicle_count)

            return render(request,'hasil.html', {'prediction' : status, 'count': vehicle_count})
        
    return HttpResponse("<h1>Formulir tidak dikirim dengan metode POST atau file gambar tidak ada</h1>")



    # # Loop through all the images
    # print("Img path", images_data)
    # img = cv2.imread(images_data)

    # vehicle_boxes = vd.detect_vehicles(img)
    # vehicle_count = len(vehicle_boxes)
    # print(vehicle_count)
    # Update total count
    # vehicles_folder_count += vehicle_count

    # for box in vehicle_boxes:
    #     x, y, w, h = box

    #     cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)

    #     cv2.putText(img, "Vehicles: " + str(vehicle_count), (20, 50), 0, 2, (100, 200, 0), 3)


    print("Total current count", vehicle_count)