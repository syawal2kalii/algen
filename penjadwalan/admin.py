from django.contrib import admin
from . import models as Models


# Register your models here.
admin.site.register(Models.Dosen)
admin.site.register(Models.Mata_kuliah)
admin.site.register(Models.Ruangan)
admin.site.register(Models.Group)
admin.site.register(Models.Waktu)
admin.site.register(Models.DosenByMatkul)
admin.site.register(Models.GroupByMatkul)
