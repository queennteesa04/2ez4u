"""
M1 - Data Pesanan: Array vs Linked List
Dilarang memakai dict/set/sorted/.sort()/collections/heapq/bisect.
"""

class ArrayPesanan:
    def __init__(self, kapasitas_awal=4):
        self.data = [None] * kapasitas_awal
        self.n = 0

    def __len__(self):
        return self.n

    def _grow(self):
        baru = [None] * (len(self.data) * 2)
        i = 0
        while i < self.n:
            baru[i] = self.data[i]
            i += 1
        self.data = baru

    def append(self, nilai):
        if self.n == len(self.data):
            self._grow()
        self.data[self.n] = nilai
        self.n += 1

    def insert(self, indeks, nilai):
        if indeks < 0:
            indeks = 0
        if indeks > self.n:
            indeks = self.n
        if self.n == len(self.data):
            self._grow()
        i = self.n
        while i > indeks:
            self.data[i] = self.data[i - 1]
            i -= 1
        self.data[indeks] = nilai
        self.n += 1

    def get(self, indeks):
        if indeks < 0 or indeks >= self.n:
            return None
        return self.data[indeks]

    def remove(self, indeks):
        if indeks < 0 or indeks >= self.n:
            return None
        nilai = self.data[indeks]
        i = indeks
        while i < self.n - 1:
            self.data[i] = self.data[i + 1]
            i += 1
        self.data[self.n - 1] = None
        self.n -= 1
        return nilai

    def tambah_berdasarkan_prioritas(self, pesanan):
        # 1 = VIP depan, 2 = PRIORITAS tengah, 3 = REGULER belakang.
        if pesanan.prioritas == 1:
            self.insert(0, pesanan)
        elif pesanan.prioritas == 2:
            self.insert(self.n // 2, pesanan)
        else:
            self.append(pesanan)


class Node:
    def __init__(self, nilai):
        self.nilai = nilai
        self.next = None


class LinkedListPesanan:
    def __init__(self):
        self.head = None
        self.tail = None
        self.n = 0

    def __len__(self):
        return self.n

    def append(self, nilai):
        node = Node(nilai)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.n += 1

    def insert(self, indeks, nilai):
        if indeks <= 0:
            node = Node(nilai)
            node.next = self.head
            self.head = node
            if self.tail is None:
                self.tail = node
            self.n += 1
            return

        if indeks >= self.n:
            self.append(nilai)
            return

        sebelum = self.head
        i = 1
        while i < indeks:
            sebelum = sebelum.next
            i += 1

        node = Node(nilai)
        node.next = sebelum.next
        sebelum.next = node
        self.n += 1

    def get(self, indeks):
        if indeks < 0 or indeks >= self.n:
            return None
        cur = self.head
        i = 0
        while i < indeks:
            cur = cur.next
            i += 1
        return cur.nilai

    def remove(self, indeks):
        if indeks < 0 or indeks >= self.n or self.head is None:
            return None

        if indeks == 0:
            nilai = self.head.nilai
            self.head = self.head.next
            self.n -= 1
            if self.n == 0:
                self.tail = None
            return nilai

        sebelum = self.head
        i = 1
        while i < indeks:
            sebelum = sebelum.next
            i += 1

        node = sebelum.next
        sebelum.next = node.next
        if node is self.tail:
            self.tail = sebelum
        self.n -= 1
        return node.nilai

    def tambah_berdasarkan_prioritas(self, pesanan):
        if pesanan.prioritas == 1:
            self.insert(0, pesanan)
        elif pesanan.prioritas == 2:
            self.insert(self.n // 2, pesanan)
        else:
            self.append(pesanan)


class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas,
                 t_masuk_detik, t_selesai_detik, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk_detik = t_masuk_detik
        self.t_selesai_detik = t_selesai_detik
        self.status = status

    def __repr__(self):
        return (
            self.oid + " | " + self.menu + " | Rp" + str(self.harga)
            + " | P" + str(self.prioritas) + " | " + self.status
        )


def baca_csv(path, batas=None):
    import csv
    hasil = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if batas is not None and len(hasil) >= batas:
                break
            selesai = None if row[7] == "" else int(float(row[7]))
            hasil.append(
                Pesanan(
                    row[0], row[1], row[2], row[3], int(row[4]), int(row[5]),
                    int(row[6]), selesai, row[8]
                )
            )
    return hasil


def isi_dua_struktur(data):
    arr = ArrayPesanan(max(4, len(data)))
    linked = LinkedListPesanan()
    i = 0
    while i < len(data):
        arr.append(data[i])
        linked.append(data[i])
        i += 1
    return arr, linked
