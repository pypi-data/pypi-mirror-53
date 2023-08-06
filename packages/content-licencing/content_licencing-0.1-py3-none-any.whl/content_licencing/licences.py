from django.conf import settings

# create licencing choices from settings
CONTENT_LICENCING_LICENCES = getattr(settings, 'CONTENT_LICENCING_LICENCES', [])

LICENCE_CHOICES = []

LICENCE_VERSION_CHOICES = {
}

for choice in CONTENT_LICENCING_LICENCES:
    licence_choice = (
        choice['short_name'], choice['full_name']
    )

    LICENCE_CHOICES.append(licence_choice)

    version_choices = []
    for version, link in choice['versions'].items():
        version_choice = (
            version, version
        )
        version_choices.append(version_choice)

    LICENCE_VERSION_CHOICES[choice['short_name']] = version_choices


class ContentLicence:

    def __init__(self, short_name, version):
        self.short_name = short_name
        self.version = version

    def as_dict(self):
        dic = {
            'short_name' : self.short_name,
            'version' : self.version,
        }

        return dic

        
DEFAULT_LICENCE = ContentLicence(settings.CONTENT_LICENCING_DEFAULT_LICENCE['short_name'], settings.CONTENT_LICENCING_DEFAULT_LICENCE['version'])
