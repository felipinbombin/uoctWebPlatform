from django.db import models

# Create your models here.
class Tramos15MinUOCT(models.Model):
    eje_id = models.CharField(max_length=200, blank=True, null=True)
    secuencia_eje_macro = models.IntegerField(blank=True, null=True)
    tramo = models.CharField(max_length=200)
    eje = models.CharField(max_length=200)
    hito_origen = models.CharField(max_length=200, blank=True, null=True)
    hito_destino = models.CharField(max_length=200, blank=True, null=True)
    zona = models.CharField(max_length=200, blank=True, null=True)
    destino = models.CharField(max_length=200, blank=True, null=True)
    calle_origen = models.CharField(max_length=200, blank=True, null=True)
    calle_destino = models.CharField(max_length=200, blank=True, null=True)
    dist_en_ruta = models.IntegerField()
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    velocidad_tramo = models.FloatField(blank=True, null=True)
    tiempo_viaje_tramo = models.IntegerField(blank=True, null=True)
    tiempo_viaje_eje = models.IntegerField(blank=True, null=True)
    velocidad_eje = models.FloatField(blank=True, null=True)
    super_lento = models.IntegerField(blank=True, null=True)
    segundos_por_km_tramo = models.FloatField(blank=True, null=True)
    nobs = models.IntegerField(blank=True, null=True)
    grupo = models.CharField(max_length=200, blank=True, null=True)
    periodo15 = models.TimeField(blank=True, null=True)
    tipo_dia = models.CharField(max_length=200, blank=True, null=True)
    diferencia_referencia = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tramos_15min_uoct'
        unique_together = (('tramo', 'eje', 'dist_en_ruta'),)

class Status(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'

