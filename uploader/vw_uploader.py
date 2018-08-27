from os import path, mkdir
import re

from django.shortcuts import render
from django.conf import settings
from seguridad.mkitsafe import *

# Create your views here.

# @valida_acceso()
def uplopader( request, type ):
    if 'POST' == request.method:
        if( len( request.FILES ) > 0 ):
            arch = request.FILES.get( 'uploader-file' )
            target_dir = path.abspath( path.join( settings.MEDIA_ROOT, type ) )
            target_file = path.join( target_dir, arch.name )
            extension = path.splitext( target_file )[ -1 ]
            basename = path.basename( target_file ).replace( extension, "" )
            basename = re.sub( '[^A-Za-z0-9-_]', "_", basename )
            target_file = path.join( target_dir, "{}{}".format( basename, extension ) )
            if not path.isdir( target_dir ):
                mkdir( target_dir )
            counter = 1
            while path.isfile( target_file ):
                target_file = path.join( target_dir, "{}_{:03d}{}".format( basename, counter, extension ) )
                counter += 1
            with open( target_file, 'wb+' ) as file:
                for parte in arch.chunks():
                    file.write( parte )
            return render( request, 'uploader/results.html', {
                'file' : path.basename( target_file ),
                'onresponse' : request.POST.get( 'onresponse' ),
                'excecute' : request.POST.get( 'excecute' ),
                'message' : request.POST.get( 'message' )
            } )
        return render( request, 'uploader/form.html', {} )
    else:
        return render( request, 'uploader/form.html', {} )
