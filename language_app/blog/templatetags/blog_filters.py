from django import template

register = template.Library()

@register.filter
def ordering_button_style(ordering, current_ordering):
    """Checks if the current ordering applies to the given ordering button and changes its
    bootstrap styling accordingly.

    args:
        ordering: the ordering type that this button applies to
        current_ordering: The current ordering of the definitions
    """
    if ordering == current_ordering:
        return 'btn btn-dark'
    else:
        return 'btn btn-outline-dark'
    
@register.filter
def count_definitions_in_category(category):
    """Given a category, use the reverse many-to-many relationship between Definition.categories
    and Category to count the number of definitions with the given category using the related name.
    """

    # Placed the definitions count in a filter as older Django versions don't support parentheses
    # directly in templates
    return category.definitions.count()