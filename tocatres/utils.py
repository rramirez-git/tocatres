
def print_error( message, level = "Warning" ):
    print( "=======================", level, message )
    
def print_list( lista ):
    for indice, elemento in enumerate( lista ):
        print( "{:04d}: {}".format( indice, elemento ) )

def requires_jquery_ui( request ):
    ua = request.META[ "HTTP_USER_AGENT" ].lower()
    if "chrome" in ua \
            or "chromium" in ua \
            or "edge" in ua \
            or "mobi" in ua \
            or "phone" in ua:
        return False
    return True