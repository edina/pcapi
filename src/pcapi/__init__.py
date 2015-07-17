from pkg_resources import get_distribution

# api_version is pcapi API version - that is what currently appears on the URL
api_version = '1.4'
__version__ = get_distribution('pcapi').version
