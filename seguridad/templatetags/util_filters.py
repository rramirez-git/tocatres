from django import template
from django.template.defaultfilters import stringfilter
from random import randint

register = template.Library()

@register.filter
@stringfilter
def summary( text ):
    number_of_words = 25
    if len( text.split( " " ) ) > number_of_words:
        return " ".join( text.split( " " )[ : number_of_words ] ) + "..."
    return text

@register.filter
@stringfilter
def as_paragraph( text ):
    pars = []
    for p in text.split( '\n' ):
        if "" != p.strip():
            pars.append( '<p>{}</p>'.format( p.strip() ) ) 
    return "".join( pars )
