from .core import BlogBuilder, FileBuilder
from .core.cache import CacheFactory
from .core.exceptions import BlogException, PathError, AuthorizationError, BlogCacheException
from .settings import BLOG_FOLDER, BLOG_INDEX_FILE, BLOG_CACHE, BLOG_CACHE_OPTIONS

from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import TemplateView
from django_leaflet_gpx.templatetags import gpx_map

import datetime
import logging
import os

logger = logging.getLogger(__name__)


def get_cache():
    """
    Return the cache class
    :return:
    """
    if not BLOG_CACHE:
        return None

    cache_type = getattr(CacheFactory(), BLOG_CACHE)
    try:
        return cache_type(BLOG_CACHE_OPTIONS)
    except BlogCacheException as e:
        logger.warning(e.message)
        return None


class BlogFileView(TemplateView):

    EXTENSIONS = ['jpg', 'png', 'pdf', 'gpx']

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def head(self, *args, **kwargs):
        """Retourne la date de dernière modification de l'image"""

        response = HttpResponse('')
        return response

        # TODO inch'allah !
        url = kwargs.get('url')
        path = self._get_image_path(url)
        if path:
            response['Last-Modified'] = datetime.datetime.fromtimestamp(
                os.path.getmtime(path)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

    def get(self, request, *args, **kwargs):

        url = kwargs.get('url', None)
        builder = FileBuilder(BLOG_FOLDER, BlogFileView.EXTENSIONS)

        try:
            file = builder.get(url)
        except FileNotFoundError:
            return HttpResponseNotFound()

        response = HttpResponse(file.content, content_type=file.content_type)
        return response


class BlogContentView(TemplateView):
    template_name = 'blog/content.html'

    def __init__(self):
        super().__init__()

        self.content = None
        self._contains_gpx = False
        self._contains_code = False

    def redirect_to_error(self, message=None):
        """
        Redirect to an error page
        :param message:
        :return:
        """
        self.template_name = 'error-page.html'
        return self.render_to_response({'message': message})

    def dispatch(self, request, *args, **kwargs):
        """
        Global exception catching
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error("BlogContentView.dispatch: {} {}".format(e.__class__.__name__, str(e)))
            if settings.DEBUG:
                logger.exception(e)
            return self.redirect_to_error(str(e) if settings.DEBUG else None)

    def get_breadcrumb_context(self):
        """
        Get the context to display the breadcrumb
        :return:
        """
        context = dict()
        context['breadcrumb'] = []

        parent = self.content.parent
        while parent:
            context['breadcrumb'].append({
                'url': parent.url,
                'title': parent.title if parent.url else "Home",
            })
            parent = parent.parent

        context['breadcrumb'].reverse()
        return context

    def get_content_context(self):
        """
        Get the context to display the content
        :return:
        """
        context = dict()
        context['content'] = self.content
        context['previous_content'] = self.content.previous
        context['next_content'] = self.content.next
        context['contains_gpx'] = self._contains_gpx
        context['contains_code'] = self._contains_code
        return context

    def parse_content_html(self, content):
        """
        Retourne le contenu HTML formaté pour le blog
        :param content:
        :param html:
        :return:
        """

        html = content.content
        soup = BeautifulSoup(html, "html.parser")

        prefix = content.url

        # Si ce n'est pas un fichier d'index, on retire le nom du fichier de l'url
        if not content.path.endswith(BLOG_INDEX_FILE):
            prefix = os.path.split(prefix)[0]

        # On remplace les urls des images pour les faire correspondre
        for img in soup.find_all('img'):
            img_url = os.path.join(prefix, img['src'])
            img['src'] = reverse('blog:file', kwargs={'url': img_url})

        context = RequestContext(self.request)

        # On recherche les tags GPX pour les remplacer par le contenu
        for p in soup.find_all('p'):
            if p.text.startswith('{{gpx:') and p.text.endswith('}}'):
                gpx_url = reverse('blog:file', kwargs={'url': os.path.join(prefix, p.text[6:-2])})
                gpx_section = render(
                    self.request,
                    'leaflet-gpx/map-gpx.html',
                    gpx_map(context, gpx_url)
                )

                p.replace_with(BeautifulSoup(gpx_section.content.decode('utf-8'), 'html.parser'))
                self._contains_gpx = True

        # On recherche les tags <pre> et <code> pour activer l'highlighting
        for pre in soup.find_all('pre'):
            if pre.find('code'):
                self._contains_code = True
                break

        return str(soup)

    def get(self, request, *args, **kwargs):

        url = kwargs.get('url', '')
        
        # Add self request attribute if not defined
        if not hasattr(self, 'request'):
            self.request = request

        # Récupération du cache
        cache = get_cache()

        # Récupération des groupes
        groups = []
        if request.user.is_authenticated and hasattr(request.user, 'ldap_user'):
            groups = request.user.ldap_user.group_names

        builder = BlogBuilder(
            base_folder=BLOG_FOLDER,
            category_file=BLOG_INDEX_FILE,
            cache=cache,
            groups=groups,
            is_admin=request.user.is_staff
        )

        try:
            self.content = builder.get(url)

        except BlogException as e:
            logger.error("Recherche de contenu: {}".format(str(e)))

            message = "J'ignore pourquoi vous êtes ici..."
            if isinstance(e, PathError):
                message = "Le contenu demandé n'existe pas."
            elif isinstance(e, AuthorizationError):
                message = "Vous n'avez pas l'autorisation d'atteindre ce contenu."

            return self.redirect_to_error(message)

        self.content.content = self.parse_content_html(self.content)

        context = super().get_context_data()
        context['view_title'] = self.content.title
        context = {
            **context,
            **self.get_breadcrumb_context(),
            **self.get_content_context()
        }

        return self.render_to_response(context)
