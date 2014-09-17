# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from re import search
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from mezzanine.pages.models import Page
from .models import PageAuthGroup


class PageAuthMiddleware(object):
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The PageAuthMiddleware middleware requires the"
                " authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the PageAuthMiddleware class.")
        slug = request.path
        if slug != '/':
            slug = slug.strip('/')
        request.unauthorized_pages = PageAuthGroup.unauthorized_pages(
            request.user)
        try:
            page = Page.objects.get(slug=slug)
            if page.pk in request.unauthorized_pages:
                return HttpResponseForbidden()
        except Page.DoesNotExist:
            pass

"""
class PageAuthGroupAdminMiddleware(object):
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The PageAuthGroupAdminMiddleware middleware requires the"
                " authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the PageAuthGroupAdminMiddleware class.")
        slug = request.path
        url_pieces = slug.split('/')
        if slug != '/':
            slug = slug.strip('/')
        request.unauthorized_pages = PageAuthGroup.unauthorized_pages(
            request.user)
        try:
            page_id = len(url_pieces) - 2
            if search('admin', slug):
                try:
                    page = Page.objects.get(id=url_pieces[page_id])
                    if page.pk in request.unauthorized_pages:
                        return HttpResponseForbidden("You do not have access to view this page. Please ask your admin to add you to authenticated group.")
                except Exception as e:
                    print e
        except Page.DoesNotExist:
            pass
"""
