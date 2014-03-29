# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from util import convert_code_to_term, convert_term_to_code
import json

@csrf_exempt
def term(request, term):
    term_code = convert_term_to_code(term)
    f = open('%s.json'%term_code, 'r')
    courses_j = f.read()
    return HttpResponse(courses_j, content_type="application/json")