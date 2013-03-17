from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'REST call for master server'

    def handle(self, *args, **options):

        import drest

        api = drest.API(settings.TEAMCITY_URL)
        api.auth(settings.TEAMCITY_USERNAME, settings.TEAMCITY_PASSWORD)
        response = api.make_request('GET',
                                    '/action.html?add2Queue=bt6' +
                                    '&name=name&value=' + site.uuid() +
                                    '&name=country&value=' + site.country +
                                    '&name=currency&value=' + site.currency +
                                    '&name=domain&value=' + site.domain)

        if response.status != 200:
            raise CommandError("TEAMCITY API Error", response)

        return True
