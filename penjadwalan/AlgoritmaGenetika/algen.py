import penjadwalan.models as datadb
from penjadwalan.AlgoritmaGenetika.classes import *
import sys

# from penjadwalan.views import deinisialisasi
from math import ceil, log2
import random

cpg = []
lts = []
slots = []
max_score = None
bits_needed_backup_store = {}


def deinisialisasi():
    Group.groups = []
    Professor.professors = []
    CourseClass.classes = []
    Room.rooms = []
    Slot.slots = []


def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():
    print("#1 convert input to bin")
    global cpg, lts, slots, max_score

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
    max_chromosomes = 0
    for a in range(len(semester_tersedia)):
        max_chromosomes += len(
            datadb.Group.objects.filter(semester=semester_tersedia[a])
        ) * len(datadb.Mata_kuliah.objects.filter(semester=semester_tersedia[a]))
    print("#1.1 Max Chromosomes =", max_chromosomes)

    # deinisialisasi()

    # generate random gen jika di butuhkan
    if len(Professor.professors) != max_chromosomes:
        selisih = max_chromosomes - int(len(Professor.professors))
        for i in range(selisih):
            Professor.professors.append(Professor.professors[0])

    if len(CourseClass.classes) != max_chromosomes:
        selisih = max_chromosomes - int(len(CourseClass.classes))
        for i in range(selisih):
            CourseClass.classes.append(CourseClass.classes[0])

    if len(Group.groups) != max_chromosomes:
        selisih = max_chromosomes - int(len(Group.groups))
        for i in range(selisih):
            Group.groups.append(Group.groups[0])
    print("#1.1 len setiap class berubah menjadi ", max_chromosomes)
    # generate cpg = 0000000000,0000000
    # chromosome cpg id = [
    #   0, 0, 0,
    #   1, 1, 1,
    #   2, 2, 2,
    #   3, 3, 3,
    #   4, 4, 4,
    #   5, 0, 5,
    #   0, 0, 0,
    #   0, 0, 0,
    #   0, 0, 0,
    #   0, 0, 0,
    #   0, 0, 0,
    #   0, 0, 0
    # ]
    cpg = []
    for i in range(
        max(len(CourseClass.classes), len(Professor.professors), len(Group.groups))
    ):
        cpg.extend(
            [
                CourseClass.find(CourseClass.classes[i].code),  # return 0/1
                Professor.find(Professor.professors[i].name),
                Group.find(Group.groups[i].name),
            ]
        )

    print("#1.2 chromosome cpg id =", cpg)
    print("#1.2 len course class", len(CourseClass.classes))
    print("len bits needed ", bits_needed(CourseClass.classes))
    for _c in range(len(cpg)):
        if _c % 3 == 0:
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), "0")
        elif _c % 3 == 1:
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), "0")
        else:
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), "0")

    print("#1.3 chromosomes cpg binary =", cpg)
    # 1.3 chromosomes cpg binary = [
    #   '0000', '0000', '0000',
    #   '0001', '0001', '0001',
    #   '0010', '0010', '0010',
    #   '0011', '0011', '0011',
    #   '0100', '0100', '0100',
    #   '0101', '0000', '0101',
    #   '0000', '0000', '0000',
    #   '0000', '0000', '0000',
    #   '0000', '0000', '0000',
    #   '0000', '0000', '0000',
    #   '0000', '0000', '0000',
    #   '0000', '0000', '0000']
    #

    cpg = join_cpg_pair(cpg)
    print("#1.4 cpg pair ", cpg)
    cpg = [
        "000000000000",
        "000100010001",
        "001000100010",
        "001100110011",
        "010001000100",
        "010100000101",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
    ]

    # 0 -> 0b0 -> .......000000
    # 1 -> 0b1 -> .......000001
    # 2 -> 0b10 -> ......000010
    for r in range(len(Room.rooms)):
        # print("bin(r)", bin(r))
        # print("bin(r)[2:]=", bin(r)[2:])
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), "0"))
    print("#1.5.1 lts", lts)

    for t in range(len(Slot.slots)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots), "0"))
    print("#1.5.2 lts", slots)

    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3
    print("#1.6 max score =", max_score)
    # max_score = panjangcpg*jumlah aturan
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


def init_population(n):
    #
    # chromosomes : [['0000000000000000', '0001000100010111', '0010001000101000', '0011001100110011', '0100010001000110', '0101000001010000', '0000000000000001', '0000000000000111', '0000000000000010', '0000000000001001', '0000000000000101', '0000000000000100']]
    # chromosomes : [
    #                ['0000000000000000', '0001000100010111', '0010001000101000', '0011001100110011', '0100010001000110', '0101000001010000', '0000000000000001', '0000000000000111', '0000000000000010', '0000000000001001', '0000000000000101', '0000000000000100'],
    #                ['0000000000000100', '0001000100011000', '0010001000101000', '0011001100111010', '0100010001000000', '0101000001011011', '0000000000000111', '0000000000000010', '0000000000001001', '0000000000001001', '0000000000001010', '0000000000000110']
    #               ]
    # chromosomes : [
    #               ['0000000000000000', '0001000100010111', '0010001000101000', '0011001100110011', '0100010001000110', '0101000001010000', '0000000000000001', '0000000000000111', '0000000000000010', '0000000000001001', '0000000000000101', '0000000000000100'],
    #               ['0000000000000100', '0001000100011000', '0010001000101000', '0011001100111010', '0100010001000000', '0101000001011011', '0000000000000111', '0000000000000010', '0000000000001001', '0000000000001001', '0000000000001010', '0000000000000110'],
    #               ['0000000000000111', '0001000100010001', '0010001000100011', '0011001100110011', '0100010001000000', '0101000001011000', '0000000000000100', '0000000000001001', '0000000000001011', '0000000000000101', '0000000000000011', '0000000000000101']
    #               ]
    # #
    print("##2.1 init population ({})".format(n))
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
        print("chromosomes :", chromosomes)
    return chromosomes


