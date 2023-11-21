from django.shortcuts import render


def thank_you_view(request):
    return render(request, 'thank_you.html')
