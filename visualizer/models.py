from django.db import models

# Create your models here.

# class ImageDetails(models.Model):
#     type = models.CharField(max_length=1) # Simple: S, Cor: C, Cord: D
#     prime_object_name = models.CharField(max_length=100)
#     detector = models.CharField(max_length=50)
#     image_file = models.CharField(max_length=200)
#     satellite_pointing_state = models.CharField(max_length=50)
#     operational_amplifier = models.CharField(max_length=50)
#     binning_x_direction = models.CharField(max_length=50)
#     binning_y_direction = models.CharField(max_length=50)
#     ccd_temperature_k = models.FloatField()
#     date_of_observation = models.DateTimeField()
#     actual_start_time_of_observation = models.DateTimeField()
#     jd_date_of_obs = models.FloatField()
#     requested_exposure_start_time = models.DateTimeField()
#     actual_exposure_start_time = models.DateTimeField()
#     exposure_actual_length_of_exposure_seconds = models.FloatField()
#     shutter_state = models.IntegerField()

#     def __str__(self):
#         return "'" + self.image_file + "' of type:" + self.type

class ObservationSet(models.Model):
    xbinning = models.IntegerField()
    ybinning = models.IntegerField()
    creator = models.CharField(max_length=16)
    telescop = models.CharField(max_length=16)
    exposure = models.FloatField()
    aexptime = models.FloatField()
    rexptime = models.FloatField()
    date_obs = models.DateTimeField()
    time_obs = models.DateTimeField()
    cmdra = models.CharField(max_length=32)
    cmddec = models.CharField(max_length=32)
    cmdrol = models.FloatField()
    cmdq0 = models.FloatField()
    cmdq1 = models.FloatField()
    cmdq2 = models.FloatField()
    cmdq3 = models.FloatField()
    ra = models.CharField(max_length=32)
    dec = models.CharField(max_length=32)
    objctra = models.CharField(max_length=32)
    objctdec = models.CharField(max_length=32)
    objctrol = models.FloatField()
    ela_min = models.FloatField()
    ela_max = models.FloatField()
    ela_ang = models.FloatField()
    sun_min = models.FloatField()
    sun_max = models.FloatField()
    temp_ccd = models.FloatField()
    object = models.CharField(max_length=32)
    observer = models.CharField(max_length=8)
    intent = models.CharField(max_length=16)
    instrume = models.CharField(max_length=16)
    targtype = models.CharField(max_length=8)
    prop_id = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    moving = models.CharField(max_length=4)
    geo_lat = models.CharField(max_length=16)
    geo_long = models.CharField(max_length=16)
    imgstate = models.CharField(max_length=16)
    archive = models.CharField(max_length=8)
    obs_type = models.CharField(max_length=8)
    obs_id = models.CharField(max_length=32)
    year = models.IntegerField()
    day = models.IntegerField()
    raw = models.BooleanField()
    cor = models.BooleanField()
    cord = models.BooleanField()
    clean = models.BooleanField()
    # simple = models.ForeignKey(ImageDetails, null=True, on_delete=models.SET_NULL, related_name="simple_image")
    # cor = models.ForeignKey(ImageDetails, null=True, on_delete=models.SET_NULL, related_name="cor_image")
    # cord = models.ForeignKey(ImageDetails, null=True, on_delete=models.SET_NULL, related_name="cord_image")

    def __str__(self):
        s = ("✅", "❌")[self.raw is None or self.raw is False]
        c = ("✅", "❌")[self.cor is None or self.cor is False]
        d = ("✅", "❌")[self.cord is None or self.cord is False]
        cl = (", CL:✅", "")[self.clean is None or self.clean is False]
        return "(ObservationSet: " + self.obs_id + " | S:" + s + " C:" + c + " D:" + d + cl + ")"
