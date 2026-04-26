from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
from .models import Contact


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save()
            content_html = render_to_string('contact/email.html', {
                'name': contact.first_name,
                'message': contact.message,
            })
            email = EmailMessage(
                subject='We received your message - Planteer 🌱',
                body=content_html,
                from_email=settings.EMAIL_HOST_USER,
                to=[contact.email],
            )
            email.content_subtype = 'html' 
            email.send()
            messages.success(request,"your message is received")
            return redirect('contact:contact')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

def contact_messages_view(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/contact_messages.html', {'messages': messages})