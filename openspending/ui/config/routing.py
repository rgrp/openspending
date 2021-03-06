"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from paste.deploy.converters import asbool
from routes import Mapper

from openspending.plugins.core import PluginImplementations
from openspending.plugins.interfaces import IRoutes


routing_plugins = PluginImplementations(IRoutes)

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'], explicit=True)
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    # The ErrorTestController is used to test our custom error pages.
    map.connect('/_error_test/{action}', controller='error_test')

    # CUSTOM ROUTES HERE
    for plugin in routing_plugins:
        plugin.before_map(map)

    if not asbool(config.get('openspending.sandbox_mode', False)):
        map.sub_domains = True
        # Ignore the ``www`` sub-domain
        map.sub_domains_ignore = ['www', 'sandbox', 'staging']

        map.connect('/', controller='home', action='index_subdomain',
                    conditions={'sub_domain': True})

    map.connect('/', controller='home', action='index')

    map.connect('/getinvolved', controller='home', action='getinvolved')
    map.connect('/reporterror', controller='home', action='reporterror')
    map.connect('/locale', controller='home', action='locale')

    map.connect('/login', controller='account', action='login')
    map.connect('/register', controller='account', action='register')
    map.connect('/settings', controller='account', action='settings')
    map.connect('/after_login', controller='account', action='after_login')
    map.connect('/after_logout', controller='account', action='after_logout')

    map.connect('search', '/search', controller='search', action='index')

    map.connect('/dataset.{format}', controller='dataset', action='index')
    map.connect('/dataset', controller='dataset', action='index')

    map.connect('/dataset/{name}.{format}', controller='dataset', action='view')
    map.connect('/dataset/{name}', controller='dataset', action='view')
    map.connect('/dataset/bubbles/{name}/{breakdown_field}/{drilldown_fields}', controller='dataset', action='bubbles')

    map.connect('/dataset/{dataset}/dimension.{format}',
                controller='dimension', action='index')
    map.connect('/dataset/{dataset}/dimension',
                controller='dimension', action='index')
    map.connect('/dataset/{dataset}/dimension/{dimension}.{format}',
                controller='dimension', action='view')
    map.connect('/dataset/{dataset}/dimension/{dimension}',
                controller='dimension', action='view')

    map.connect('/dataset/{name}/{action}.{format}', controller='dataset')
    map.connect('/dataset/{name}/{action}', controller='dataset')

    map.connect('/entity', controller='entity', action='index')
    map.connect('/entity/{id}.{format}', controller='entity', action='view')
    map.connect('/entity/{id}', controller='entity', action='view')
    map.connect('/entity/{id}/entries.{format}', controller='entity',
                action='entries')
    map.connect('/entity/{id}/entries', controller='entity', action='entries')
    map.connect('/entity/{id}/{slug}', controller='entity', action='view')

    map.connect('/classifier/{id}.{format}', controller='classifier',
                action='view')
    map.connect('/classifier/{id}', controller='classifier', action='view')

    map.connect('/classifier/{taxonomy}/{name}.{format}',
                controller='classifier', action='view_by_taxonomy_name')
    map.connect('/classifier/{taxonomy}/{name}',
                controller='classifier', action='view_by_taxonomy_name')
    map.connect('/classifier/{taxonomy}/{name}/view',
                controller='classifier', action='view_by_taxonomy_name')

    map.connect('/classifier/{taxonomy}/{name}/entries.{format}',
                controller='classifier', action='entries')
    map.connect('/classifier/{taxonomy}/{name}/entries',
                controller='classifier', action='entries')

    map.connect('/entry', controller='entry', action='index')
    map.connect('/entry/{id}.{format}', controller='entry', action='view')
    map.connect('/entry/{id}', controller='entry', action='view')
    map.connect('/entry/{id}/{action}', controller='entry')

    map.connect('/api', controller='api', action='index')
    map.connect('/api/search', controller='api', action='search')
    map.connect('/api/aggregate', controller='api', action='aggregate')
    map.connect('/api/mytax', controller='api', action='mytax')

    map.connect('/api/rest/', controller='rest', action='index')
    map.connect('/api/2/aggregate', controller='api2', action='aggregate')

    map.connect('/500', controller='error', action='render', code="500")

    map.connect('/__version__', controller='home', action='version')

    for plugin in routing_plugins:
        plugin.after_map(map)

    map.redirect('/*(url)/', '/{url}', _redirect_code='301 Moved Permanently')
    return map
