from django.shortcuts import render, redirect
from .models import Package
from django.contrib.auth.models import User, auth
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path
from django.conf import settings
import time
from pyzbar.pyzbar import decode
import qrcode
import io
import base64
from django.http import HttpResponse
from PIL import Image

# Create your views here.
def home(request):
    return render(request, 'index.html')

def registerpackageform(request):
    return render(request, 'registerpackageform.html')

def loginform(request):
    return render(request, 'loginform.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
    
def addregisterpackage(request):

    if not firebase_admin._apps:
        cred = credentials.Certificate(Path(settings.BASE_DIR, 'static', 'ServiceAccountKey.json'))
        default_app = firebase_admin.initialize_app(cred)

    db = firestore.client()

    qrcode_id = request.POST['qrcode_id']

    sender_firstname = request.POST['sender_firstname']
    sender_lastname = request.POST['sender_lastname']
    sender_add = request.POST['sender_add']
    sender_dis = request.POST['sender_dis']
    sender_pro = request.POST['sender_pro']
    sender_code = request.POST['sender_code']

    recip_firstname = request.POST['recip_firstname']
    recip_lastname = request.POST['recip_lastname']
    recip_add = request.POST['recip_add']
    recip_dis = request.POST['recip_dis']
    recip_pro = request.POST['recip_pro']
    recip_code = request.POST['recip_code']

    doc_ref = db.collection('PackageInformation').document(qrcode_id)
    doc = doc_ref.get().to_dict()

    if doc is not None:
        if doc['activation'] == False:
            messages.info(request, "This QRcode isn't activated.")
            return render(request, 'activateform.html', {'qrcode_id' : qrcode_id})
        elif doc['registeration'] == True:
            messages.info(request, "This QRcode is already registered. Please change QRcode ID")
            return redirect('/registerpackage')
        else:    
            db.collection('PackageInformation').document(qrcode_id).set({   'registeration' : True,
                                                                            'sender_firstname' : sender_firstname,
                                                                            'sender_lastname' : sender_lastname,
                                                                            'sender_add' : sender_add,
                                                                            'sender_dis' : sender_dis,
                                                                            'sender_pro' : sender_pro,
                                                                            'sender_code' : sender_code,
                                                                            'recip_firstname' : recip_firstname,
                                                                            'recip_lastname' : recip_lastname,
                                                                            'recip_add' : recip_add,
                                                                            'recip_dis' : recip_dis,
                                                                            'recip_pro' : recip_pro,
                                                                            'recip_code' : recip_code,
                                                                            'avaliable' : False}, merge=True)
            return render(request, 'trackresult.html', {'qrcode_id' : qrcode_id,
                                                    'sender_firstname' : sender_firstname,
                                                    'sender_lastname' : sender_lastname,
                                                    'sender_add' : sender_add,
                                                    'sender_dis' : sender_dis,
                                                    'sender_pro' : sender_pro,
                                                    'sender_code' : sender_code,
                                                    'recip_firstname' : recip_firstname,
                                                    'recip_lastname' : recip_lastname,
                                                    'recip_add' : recip_add,
                                                    'recip_dis' : recip_dis,
                                                    'recip_pro' : recip_pro,
                                                    'recip_code' : recip_code})
    else:
        messages.info(request, "Doesn't has any QRcode seem like this one.")
        return redirect('/registerpackage')

def registerform(request):
    return render(request, 'registerform.html')

def addlogin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        messages.info(request, 'Username or Password is wrong.')
        return redirect('/login')

def addregister(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    repassword = request.POST['repassword']

    if password == repassword:
        if User.objects.filter(username=username).exists():
            messages.info(request, 'This Username is already in use.')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This E-mail is already in use.')
            return redirect('/register')
        else:
            User.objects.create_user(username = username,
                            first_name = firstname,
                            last_name = lastname,
                            email = email,
                            password = password).save()
            return redirect('/')

    else: 
        messages.info(request, 'Password are not same')
        return redirect('/register')

def generate(request):
    if not firebase_admin._apps:
        cred = credentials.Certificate(Path(settings.BASE_DIR, 'static', 'ServiceAccountKey.json'))
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    uid = request.POST['uid']

    db.collection('PackageInformation').document(uid).set({'activation' : False, 'uid' : uid})

    image = qrcode.make(uid)
    response = HttpResponse(content_type='image/jpeg')
    image.save(response, "JPEG")
    return response

def generateform(request):
    uid = 'TH' + str("{0:.7f}".format(time.time()).replace('.', ''))
    return render(request, 'generateform.html', {"uid" : uid})

def trackform(request):
    return render(request, 'trackform.html')

def addtrack(request):
    if not firebase_admin._apps:
        cred = credentials.Certificate(Path(settings.BASE_DIR, 'static', 'ServiceAccountKey.json'))
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    qrcode_id = request.POST['qrcode_id']

    doc_ref = db.collection('PackageInformation').document(qrcode_id)
    doc = doc_ref.get().to_dict()

    if doc is not None:
        if doc['activation'] == False:
            messages.info(request, "This QRcode isn't activated.")
            return redirect('/track')
        elif doc['registeration'] == False:
            messages.info(request, "This QRcode isn't registered. Please register package.")
            return redirect('/track')
        elif doc['registeration'] == True:
            if 'width' in doc:
                return render(request, 'trackresult.html', {'qrcode_id' : qrcode_id,
                                                            'sender_firstname' : doc['sender_firstname'],
                                                            'sender_lastname' : doc['sender_lastname'],
                                                            'sender_add' : doc['sender_add'],
                                                            'sender_dis' : doc['sender_dis'],
                                                            'sender_pro' : doc['sender_pro'],
                                                            'sender_code' : doc['sender_code'],
                                                            'recip_firstname' : doc['recip_firstname'],
                                                            'recip_lastname' : doc['recip_lastname'],
                                                            'recip_add' : doc['recip_add'],
                                                            'recip_dis' : doc['recip_dis'],
                                                            'recip_pro' : doc['recip_pro'],
                                                            'recip_code' : doc['recip_code'],
                                                            'width' : round(doc['width'], 2),
                                                            'height' : round(doc['height'], 2),
                                                            'depth' : round(doc['depth'], 2),
                                                            'weight' : round(doc['weight'], 2)})
            elif 'width' not in doc:
                return render(request, 'trackresult.html', {'qrcode_id' : qrcode_id,
                                                            'sender_firstname' : doc['sender_firstname'],
                                                            'sender_lastname' : doc['sender_lastname'],
                                                            'sender_add' : doc['sender_add'],
                                                            'sender_dis' : doc['sender_dis'],
                                                            'sender_pro' : doc['sender_pro'],
                                                            'sender_code' : doc['sender_code'],
                                                            'recip_firstname' : doc['recip_firstname'],
                                                            'recip_lastname' : doc['recip_lastname'],
                                                            'recip_add' : doc['recip_add'],
                                                            'recip_dis' : doc['recip_dis'],
                                                            'recip_pro' : doc['recip_pro'],
                                                            'recip_code' : doc['recip_code']})
            else:
                message.info(request, "Something is wrong, Please try again. :(")
                return redirect('/track')
    else:
        messages.info(request, "Doesn't has any QRcode seem like this one.")
        return redirect('/track')

def activateform(request):
    return render(request, 'activateform.html')

def addactivate(request):
    qrcode_id = request.POST['qrcode_id']
    activation_name = request.POST['activation_name']

    if not firebase_admin._apps:
        cred = credentials.Certificate(Path(settings.BASE_DIR, 'static', 'ServiceAccountKey.json'))
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    doc_ref = db.collection('PackageInformation').document(qrcode_id)
    doc = doc_ref.get().to_dict()

    if doc is not None:
        if doc['activation'] == False:
            db.collection('PackageInformation').document(qrcode_id).set({   'activation' : True, 
                                                                            'activation_name' : activation_name,
                                                                            'registeration' : False,
                                                                            'avaliable' : True}, merge=True)
            return redirect('/avaliablecode')

        elif doc['activation'] == True:
            messages.info(request, 'This QRcode is activated already.')
            return redirect('/activate')

        else:
            messages.info(request, 'Sorry, Something is wrong. :(')
    else:
        messages.info(request, "Doesn't has any QRcode seem like this one.")
        return redirect('/activate')

def avaliablecode(request):
    if not firebase_admin._apps:
        cred = credentials.Certificate(Path(settings.BASE_DIR, 'static', 'ServiceAccountKey.json'))
        default_app = firebase_admin.initialize_app(cred)
    avaliablelist = []
    username = request.user.username    
    db = firestore.client()
    doc_ref = db.collection('PackageInformation')
    query_ref = doc_ref.where('activation_name', '==', username).where('avaliable', '==', True).get()

    for data in query_ref:
        fields = data.to_dict()
        if 'uid' in fields:
            avaliablelist.append(fields['uid'])
    
    return render(request, 'avaliablecode.html', {'avaliablelist' : avaliablelist})

def registeredcode(request):
    if not firebase_admin._apps:
        cred = credentials.Certificate(Path(settings.BASE_DIR, 'static', 'ServiceAccountKey.json'))
        default_app = firebase_admin.initialize_app(cred)
    registeredlist = []
    username = request.user.username    
    db = firestore.client()
    doc_ref = db.collection('PackageInformation')
    query_ref = doc_ref.where('activation_name', '==', username).where('registeration', '==', True).get()

    for data in query_ref:
        fields = data.to_dict()
        if 'uid' in fields:
            registeredlist.append(fields['uid'])
    
    return render(request, 'registeredcode.html', {'registeredlist' : registeredlist})

def trackqrform(request):
    return render(request, 'trackqrform.html')

def addtrackqr(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fname = uploaded_file.name
        if fname.endswith('.jpg') or fname.endswith('.png') or fname.endswith('.jpeg') or fname.endswith('.jfif'):
            img = Image.open(io.BytesIO(uploaded_file.read()))

            if len(decode(img)) != 0:
                barcode = decode(img)[0]
                data = barcode.data.decode('utf-8')

                return render(request, 'trackform.html', {'qrcode_id' : data})

        else:
            messages.info(request, 'File extension is not suppported.')
            return redirect('/trackqr')
    else:
        messages.info(request, "Something is wrong.")
        return redirect('/trackqr')

def registerpackageqrform(request):
    return render(request, 'registerpackageqrform.html')

def addregisterpackageqr(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fname = uploaded_file.name
        if fname.endswith('.jpg') or fname.endswith('.png') or fname.endswith('.jpeg') or fname.endswith('.jfif'):
            img = Image.open(io.BytesIO(uploaded_file.read()))

            if len(decode(img)) != 0:
                barcode = decode(img)[0]
                data = barcode.data.decode('utf-8')
                return render(request, 'registerpackageform.html', {"qrcode_id" : data})
            elif len(decode(img)) == 0:
                messages.info(request, "Can't find any QRcode. Please try again.")
                return redirect('/registerpackageqr')
            else:
                messages.info(request, "Something is wrong.")
                return redirect('/registerpackageqr')

        else:
            messages.info(request, 'File extension is not suppported.')
            return redirect('/registerpackageqr')
    else:
        messages.info(request, "Something is wrong.")
        return redirect('/registerpackageqr')

def activateqrform(request):
    return render(request, 'activateqrform.html')

def addactivateqr(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fname = uploaded_file.name
        print(fname)
        if fname.endswith('.jpg') or fname.endswith('.png') or fname.endswith('.jpeg') or fname.endswith('.jfif'):
            img = Image.open(io.BytesIO(uploaded_file.read()))

            if len(decode(img)) != 0:
                barcode = decode(img)[0]
                data = barcode.data.decode('utf-8')
                return render(request, 'activateform.html', {'qrcode_id' : data})

        else:
            messages.info(request, 'File extension is not suppported.')
            return redirect('/activateqr')
    else:
        messages.info(request, "Something is wrong.")
        return redirect('/activateqr')