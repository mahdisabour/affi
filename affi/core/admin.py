from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

exlude_model_name = ["ModelWithMetaData"]

app_models = apps.get_app_config('core').get_models()
for model in app_models:
    # if model.model_name not in exlude_model_name:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass