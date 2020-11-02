from django.shortcuts import render
import penjadwalan.models as datadb
import sys

# Create your views here.
def hello(request):
    return render(request, "tes.html")


def generate(request):

    # groupsemester = [1,3,5]
    # matkulsemester = [1,3,5]
    # semester_tersedia = union (group semester +matkul semester)

    gruopsemester = datadb.Group.objects.values_list(
        "semester", flat=True
    ).distinct()  # type list

    matkulsemester = datadb.Mata_kuliah.objects.values_list(
        "semester", flat=True
    ).distinct()  # type list

    semester_tersedia = list(
        set.union(set(gruopsemester), set(matkulsemester))
    )  # type list

    # panjang chromosome = jumlah grup semester 1,3,5 * jumlah matkul semester 1,3,5
    #               EX = 2*2 (sem 1) + 2*2 (sem 3) + 2*2 sem(5) = 12

    panjang_chromosomes = 0
    for a in range(len(semester_tersedia)):
        panjang_chromosomes += len(
            datadb.Group.objects.filter(semester=semester_tersedia[a])
        ) * len(datadb.Mata_kuliah.objects.filter(semester=semester_tersedia[a]))

    # print(panjang_chromosomes)

    return render(request, "generate.html", {"group": group})
