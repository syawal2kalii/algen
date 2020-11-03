from django.shortcuts import render
import penjadwalan.models as datadb
import penjadwalan.AlgoritmaGenetika.algen as algen
from penjadwalan.AlgoritmaGenetika.classes import *

# Create your views here.
def hello(request):
    return render(request, "tes.html")


def inisialisasi():
    Group.groups = []
    for group in datadb.Group.objects.all():
        Group.groups.append(
            Group(group.nama_group, int(group.semester), int(group.size))
        )

    # tambah Mata Kuliah yang di ajar
    Professor.professors = []

    for dosen in datadb.Dosen.objects.all():
        Professor.professors.append(Professor(dosen.nama_dosen))

    CourseClass.classes = []
    for course in datadb.Mata_kuliah.objects.all():
        CourseClass.classes.append(CourseClass(course.nama_matkul))

    Room.rooms = []
    for room in datadb.Ruangan.objects.all():
        Room.rooms.append(Room(room.nama_ruangan, int(room.kapasitas)))
        # Room.rooms = [Room("lab rpl", 30), Room("lab jarkom", 30)]

    Slot.slots = []
    for slot in datadb.Waktu.objects.all():
        Slot.slots.append(Slot(slot.mulai, slot.berakhir, slot.hari))


def deinisialisasi():
    Group.groups = []
    Professor.professors = []
    CourseClass.classes = []
    Room.rooms = []
    Slot.slots = []


def generate(request):
    deinisialisasi()
    inisialisasi()
    print("len course class generate:", len(CourseClass.classes))
    algen.algo()

    print("len course class :", len(CourseClass.classes))

    # groupsemester = [1,3,5]
    # matkulsemester = [1,3,5]
    # semester_tersedia = union (group semester +matkul semester)

    # gruopsemester = datadb.Group.objects.values_list(
    #     "semester", flat=True
    # ).distinct()  # type list

    # matkulsemester = datadb.Mata_kuliah.objects.values_list(
    #     "semester", flat=True
    # ).distinct()  # type list

    # semester_tersedia = list(
    #     set.union(set(gruopsemester), set(matkulsemester))
    # )  # type list

    # # panjang chromosome = jumlah grup semester 1,3,5 * jumlah matkul semester 1,3,5
    # #               EX = 2*2 (sem 1) + 2*2 (sem 3) + 2*2 sem(5) = 12

    # panjang_chromosomes = 0
    # for a in range(len(semester_tersedia)):
    #     panjang_chromosomes += len(
    #         datadb.Group.objects.filter(semester=semester_tersedia[a])
    #     ) * len(datadb.Mata_kuliah.objects.filter(semester=semester_tersedia[a]))

    # print(panjang_chromosomes)

    return render(request, "generate.html")
