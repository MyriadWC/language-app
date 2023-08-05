from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Definition

# NOTE: This validation is now performed in DefinitionUpdateView and DefinitionCreateView, so this
# signal receiver is now an unnccessary backstop to that check and can safely be deleted.
@receiver(m2m_changed, sender=Definition.categories.through)
def validate_categories(sender, instance, action, **kwargs):

    if action in ['post_add', 'post_remove', 'post_clear']:

        if instance.categories.count() > 5:

            raise ValidationError("A definition can belong to at most five categories")