from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField("Название на русском", max_length=200)
    title_en = models.CharField("Название на английском", max_length=200, blank=True)
    title_jp = models.CharField("Название на японском", max_length=200, blank=True)
    image = models.ImageField("Картинка", upload_to='pokemon_images/', blank=True, null=True)
    description = models.TextField("Описание", blank=True)

    evolved_from = models.ForeignKey(
        'self',
        verbose_name="Эволюционирует из",
        null=True,
        blank=True,
        related_name='next_evolutions',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name="Покемон")
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeared_at = models.DateTimeField("Появляется в", null=True, blank=True)
    disappeared_at = models.DateTimeField("Исчезает в", null=True, blank=True)
    level = models.IntegerField("Уровень", null=True, blank=True)
    health = models.IntegerField("Здоровье", null=True, blank=True)
    strength = models.IntegerField("Сила", null=True, blank=True)
    defence = models.IntegerField("Защита", null=True, blank=True)
    stamina = models.IntegerField("Выносливость", null=True, blank=True)