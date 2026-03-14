from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Module(models.Model):
    MODULE_ID_MAX_LEN = 20
    SHORT_NAME_MAX_LEN = 20
    FULL_NAME_MAX_LEN = 50

    # moduleID example: COMPSCI2021
    moduleID = models.CharField(max_length=MODULE_ID_MAX_LEN, unique=True)
    # short_name example: WAD2
    short_name = models.CharField(max_length=SHORT_NAME_MAX_LEN, unique=True)
    # full_name example: Web Application Development 2  
    full_name = models.CharField(max_length=FULL_NAME_MAX_LEN)

    def __str__(self):
        return f"moduleID: {self.moduleID}, short_name: {self.short_name}"


class Review(models.Model):
    MESSAGE_MAX_LEN = 200

    date = models.DateField()
    rating = models.FloatField(
        validators=[MaxValueValidator(5.0), MinValueValidator(0.0)]
    )
    likes = models.PositiveIntegerField(default=0)
    message = models.CharField(max_length=MESSAGE_MAX_LEN, blank=True)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'module'], 
                name='unique_review_student_module',
            )
        ]

    def __str__(self):
        return f"reviewID: {self.pk}"