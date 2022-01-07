from django.shortcuts import render


def coup(request):
    context = {}
    return render(request, 'coup/coup.html', context)
