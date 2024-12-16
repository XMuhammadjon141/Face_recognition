import cv2
import face_recognition
import os
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from tkinter import filedialog
import numpy as np

# O'qitilgan yuz ma'lumotlari
known_face_encodings = []
known_face_names = []

# Yangi yuzni kiritish funksiyasi
def add_new_face(name, frame):
    face_encodings = face_recognition.face_encodings(frame)
    if face_encodings:
        face_encoding = face_encodings[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
        return True
    else:
        return False

# Suratga olish funksiyasi
def capture_face(name):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        cv2.imshow('Press Space to Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):  # Space tugmasi bosilganda
            if add_new_face(name, frame):
                cv2.imwrite(f"images/{name}.jpg", frame)
                break
    video_capture.release()
    cv2.destroyAllWindows()

# Yuzni aniqlash jarayonini to'xtatish uchun flag
stop_recognition = False

# Kamera orqali real vaqt mobaynida yuzni aniqlash
def run_face_recognition():
    global stop_recognition
    stop_recognition = False

    video_capture = cv2.VideoCapture(0)

    while not stop_recognition:
        ret, frame = video_capture.read()

        # Rasmni kichraytirish va RGB formatiga o'tkazish
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Yuzlarni aniqlash va kodlash
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Aniqlangan yuzlarni tanish va nomini chiqarish
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Yuqori kadr hajmini tiklash
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Yuqori, o'ng, pastki va chap xududlarni aniqlash
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        # Oyna chiqarish
        cv2.imshow('Video', frame)

        # 'q' tugmasi bosilganda chiqish
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def stop_face_recognition():
    global stop_recognition
    stop_recognition = True

def gen(camera):
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break
        # Yuzni aniqlash va video tasvirni qaytarish
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

def video_feed(request):
    camera = cv2.VideoCapture(0)
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')

def face(request):
    return render(request, 'index.html')

def add_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if 'capture' in request.FILES:
            frame = request.FILES['capture']
            frame = face_recognition.load_image_file(frame)
            if add_new_face(name, frame):
                return JsonResponse({'status': 'success', 'message': f"{name} muvaffaqiyatli qo'shildi!"})
            else:
                return JsonResponse({'status': 'error', 'message': 'Yuz aniqlanmadi.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Iltimos, suratni yuboring.'})
    return render(request, 'add_user.html')
