from django.db import models

# Create your models here.
class Package(models.Model):
    qrcode_id = models.CharField(max_length=20)
    activation = models.BooleanField(default=False)
    activation_name = models.TextField()
    registeration = models.BooleanField(default=False)

    sender_firstname = models.TextField()
    sender_firstname = models.TextField()
    sender_add = models.TextField()
    sender_subdis = models.TextField()
    sender_dis = models.TextField()
    sender_code = models.TextField()

    recip_firstname = models.TextField()
    recip_lastname = models.TextField()
    recip_add = models.TextField()
    recip_subdis = models.TextField()
    recip_dis = models.TextField()
    recip_code = models.TextField()

    height = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()
    weight = models.FloatField()


