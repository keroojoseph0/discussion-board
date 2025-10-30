import hashlib
from urllib.parse import urlencode
from django import template
from django.conf import settings

default = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', 'mm')
size = getattr(settings, 'GRAVATAR_SIZE', 256)


register = template.Library()

@register.filter
def gravatar(user):
    """
    Generate Gravatar URL from user object or email string.
    Usage: {{ user|gravatar }}
    """
    # Handle both User object and plain string
    if hasattr(user, 'email'):
        email = user.email or ''
    else:
        email = str(user)

    email = email.lower().encode('utf-8')
    default = 'mm'
    size = 256

    url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
        md5=hashlib.md5(email).hexdigest(),
        params=urlencode({'d': default, 's': str(size)})
    )
    return url
