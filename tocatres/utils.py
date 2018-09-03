
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

def month_name( month ):
    if 1 == int( month ):
        return "Ene"
    if 2 == int( month ):
        return "Feb"
    if 3 == int( month ):
        return "Mar"
    if 4 == int( month ):
        return "Abr"
    if 5 == int( month ):
        return "May"
    if 6 == int( month ):
        return "Jun"
    if 7 == int( month ):
        return "Jul"
    if 8 == int( month ):
        return "Ago"
    if 9 == int( month ):
        return "Sep"
    if 10 == int( month ):
        return "Oct"
    if 11 == int( month ):
        return "Nov"
    if 12 == int( month ):
        return "Dic"
    return ""
