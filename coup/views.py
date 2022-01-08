from django.shortcuts import render
from django.http import HttpResponseRedirect


def coup_login(request):
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
            return HttpResponseRedirect("/coup/game")
    else:
        return render(request, 'coup/coup_login.html', context)


def coup_game(request):
    context = {}
    return render(request, 'coup/coup_game.html', context)