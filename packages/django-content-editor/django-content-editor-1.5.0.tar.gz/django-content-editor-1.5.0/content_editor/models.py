from __future__ import unicode_literals

from django.db import models

from six import python_2_unicode_compatible


try:
    from types import SimpleNamespace
except ImportError:  # pragma: no cover
    # Python < 3.3
    class SimpleNamespace(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)


__all__ = ("Region", "Template", "create_plugin_base")


class Region(SimpleNamespace):
    key = ""
    title = "unnamed"
    inherited = False


class Template(SimpleNamespace):
    key = ""
    template_name = None
    title = ""
    regions = []


def create_plugin_base(content_base):
    """
    This is purely an internal method. Here, we create a base class for
    the concrete content types, which are built in
    ``create_plugin``.

    The three fields added to build a concrete content type class/model
    are ``parent``, ``region`` and ``ordering``.
    """

    @python_2_unicode_compatible
    class PluginBase(models.Model):
        parent = models.ForeignKey(
            content_base,
            related_name="%(app_label)s_%(class)s_set",
            on_delete=models.CASCADE,
        )
        region = models.CharField(max_length=255)
        ordering = models.IntegerField(default=0)

        class Meta:
            abstract = True
            app_label = content_base._meta.app_label
            ordering = ["ordering"]

        def __str__(self):
            return "%s<region=%s ordering=%s pk=%s>" % (
                self._meta.label,
                self.region,
                self.ordering,
                self.pk,
            )

        @classmethod
        def get_queryset(cls):
            return cls.objects.all()

    return PluginBase
