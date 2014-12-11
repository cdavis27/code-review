from django.contrib import admin
from django.db.models import get_models, get_app

for model in get_models(get_app('api')):
    admin.site.register(model)