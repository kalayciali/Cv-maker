from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='accounts', blank=True)
    bullet_descript = models.CharField(max_length=200, blank=True)
    descript = models.TextField(max_length=500, blank=True)
    phone_regex = RegexValidator(regex=r'^\d{11}$', message= "0 ile başlayarak 11 haneli olarak giriniz.")
    phone_num = models.CharField(validators=[phone_regex, ], max_length=11, blank=True)
    address = models.CharField(max_length=30, blank=True)
    links = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Profile"

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

