from django.db import models


class RouteQuerySet(models.QuerySet):

    pass
    # def verified(self):
    #     return self.filter(email_confirmed=True)


class RouteManager(models.Manager):

    def get_queryset(self):
        return RouteQuerySet(self.model, using=self._db).all()

    # def verified(self):
    #     return self.get_queryset().verified()
