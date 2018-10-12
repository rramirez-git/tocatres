from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import *
from .models import *
from .mkitsafe import *

@valida_acceso()
def index( request ):
    pass

@valida_acceso()
def update( request, pk ):
    pass

def setvalue( request, pk ):
    pass