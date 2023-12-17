from django.template.defaultfilters import slugify

# Пример использования slugify
title = "Однажды в кануне лета"
post_slug = slugify(title)
print(post_slug)