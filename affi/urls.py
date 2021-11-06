"""affi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .graphqlapi.api import schema
from django.conf import settings
from django.conf.urls.static import static
# from .graphql.views import GraphQLView

from .product.views import woocommerce_update_product, woocommerce_create_product


urlpatterns = [
    url(r"^graphql/$", csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True)), name="api"),
    path('admin/', admin.site.urls),
    path("woocommerce_update_product/", woocommerce_update_product, name="woocommerce_update_product"),
    path("woocommerce_create_product/", woocommerce_create_product, name="woocommerce_create_product"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
