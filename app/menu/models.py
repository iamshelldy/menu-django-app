from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('menu', 'parent', 'slug')

    def __str__(self):
        return self.name

    def get_item_url(self):
        ancestors = []
        node = self

        while node.parent:
            ancestors.append(node.parent.slug)
            node = node.parent

        ancestors = list(reversed(ancestors))

        path = '/'.join(ancestors + [self.slug])
        return f'/{path}/'
