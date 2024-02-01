from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.views import View
from .forms import MyUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Message
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import MyUserForm
from django import forms

class MainView(TemplateView):
    template_name = "chat/main.html"


class RegisterView(CreateView):
    template_name = "chat/register.html"
    model = User
    form_class = MyUserForm
    success_url = '/chat/main'

            
class LogoutView(View):
    template_name = "chat/logout.html"
    def get(self, request):
        logout(request)
        messages.success(request,"SuccessFully Logged OUT")
        return render(request, self.template_name)



class LoginView(View):
    template_name = "chat/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        # import pdb;
        # pdb.set_trace()
        user = authenticate(username=username, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            messages.success(request, "Successful LogIn")
            return redirect("/chat/index")

        else:
            messages.error(request, "Invalid Credential")
            return render(request, self.template_name)

# class IndexView(TemplateView):
#     template_name = "chat/index.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         totalRooms = Room.objects.all()
#         context['totalRooms'] = totalRooms
#         print(totalRooms)


class IndexView(ListView):
    template_name = "chat/index.html"
    model = Room
    context_object_name = 'totalRooms'
    form_class = forms.Form  # Using a basic form

    def post(self, request, *args, **kwargs):
        existing_room_name = request.POST.get("existing_room")
        new_room_name = request.POST.get("new_room_name")
        
        print("existing_room_name:",existing_room_name,"new_room_name:", new_room_name)
        # print(existing_room_name, new_room_name)
        if new_room_name:
            print("IN")
            # Create a new room and redirect to it
            room, created = Room.objects.get_or_create(name=new_room_name)
            return redirect("/chat/" + new_room_name + "/")
        elif existing_room_name and existing_room_name != 'None':
            print("IN_existing")
            # Redirect to the selected existing room
            return redirect("/chat/" + existing_room_name + "/")
        
        #Check for existim_room_name and new_room_name remains empty
        else:
            return redirect("/chat/index")



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_selection_form'] = self.form_class()
        return context
    

class RoomView(TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = self.kwargs['room_name']
        user_object = get_object_or_404(User, username=self.request.user)
        
        # Use get_or_create to retrieve the existing room or create a new one
        room, created = Room.objects.get_or_create(name=room_name)
        
        if created:
            # If the room is newly created, add the current user as a member
            room.members.add(user_object)
            
        context['room_name'] = room_name
        context['username'] = self.request.user.username
        context['timestamp'] = timezone.now() 
        print("Room:",room_name)
        return context
        

    def get(self, request, *args,**kwargs):
        # Call the superclass method to get the context data
        context = self.get_context_data(**kwargs)

        username = request.user.get_username()
        # messages = Message.objects.filter(room=room_name)
        room_obj = Room.objects.get(name = self.kwargs['room_name'])
        messages = Message.objects.filter(room=room_obj)
        messages = Message.objects.filter(room=room_obj).order_by('id')
        # messages = {"sachal":'sldf'}
        context['messages'] = messages
        return render(request, 'chat/room.html', context)

    