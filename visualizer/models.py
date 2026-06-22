from django.db import models

# Create your models here.

class ObsLocation(models.Model):
    domain = models.TextField()
    s_path = models.TextField()

    def __str__(self):
        return "(" + self.domain + "/" + self.s_path + ")"

class ObsHeader(models.Model):
    bitpix = models.IntegerField()
    naxis = models.IntegerField()
    naxis1 = models.IntegerField()
    naxis2 = models.IntegerField()
    extend = models.BooleanField()
    bscale = models.FloatField()
    bzero = models.IntegerField()
    # Image
    biassec = models.CharField(max_length=32)
    trimsec = models.CharField(max_length=32)
    datasec = models.CharField(max_length=32)
    ccdsec = models.CharField(max_length=32)
    gain = models.FloatField()
    rdnoise = models.FloatField()
    filter = models.CharField(max_length=32)
    waveleng = models.IntegerField()
    bandpass = models.CharField(max_length=32)
    xbinning = models.IntegerField()
    ybinning = models.IntegerField()
    compr_al = models.CharField(max_length=32)
    comp_set = models.CharField(max_length=16)
    n_subimg = models.IntegerField()
    overscan = models.IntegerField()
    creator = models.CharField(max_length=16)
    telescop = models.CharField(max_length=16)
    shutter = models.CharField(max_length=16)
    shut_age = models.FloatField()
    detector = models.CharField(max_length=32)
    # Timing
    timesys = models.CharField(max_length=4)
    exposure = models.FloatField()
    aexptime = models.FloatField()
    rexptime = models.FloatField()
    date_obs = models.DateTimeField()
    time_obs = models.DateTimeField()
    r_exp_s = models.DateTimeField()
    a_exp_s = models.DateTimeField()
    len_flu = models.FloatField()
    len_tran = models.FloatField()
    len_read = models.FloatField()
    len_proc = models.FloatField()
    lendelay = models.FloatField()
    len_save = models.FloatField()
    # Pointing
    equinox = models.FloatField()
    mode = models.CharField(max_length=32)
    modetime = models.FloatField()
    cmd = models.CharField(max_length=32)
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
    hist_nb = models.IntegerField()
    avg_vel = models.FloatField()
    ra_vel = models.FloatField()
    dec_vel = models.FloatField()
    rol_vel = models.FloatField()
    # Environment Data
    temp_ccd = models.FloatField()
    ccdt_nb = models.IntegerField()
    temp_roe = models.FloatField()
    temp_amp = models.FloatField()
    temp_pld = models.FloatField()
    # Mission Planning Section
    object = models.CharField(max_length=32)
    observer = models.CharField(max_length=8)
    intent = models.CharField(max_length=16)
    instrume = models.CharField(max_length=16)
    targtype = models.CharField(max_length=8)
    prop_id = models.CharField(max_length=16)
    pi_name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    moving = models.CharField(max_length=4)
    m2 = models.CharField(max_length=16)
    geo_lat = models.CharField(max_length=16)
    geo_long = models.CharField(max_length=16)
    # Diagnostic
    imgstate = models.CharField(max_length=16)
    # Calibration
    archive = models.CharField(max_length=8)
    obs_type = models.CharField(max_length=8)
    obs_id = models.CharField(max_length=32)

    def __str__(self):
        return "'" + self.image_file + "' of type:" + self.type

class ObservationSet(models.Model):
    name = models.TextField()
    location = models.ForeignKey(ObsLocation, on_delete=models.PROTECT)
    f_path = models.TextField()
    dt = models.DateTimeField()
    saved = models.BooleanField()
    raw = models.BooleanField()
    cor = models.BooleanField()
    cord = models.BooleanField()
    header = models.ForeignKey(ObsHeader, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        sigil = ("✴️", "✅")[self.saved]
        r = (sigil, "❌")[self.raw is None or self.raw is False]
        c = (sigil, "❌")[self.cor is None or self.cor is False]
        d = (sigil, "❌")[self.cord is None or self.cord is False]
        return "(Observation " + self.name + " | R:" + r + " C:" + c + " D:" + d + ")"
