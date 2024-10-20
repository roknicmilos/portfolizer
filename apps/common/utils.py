from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.urls import reverse


def get_model_admin_details_url(obj: Model) -> str:
    content_type = ContentType.objects.get_for_model(obj.__class__)
    view_name = f"admin:{content_type.app_label}_{content_type.model}_change"
    return reverse(view_name, args=(obj.id,))


def get_model_admin_create_url(model_class: type[Model]) -> str:
    content_type = ContentType.objects.get_for_model(model_class)
    return reverse(f"admin:{content_type.app_label}_{content_type.model}_add")
