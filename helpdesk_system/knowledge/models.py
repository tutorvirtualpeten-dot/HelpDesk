from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        ARCHIVED = 'ARCHIVED', _('Archived')

    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    content = models.TextField(_("Content")) # Could use a rich text field later
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CannedResponse(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Response Content"))
    shortcut = models.CharField(_("Shortcut"), max_length=50, unique=True, help_text="e.g. #greeting")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
