from reachify.reachapp.models import Platform


def get_instagram_platform():
    instance = Platform.objects.filter(name="Instagram").first()
    return instance
