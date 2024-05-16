from django.shortcuts import render


def main(request):
    return render(request, "vision_park/main.html")
