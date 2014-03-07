import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from course.models import Course

# Create your views here.
@csrf_exempt
def subject(request,subject):
    courses = Course.objects.filter(subject=subject)
    CNBRS = []
    for course in courses:
        CNBRS.append(course.CNBR)
    result = json.dumps(
        CNBRS,
    )
    return HttpResponse(result, content_type="application/json")

@csrf_exempt
def courses(request, subject, CNBR):
    course_db = Course.objects.get(code=(subject+CNBR).upper())
    result = json.dumps(
        course_db.dump_data()
    )
    return HttpResponse(result, content_type="application/json")
