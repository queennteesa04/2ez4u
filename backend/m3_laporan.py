"""
M3 - Sorting dan searching pesanan.
"""


def nilai_kunci(pesanan, kunci):
    if kunci == "oid":
        return pesanan.oid
    if kunci == "harga":
        return pesanan.harga
    if kunci == "selesai":
        if pesanan.t_selesai_detik is None:
            return -1
        return pesanan.t_selesai_detik
    raise ValueError("Kunci harus oid, harga, atau selesai")


def insertion_sort(data, kunci="selesai"):
    hasil = []
    i = 0
    while i < len(data):
        hasil.append(data[i])
        i += 1
    perbandingan = 0
    pemindahan = 0
    i = 1
    while i < len(hasil):
        item = hasil[i]
        key_item = nilai_kunci(item, kunci)
        j = i - 1
        while j >= 0:
            perbandingan += 1
            if nilai_kunci(hasil[j], kunci) > key_item:
                hasil[j + 1] = hasil[j]
                pemindahan += 1
                j -= 1
            else:
                break
        hasil[j + 1] = item
        pemindahan += 1
        i += 1
    return hasil, perbandingan, pemindahan


def merge_sort(data, kunci="selesai"):
    sumber = []
    i = 0
    while i < len(data):
        sumber.append(data[i])
        i += 1
    target = [None] * len(sumber)
    lebar = 1
    perbandingan = 0
    pemindahan = 0
    n = len(sumber)
    while lebar < n:
        awal = 0
        while awal < n:
            tengah = awal + lebar
            akhir = awal + 2 * lebar
            if tengah > n:
                tengah = n
            if akhir > n:
                akhir = n
            kiri = awal
            kanan = tengah
            keluar = awal
            while kiri < tengah and kanan < akhir:
                perbandingan += 1
                if nilai_kunci(sumber[kiri], kunci) <= nilai_kunci(sumber[kanan], kunci):
                    target[keluar] = sumber[kiri]
                    kiri += 1
                else:
                    target[keluar] = sumber[kanan]
                    kanan += 1
                keluar += 1
                pemindahan += 1
            while kiri < tengah:
                target[keluar] = sumber[kiri]
                kiri += 1
                keluar += 1
                pemindahan += 1
            while kanan < akhir:
                target[keluar] = sumber[kanan]
                kanan += 1
                keluar += 1
                pemindahan += 1
            awal += 2 * lebar
        sumber, target = target, sumber
        lebar *= 2
    return sumber, perbandingan, pemindahan


def linear_search(data, target_oid):
    perbandingan = 0
    i = 0
    while i < len(data):
        perbandingan += 1
        if data[i].oid == target_oid:
            return i, perbandingan
        i += 1
    return -1, perbandingan


def binary_search(data_terurut_oid, target_oid):
    kiri = 0
    kanan = len(data_terurut_oid) - 1
    perbandingan = 0
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        perbandingan += 1
        oid_tengah = data_terurut_oid[tengah].oid
        if oid_tengah == target_oid:
            return tengah, perbandingan
        perbandingan += 1
        if oid_tengah < target_oid:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1, perbandingan
