from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    url = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Родитель'
    )
    menu_name = models.CharField(max_length=50, verbose_name='Имя меню')
    is_root = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.title
