# views.py
import cv2
import face_recognition
from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import UserData
from django.core.files.storage import FileSystemStorage
import numpy as np
user = UserData.objects.filter(name='Muhammadjon').first()
print(user.id)
# Yuzlarni aniqlash uchun global ro'yxatlar
known_face_encodings = []
known_face_names = []

# Yangi yuzni qo'shish
def add_new_face(name, frame):
    face_encodings = face_recognition.face_encodings(frame)
    if face_encodings:
        face_encoding = face_encodings[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

        # Yuzni bazaga saqlash
        user_face = UserData.objects.create(
            name=name,
            face_encoding=face_encoding.tobytes(),
        )
        user_face.save()
        return True
    return False

# Yuz qo'shish view
def add_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if 'capture' in request.FILES:
            photo = request.FILES['capture']
            frame = face_recognition.load_image_file(photo)
            if add_new_face(name, frame):
                return JsonResponse({'status': 'success', 'message': f"{name} muvaffaqiyatli qo'shildi!"})
            else:
                return JsonResponse({'status': 'error', 'message': 'Yuz aniqlanmadi.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Iltimos, suratni yuboring.'})

    return render(request, 'add_user.html')

# Yuzni aniqlash view
def run_face_recognition(request):
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        # Kadrni kichraytirish va RGB formatiga o'tkazish
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            user_id = None

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Barcha foydalanuvchilarni tekshirib chiqish va id ni olish
                user1 = UserData.objects.filter(name=name).all()
                print(f"Foydalanuvchi: {name}, ID: {user1.id}")  # ID ni terminalga chiqarish

            # Kadrni ko'rsatish
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, f"{name} (ID: {user_id})", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0,
                        (255, 255, 255), 1)

        # Oyna chiqishini yaratish
        cv2.imshow('Video', frame)

        # 'q' tugmasi bosilganda chiqish
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Yuzlarni video formatda yuborish
import threading

# Global o'zgaruvchi foydalanuvchini aniqlash uchun
identified_user = None

# def video_feed(request):
#     video_capture = cv2.VideoCapture(0)
#     global identified_user

def gen(camera):
    video_capture = cv2.VideoCapture(0)
    global identified_user
    global identified_user
    while True:
        ret, frame = camera.read()
        if not ret:
            break

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

                # Foydalanuvchini aniqlash
                user = UserData.objects.filter(name=name).first()
                if user and user.status == "user":
                    print(f"Foydalanuvchi tanildi: {user.name}, {user.id}, {user.status}")

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

    return StreamingHttpResponse(gen(video_capture), content_type='multipart/x-mixed-replace; boundary=frame')

# Tanilgan foydalanuvchini tekshirish
def check_identified_user(request):
    global identified_user
    if identified_user:
        user = identified_user
        identified_user = None  # Reset user after detection
        return JsonResponse({"redirect": True, "user_name": user})
    return JsonResponse({"redirect": False})
def video_feed(request):
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed(request):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return StreamingHttpResponse("Kamera ochilmadi!", status=500)

    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')


def face(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


def main(request):
    return render(request, 'main.html')


