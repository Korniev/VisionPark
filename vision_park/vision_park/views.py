# from django.http import HttpResponse
# def main(request):
#     return HttpResponse("Hello, world. You're at the vision_park index.")


from django.shortcuts import render


def main(request):
    return render(request, "vision_park/main.html")