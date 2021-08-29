from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
import pyrebase
import datetime

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
            name = db.child(sid).update({"name":name})
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
    name = db.child("user").child(userobj).child("name").child("name").get()
    print(name.val())
    avpath = "avatar/"+ userobj +".jpg" 
    avpath = pyrestorage.child(avpath).get_url(None)
    print(userobj)
    #print(avpath)
    return render(request, 'dashboard/sidebar.html', {"msg": message ,"lid": userobj,"dp": avpath,"nam": name.val()})
