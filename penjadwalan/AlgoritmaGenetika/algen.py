import penjadwalan.models as datadb

cpg = []
lts = []
slots = []
max_score = None


def convert_input_to_bin():
    print("#1 convert input to bin")
    global cpg, lts, slots, max_score

    gruopsemester = datadb.Group.objects.values_list(
        "semester", flat=True
    ).distinct()  # type list

    matkulsemester = datadb.Mata_kuliah.objects.values_list(
        "semester", flat=True
    ).distinct()  # type list

    semester_tersedia = list(
        set.union(set(gruopsemester), set(matkulsemester))
    )  # type list

    panjang_chromosomes = 0
    for a in range(len(semester_tersedia)):
        panjang_chromosomes += len(
            datadb.Group.objects.filter(semester=semester_tersedia[a])
        ) * len(datadb.Mata_kuliah.objects.filter(semester=semester_tersedia[a]))

    """
    banyak group semester unique = 1,3,5
    banyak matkul semester unique = 1,3,5
    semester tersedia = 1,3,5

    panjangchromosome = banyakgroup di semester [0]+[1]+[2] * n matkul semester [0,3,5]

    pjgc
    for a in range(len(semester_tersedia)) :
        pjgc += len(Group.objects.get(semester=semester_tersedia[a]))*len(Matkul.objects.get(semester=semester_tersedia[a]))

    getgroupbysemesterunique
    group semester = 3 (2018,2019,2020)
    matkul semester = 2  
    maksimal = 2*2 3*
    """


def algo():
    print("#0 Algoritma Genetika Mulai")
    generation = 0
    convert_input_to_bin()
