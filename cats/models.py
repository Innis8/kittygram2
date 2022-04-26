from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Чёрный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный'),
)

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats', on_delete=models.CASCADE)
    achievements = models.ManyToManyField(
        Achievement,
        through='AchievementCat'
    )

    class Meta:
        # Для сериализаторов в DRF есть несколько встроенных
        # классов-валидаторов, среди них есть UniqueValidator и
        # UniqueTogetherValidator.
        # В базе данных не должно быть двух или более записей, у которых имя
        # котика и хозяин совпадают.
        # unique_together = ('name', 'owner')

        # Но документация Django рекомендует вместо unique_together
        # использовать UniqueConstraint: этот способ обеспечивает большую
        # функциональность, а unique_together может быть признан устаревшим в
        # будущем.
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'owner'],
                name='unique_name_owner'
            )
        ]

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'
