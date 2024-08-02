from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.read = True
    message.save()
    return render(request, 'messaging/view_message.html', {'message': message})