def waktu_bits(chromosome):
    i = (
        bits_needed(CourseClass.classes)
        + bits_needed(Professor.professors)
        + bits_needed(Group.groups)
    )
    return chromosome[i : i + bits_needed(Slot.slots)]


def pengajar_bits(chromosome):
    i = bits_needed(CourseClass.classes)
    # return ....
    return chromosome[i : i + bits_needed(Professor.professors)]


def waktu_bentrok(a, b):
    if waktu_bits(a) == waktu_bits(b):
        return 1
    return 0


def ruangan_bits(chromosome):
    # return letak chromosomes ruangan_bits -> chromosome[14:16] (2 terakhir)
    i = (
        bits_needed(CourseClass.classes)
        + bits_needed(Professor.professors)
        + bits_needed(Group.groups)
        + bits_needed(Slot.slots)
    )
    return chromosome[i : i + bits_needed(Room.rooms)]


def gunakan_ruangan_kosong(chromosome):
    scores = 0
    print(chromosome)
    print(len(chromosome) - 1)
    for i in range(len(chromosome) - 1):
        clash = False
        for j in range(i + 1, len(chromosome)):
            # if j == 1 and i == 1:
            #     sys.exit()
            # untuk melihat yang di cocokkan
            # print("chromosome[i]", chromosome[i], " nilai i", i)
            # print("chromosome[i]", chromosome[j], " nilai j", j)
            if waktu_bentrok(chromosome[i], chromosome[j]) and ruangan_bits(
                chromosome[i]
            ) == ruangan_bits(chromosome[j]):
                # melihat cromosome yang clash / bertabrakan
                # print("clash true")
                # print("chromosome[i]", chromosome[i], " nilai i", i)
                # print("chromosome[j]", chromosome[j], " nilai j", j)
                clash = True
        if not clash:
            # print("score +1")
            scores = scores + 1
            # print("nilai score chromosome/populasi ke ", i, " ", scores)
        # if j == 2 and i == 2:
        #     sys.exit()
    # print("nilai score keseluruhan:", scores)
    return scores


def pengajar_tidak_bersamaan(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):
        clash = False
        for j in range(i + 1, len(chromosome)):
            if waktu_bentrok(chromosome[i], chromosome[j]) and pengajar_bits(
                chromosome[i]
            ) == pengajar_bits(chromosome[j]):
                print("clash true")
                print("chromosome[i]", chromosome[i], " nilai i", i)
                print("chromosome[j]", chromosome[j], " nilai j", j)
                clash = True
        if not clash:
            scores = scores + 1
    return scores


def evaluate(chromosomes):
    # gunakan_ruangan_kosong (use_spare_classroom)
    # pengajar_mengajar_tdk_bersamaan (fakulty_member_one_class)
    # penyesuaian_size_ruangan
    # kelas_tidak_bertabrakan_dengan_kelas_lain
    # cek_matkul_lab_mendapatkan_ruangan_lab
    # jadwal_lab_sesuai_dengan_waktu_lab
    global max_score
    score = 0
    score = score + gunakan_ruangan_kosong(chromosomes)
    print("##evaluate score gunakan ruangan kosong", score)
    score = score + pengajar_tidak_bersamaan(chromosomes)
    print("##evaluate score pengajar_tidak_bersamaan", score)
    # print("score :", score)
    # sys.exit()
    return score / max_score


def crossover(population):
    print("3.0 Crossover")
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))
    population.append(population[a][:cut] + population[b][cut:])


def algo():
    print("#0 Algoritma Genetika Mulai")
    # inisialisasi()
    generation = 0
    convert_input_to_bin()
    # population = init_population(3)
    population = [
        [
            "0000000000000000",
            "0001000100010111",
            "0010001000101000",
            "0011001100110011",
            "0100010001000110",
            "0101000001010000",
            "0000000000000001",
            "0000000000000111",
            "0000000000000010",
            "0000000000001001",
            "0000000000000101",
            "0000000000000100",
        ],
        [
            "0000000000000100",
            "0001000100011000",
            "0010001000101000",
            "0011001100111010",
            "0100010001000000",
            "0101000001011011",
            "0000000000000111",
            "0000000000000010",
            "0000000000001001",
            "0000000000001001",
            "0000000000001010",
            "0000000000000110",
        ],
        [
            "0000000000000111",
            "0001000100010001",
            "0010001000100011",
            "0011001100110011",
            "0100010001000000",
            "0101000001011000",
            "0000000000000100",
            "0000000000001001",
            "0000000000001011",
            "0000000000000101",
            "0000000000000011",
            "0000000000000101",
        ],
    ]

    print("\n----------Algoritma Genetika ------------")
    while True:
        if evaluate(max(population, key=evaluate)) == 1 or generation == 500:
            print("generation :", generation)
            print(
                "best chromosome fitness value",
                evaluate(max(population, key=evaluate)),
            )
            print("Best Chromosome: ", max(population, key=evaluate))

        else:
            print("generation ke  :", generation)
            # print(
            #     "best chromosome fitness value sementara",
            #     evaluate(max(population, key=evaluate)),
            # )
            # sys.exit()
            for _c in range(len(population)):
                crossover(population)
        sys.exit()
