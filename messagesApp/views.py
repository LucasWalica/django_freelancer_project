from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from .forms import MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.models import User 
from django.utils import timezone 
from django.db.models import Q, OuterRef, Subquery


from recruiter.models import RecruiterProfile
from freelancer.models import FreelancerProfile

class InboxView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        check_user_profile_exists(request.user)
        unreadMessages = Message.objects.filter(receiver=request.user, read=False).order_by('-timestamp')
        
        all_messages = Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
            ).exclude(sender=request.user, receiver=request.user).order_by('-timestamp')

        # Use a dictionary to ensure each conversation is only shown once
        conversations_dict = {}
        for message in all_messages:
            participants = frozenset([message.sender, message.receiver])
            if participants not in conversations_dict:
                conversations_dict[participants] = message

        # Convert the dictionary back to a list of messages
        conversations = list(conversations_dict.values())
        
        context = {
            'unreadMessages': unreadMessages,
            'conversations': conversations
        }
        return render(request, 'messages/inbox.html', context)

#chatView with each other 
class MessagesWithOtherView(LoginRequiredMixin, View):
    def get(self, request, pk2, *args, **kwargs):
        check_user_profile_exists(request.user)
        other_user = get_object_or_404(User, id=pk2)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) | 
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('timestamp').select_related('sender', 'receiver')  # Optimización de consultas
        
        form = MessageForm()
        context = {
            'messages': messages,
            'other_user': other_user,
            'form': form
        }
        
        # Marcar los mensajes recibidos como leídos
        unread_messages = messages.filter(receiver=request.user, read=False)
        unread_messages.update(read=True)
        
        return render(request, 'messages/chat.html', context)
    
    def post(self, request, pk2, *args, **kwargs):
        other_user = get_object_or_404(User, id=pk2)
        form = MessageForm(request.POST)
        
        if form.is_valid():
            body = form.cleaned_data.get('body')
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                body=body,
                timestamp=timezone.now(),
                read=False
            )
            # Redirigir a la misma página de chat para evitar reenvío del formulario
            return redirect('messageWithOther', pk1=request.user.id, pk2=other_user.id)
        
        # En caso de que el formulario no sea válido
        context = {
            'messages': Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) | 
                (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('timestamp'),
            'other_user': other_user,
            'form': form
        }
        
        return render(request, 'messages/chat.html', context)



def check_user_profile_exists(user):
    try:
        freelancer = FreelancerProfile.objects.get(user=user)
        return freelancer, 'freelancer'
    except FreelancerProfile.DoesNotExist:
        pass
    
    try:
        recruiter = RecruiterProfile.objects.get(user=user)
        return recruiter, 'recruiter'
    except RecruiterProfile.DoesNotExist:
        pass
    
    return None, None
