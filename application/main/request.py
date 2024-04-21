from django.conf import settings


def settings_context(request):
    return {
        "name": settings.SITE_NAME,
        "address": settings.OWNER_ADDRESS,
        "contact_number": settings.OWNER_NUMBER,
        "contact_email": settings.OWNER_EMAIL,
        "facebook_page": settings.FACEBOOK_PAGE,
        "tiktok_page": settings.TIKTOK_PAGE,
        "insta_page": settings.INSTA_PAGE,
    }
