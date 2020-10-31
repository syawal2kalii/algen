from django.db import models

# Create your models here.
class Dosen(models.Model):
    nama_dosen = models.CharField(max_length=100)
    id_dosen = models.CharField(null=True, blank=True, max_length=100)
    no_hp = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.nama_dosen


class Mata_kuliah(models.Model):
    nama_matkul = models.CharField(null=True, max_length=100)
    semester = models.CharField(max_length=50, blank=True)
    islab = models.CharField(default="0", max_length=2)
    code = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.nama_matkul


class Group(models.Model):
    nama_group = models.CharField(null=True, max_length=100)
    semester = models.CharField(null=True, max_length=50, blank=True)
    size = models.CharField(null=True, max_length=50, blank=True)

    def __str__(self):
        return self.nama_group


class Ruangan(models.Model):
    nama_ruangan = models.CharField(null=True, max_length=100)
    kapasitas = models.CharField(null=True, blank=True, max_length=5)

    def __str__(self):
        return self.nama_ruangan


class Waktu(models.Model):
    mulai = models.CharField(null=True, max_length=100)
    berakhir = models.CharField(null=True, max_length=50)
    hari = models.CharField(null=True, max_length=50)
    islab = models.BooleanField(default=False)

    def __str__(self):
        return self.mulai + " " + self.berakhir + " " + self.hari


class Asisten(models.Model):
    nama_asisten = models.CharField(null=True, max_length=100)
    nim = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.nama_asisten


class DosenByMatkul(models.Model):
    id_dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    id_matkul = models.ForeignKey(Mata_kuliah, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_dosen) + " " + str(self.id_matkul)


class AsistenByMatkul(models.Model):
    id_asisten = models.ForeignKey(Asisten, on_delete=models.CASCADE)
    id_matkul = models.ForeignKey(Mata_kuliah, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_asisten) + " " + str(self.id_matkul)


class GroupByMatkul(models.Model):
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    id_matkul = models.ForeignKey(Mata_kuliah, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_group) + "/t" + str(self.id_matkul)

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "GroupByMatkul"
        verbose_name_plural = "GroupByMatkul"