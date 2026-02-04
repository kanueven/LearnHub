from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from topics.models import Topic
from .models import Room,Message
from django.shortcuts import get_object_or_404
from .forms import RoomForm


# Create your views here.
# #ooms = [
#     {'id':1, 'name':'Learn Python'},
#     {'id':2, 'name':'Learn Django'},
#     {'id':3, 'name':'Learn JavaScript'},
# ] r
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
        context = {'page': page}
        return render(request, 'room/login_register.html', context)
    return render(request,'room/login_register.html',{'page':page})
    

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = UserCreationForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print(request.POST)
            login(request, user)
            
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'room/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q)
                                )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages =  Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'room/index.html',context)

def room(request,pk):
    # room  = Room.objects.get(id=pk)
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all()#fetches all messages related to that room and orders them by created time
    participants = room.participants.all()
    #handle new message
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'room/room.html',{'room':room, 'room_messages':room_messages, 'participants':participants})

def userProfile(request, pk):
    user  = get_object_or_404(User, pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages':room_messages}
    return render(request, 'room/profile.html',context)

@login_required(login_url='login')
##crud operations
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'room/room_form.html',context)

#update room
def updateRoom(request, pk):
    room =  get_object_or_404(Room,pk = pk)
    form = RoomForm(instance=room)
    #no other user can update the room
    if request.user != room.host:
        return HttpResponse('this is not your room you cannot update it')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,'room/room_form.html',context)

#delete room
def deleteRoom(request,pk):
    room = get_object_or_404(Room,pk = pk)
    if request.user != room.host:
        return HttpResponse('this is not your room you cannot delete it')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'room/delete.html', {'obj':room})

#delete message
@login_required(login_url='login')
def deleteMessage(request,pk):
    messages = get_object_or_404(Message,pk = pk)
    if request.user != messages.user:
        return HttpResponse('this is not your message you cannot delete it')
    if request.method == 'POST':
        messages.delete()
        return redirect('home')
    return render(request, 'room/delete.html', {'obj':messages})