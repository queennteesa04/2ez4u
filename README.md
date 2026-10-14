# 2EZ4U APP

Ini adalah proyek Python untuk mata kuliah Struktur Data & Analisa Algoritma (EC234303). Aplikasi ini dibuat untuk mengelola data pesanan sederhana, mulai dari melihat dan menambah pesanan sampai mencoba antrean, sorting, dan searching.

## Yang sudah dibuat

- **M1:** Array dan Linked List untuk menyimpan data pesanan.
- **M2:** Queue, circular queue, stack untuk menghitung total belanja, serta fitur undo dan redo.
- **M3:** Insertion Sort, Merge Sort, Linear Search, dan Binary Search.
- **Frontend:** Tampilan sederhana menggunakan Tkinter.

Data yang dipakai ada di folder `data`, yaitu `pesanan.csv` dan `peta.csv`.

## Struktur folder

```text
2ez4u/
├── app.py
├── README.md
├── data/
│   ├── pesanan.csv
│   └── peta.csv
├── backend/
│   ├── __init__.py
│   ├── m1_pesanan.py
│   ├── m2_antrean.py
│   └── m3_laporan.py
├── frontend/
│   └── ui.py
└── tests/
    └── test_m1_m2.py
```

## Cara menjalankan

Pastikan Python sudah terpasang. Setelah itu, buka terminal di folder proyek dan jalankan:

```bash
python app.py
```

Nanti akan muncul tampilan aplikasi. Pilih fitur di bagian menu, isi kolom input sesuai petunjuk, lalu tekan tombol **Jalankan**.

Untuk menjalankan pengujian:

```bash
python tests/test_m1_m2.py
```

Kalau pengujian berhasil, pesan terakhirnya adalah:

```text
SEMUA TEST M1-M3 LULUS
```

## Fitur M1 - Data pesanan

Di bagian M1, data pesanan disimpan menggunakan Array dan Linked List. Beberapa operasi yang tersedia adalah melihat pesanan, menambah pesanan reguler, prioritas, atau VIP, serta menghapus pesanan berdasarkan indeks.

Pada menu lihat pesanan, kolom input bisa dikosongkan untuk melihat ringkasan dan 20 pesanan pertama. Kalau ingin melihat pesanan tertentu, masukkan indeksnya, misalnya `0`.

## Fitur M2 - Antrean dan kasir

M2 berisi implementasi queue biasa dan circular queue. Keduanya dipakai untuk mencoba proses masuk dan keluarnya data dari antrean.

Ada juga fitur perhitungan total belanja menggunakan stack. Contoh ekspresi yang bisa dicoba:

```text
( 3 * 12000 ) + ( 2 * 8500 ) - 5000
```

Ekspresi tersebut diubah ke bentuk postfix sebelum dihitung, dengan hasil `48000` atau Rp48.000.

Fitur undo dan redo digunakan untuk membatalkan aksi sebelumnya atau mengembalikan aksi yang dibatalkan.

## Fitur M3 - Sorting dan searching

M3 berisi dua algoritma sorting dan dua algoritma searching:

- **Insertion Sort:** mengurutkan data satu per satu. Di frontend, jumlah data dibatasi sampai 20.000 agar prosesnya tidak terlalu lama.
- **Merge Sort:** membagi data menjadi beberapa bagian lalu menggabungkan hasil yang sudah terurut. Bisa digunakan untuk seluruh data pesanan.
- **Linear Search:** mencari ID pesanan dengan memeriksa data satu per satu.
- **Binary Search:** mencari ID pada data yang sudah diurutkan berdasarkan ID.
- **Bandingkan Sort:** membandingkan hasil Insertion Sort dan Merge Sort menggunakan sampel data yang sama.

Kolom input M3 bisa diisi seperti contoh berikut:

| Menu | Contoh input |
|---|---|
| Insertion Sort | `10,harga` |
| Merge Sort | `semua,harga` |
| Bandingkan Sort | `2000,harga` |
| Linear Search | `O-000002` |
| Binary Search | `O-000002` |

Untuk sorting, pilihan kolomnya adalah `oid`, `harga`, atau `selesai`.

## Catatan

Untuk tugas ini, beberapa struktur data dan algoritma dibuat sendiri agar prosesnya bisa dipelajari dan dibandingkan. Implementasi juga mengikuti batasan dari petunjuk proyek, jadi tidak menggunakan beberapa fungsi bawaan seperti `sorted()`, `.sort()`, `heapq`, `bisect`, dan `collections`.

README ini masih bisa dilengkapi lagi dengan screenshot aplikasi, hasil pengujian, dan video demo setelah semuanya siap untuk dikumpulkan.
