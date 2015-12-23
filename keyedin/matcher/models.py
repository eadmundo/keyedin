from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator


class Key(models.Model):

    def __str__(self):
        return self.display_name

    number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    name = models.CharField(
        max_length=1,
        choices=[
            ('C', 'C'),
            ('C#', 'C#'),
            ('D', 'D'),
            ('D#', 'D#'),
            ('E', 'E'),
            ('F', 'F'),
            ('F#', 'F#'),
            ('G', 'G'),
            ('G#', 'G#'),
            ('A', 'A'),
            ('A#', 'A#'),
            ('B', 'B'),
        ])
    minor = models.BooleanField(default=False)
    unique_together = (("number", "name", "minor"),)

    @property
    def display_name(self):
        return u'{} {}'.format(
            self.name,
            'minor' if self.minor else 'major'
        )

    @property
    def dominant(self):
        number = (self.number + 7) % 12
        return Key.objects.get(
            number=number if number else 12,
            minor=self.minor
        )

    @property
    def subdominant(self):
        number = (self.number - 7) % 12
        return Key.objects.get(
            number=number if number else 12,
            minor=self.minor
        )

    @property
    def relative(self):
        diff = 3 if self.minor else -3
        number = (self.number + diff) % 12
        return Key.objects.get(
            number=number if number else 12,
            minor=not self.minor
        )

    @classmethod
    def get_key_from_string(cls, key_string):
        key_lookup = {
            'C': Key.objects.get(number=1, name='C', minor=False),
            'Cm': Key.objects.get(number=1, name='C', minor=True),
            'Db': Key.objects.get(number=2, name='C#', minor=False),
            'Dbm': Key.objects.get(number=2, name='C#', minor=True),
            'D': Key.objects.get(number=3, name='D', minor=False),
            'Dm': Key.objects.get(number=3, name='D', minor=True),
            'Eb': Key.objects.get(number=4, name='D#', minor=True),
            'Ebm': Key.objects.get(number=4, name='D#', minor=True),
            'E': Key.objects.get(number=5, name='E', minor=False),
            'Em': Key.objects.get(number=5, name='E', minor=True),
            'F': Key.objects.get(number=6, name='F', minor=False),
            'Fm': Key.objects.get(number=6, name='F', minor=True),
            'Gb': Key.objects.get(number=7, name='F#', minor=False),
            'Gbm': Key.objects.get(number=7, name='F#', minor=True),
            'G': Key.objects.get(number=8, name='G', minor=False),
            'Gm': Key.objects.get(number=8, name='G', minor=True),
            'Ab': Key.objects.get(number=9, name='G#', minor=False),
            'Abm': Key.objects.get(number=9, name='G#', minor=True),
            'A': Key.objects.get(number=10, name='A', minor=False),
            'Am': Key.objects.get(number=10, name='A', minor=True),
            'Bb': Key.objects.get(number=11, name='A#', minor=False),
            'Bbm': Key.objects.get(number=11, name='A#', minor=True),
            'B': Key.objects.get(number=12, name='B', minor=False),
            'Bm': Key.objects.get(number=12, name='B', minor=True),
        }
        return key_lookup[key_string]


class Box(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)


class Track(models.Model):

    def __str__(self):
        return u'{} - {}'.format(
            self.name,
            self.artist
        )

    name = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255)
    key = models.ForeignKey(Key)
    bpm = models.FloatField(null=False)
    boxes = models.ManyToManyField(Box, related_name='tracks', blank=True)

    @property
    def number_of_matches(self):
        return self.matches.count()

    @property
    def matches(self):
        return Track.objects.filter(
            Q(key=self.key.dominant) |
            Q(key=self.key.subdominant) |
            Q(key=self.key.relative),
            bpm__gte=self.bpm - (self.bpm * 0.03),
            bpm__lte=self.bpm + (self.bpm * 0.03)
        )
