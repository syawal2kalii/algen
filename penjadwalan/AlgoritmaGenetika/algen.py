import penjadwalan.models as datadb
from penjadwalan.AlgoritmaGenetika.classes import *
from math import ceil, log2

cpg = []
lts = []
slots = []
max_score = None
bits_needed_backup_store = {}


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
    # cpg =  [
    #   '000000000000',
    #   '000100010001',
    #   '001000100010',
    #   '001100110011',
    #   '010001000100',
    #   '010100000101',
    #   '000000000000',
    #   '000000000000',
    #   '000000000000',
    #   '000000000000',
    #   '000000000000',
    #   '000000000000']

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


def algo():
    print("#0 Algoritma Genetika Mulai")
    # inisialisasi()
    generation = 0
    convert_input_to_bin()
