from django.shortcuts import render
from .forms import ContactForm, SearchForm
from .models import Emails, site_contents
from django.utils import timezone
from django.http import HttpResponseRedirect


def about(request):
    return render(request, 'mywork/about.html')


def cv(request):
    context = {}
    add_scroll(request, context)
    return render(request, 'mywork/cv.html', context)


def ecommerce(request):
    context = {}
    add_scroll(request, context)
    return render(request, 'mywork/ecommerce.html', context)


def projects(request):
    context = {}
    add_scroll(request, context)
    return render(request, 'mywork/projects.html', context)


def contact(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            context = {}
            try:
                Email = form.cleaned_data['Email']
                Subject = form.cleaned_data['Subject']
                Message = form.cleaned_data['Message']
                if Emails.objects.all().count() > 100:
                    raise Exception("Sorry I have received too many messages right now, please try again at a later date.")
                elif (Emails.objects.all()) and (((timezone.now() - Emails.objects.last().DateTime).total_seconds()) < 60):
                    diff = (timezone.now() - Emails.objects.last().DateTime).total_seconds()
                    raise Exception(f"Sorry you have sent a message too recently, please wait {60 - diff:.0f} seconds before trying again.")
                record = Emails(Email=Email, Subject=Subject, Message=Message)
                record.save()
                context = {'result': "Email Sent!"}
            except Exception as e:
                context = {'result': e}
            return HttpResponseRedirect()
    else:
        form = ContactForm()
    context = {'form': form}
    form.auto_id = False
    return render(request, 'mywork/contact.html', context)

def search(request):
    context = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            context = {}
            try:
                search = form.cleaned_data['search']  
                results = site_contents.objects.filter(result__contains=search).order_by("name")
                count = len(results)
                context = {'search': search, "results": results, "count" : count}
            except Exception as e:
                context = {'error': e}
            return render(request, 'mywork/search_result.html', context)
    else:
        form = SearchForm()
    context = {'form': form}
    form.auto_id = False
    return render(request, 'mywork/cv.html', context)


def add_scroll(request, context):
    scroll = request.GET.get("scroll", "")
    context["scroll"] = scroll