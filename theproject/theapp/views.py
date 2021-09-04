from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
import pyrebase
import datetime
import os

#pyrebase sdk
config = {
    'apiKey': "AIzaSyCqa4-n6rAH4w16W7k0ZZBhW6nKqaOyYgU",
    'authDomain': "project-78015.firebaseapp.com",
    'databaseURL': "https://project-78015-default-rtdb.firebaseio.com",
    'projectId': "project-78015",
    'storageBucket': "project-78015.appspot.com",
    'messagingSenderId': "42607330346",
    'appId': "1:42607330346:web:4ad5d92b9c9f49f7c1ef53",
    'measurementId': "G-KSMCSSMRW4" }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()
 
# Create your views here.

def loginpage(request):
    msg = request.session.get('msg')
    if not msg:
        msg = ""
    return render(request, 'login/index.html', {"msg": msg})

def signup(request):
    return render(request, 'Registration/signup.html')

#signup function
def postsignup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        passw = request.POST['password1']
        passw2 = request.POST['password2']
        
        if passw != passw2:
            request.session['msg'] = "Passwords didn't Match! Try again"
            return signup(request)
        else:
            userobj = pyreauth.create_user_with_email_and_password(email, passw)
            sid = userobj['localId']
            print(sid)           
            request.session['uid'] = sid
            data = {"name" : name,
                "filecount": 0,
            }
            x = "avatar/" + sid + ".jpg" 
            pyrestorage.child(x).put("theapp/static/image.jpg")
            db.child(sid).set(data)
            request.session["msg"] = "Account Creation Success! Login now!"
            return loginpage(request)



#login function
def firebaseLoginAuth(request):
    if request.method =='POST':
        mail = request.POST['email']
        password = request.POST['passw']
        print(mail)
        print(password)
        #try:
        userobject = pyreauth.sign_in_with_email_and_password(mail,password)
        #localID set and print
        sid = userobject['localId']
        request.session['uid'] = sid
        sid = request.session.get('uid')
        print(sid)
        #roles set and print
        return homepage(request, "successfully logged in")
        #except:
            #request.session["msg"]="invalid email or password"
            #return loginpage(request)
    else: 
        return homepage(request, "")


#Google Sign in works
def GoogleSignin(request):
    userobj = request.POST['uid']
    print(userobj)
    request.session['uid'] = userobj
    return homepage (request, "Google Sign in success")

#Returns homepage
def homepage(request, message):
    userobj = request.session.get('uid')
    x = db.child(userobj).child("name").get()
    name = x.val()
    #print(name)
    x = db.child(userobj).child("filecount").get()
    filecount = x.val()
    #print(filecount)
    x = "avatar/"+ userobj +".jpg"
    avatar = pyrestorage.child(x).get_url(None)
    #print(avatar)
    myfiles = ownfiles(userobj)
    return render(request, 'Dashboard/sidebar.html', {"msg": message, "nam" : name, "count" : filecount, "avatar" : avatar, "lid" : userobj, "zip": myfiles})

def uploadfile(request):
   filename = request.POST['fname']
   filelink = request.FILES['drc'] 
   extension =os.path.splitext(filelink.name)
   userobj = request.session.get('uid')
   x = userobj + "/" + filename + extension[1]  
   pyrestorage.child(x).put(filelink)
   c = str(datetime.datetime.now())
   y = (pyrestorage.child(x).get_url(userobj))
   z = {"name" : (filename + extension[1]),
   "created" : c,
   "creator": userobj,
   "url": y,
   "Access": {
   userobj : True}}
   db.child("files").push(z)
   count = db.child(userobj).get()
   for pieces in count.each():
       if (pieces.key() == "filecount"):
           count = pieces.val()
           break
   count = count+1
   db.child(userobj).update({"filecount" : count})
   return homepage(request, "File Successfully Uploaded!")

#Self Files zipped
def ownfiles(userobj):
   Filename = []
   Uploadtime = []
   url = []
   x = db.child("files").get()
   for user in x.each():
       y = db.child("files").child(user.key()).get()
       for creator in y.each():
           if (creator.key()== "creator"):
               z = creator.val()
           else: z = 0
           if userobj == z:
               for og in y.each():
                   if og.key() == "created":
                       Uploadtime.append(og.val())
                   if og.key() == "name":
                       Filename.append(og.val())
                   if og.key() == "url":
                       url.append(og.val())
   print(Filename)
   print(Uploadtime)
   print(url)
   zipped = zip (Filename, Uploadtime, url)
   return zipped

def logout(request):
    auth.logout(request)
    return loginpage(request)
                   
def invite(request):
    return render(request, 'Invite/Collab.html')


