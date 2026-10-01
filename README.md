# 2EZ4U APP — Milestone 1 & 2

Proyek akhir Struktur Data & Analisa Algoritma (EC234303). Implementasi Python 3.11+ untuk engine backend mini layanan antar makanan/barang.

## Cakupan saat ini

- M1: Array dan Linked List untuk data pesanan.
- M2: Stack, infix → postfix → evaluasi, queue naif, queue melingkar, undo dan redo.
- Frontend: Tkinter sederhana untuk menjalankan fitur M1–M2.
- Data: `data/pesanan.csv` (200.000 baris) dan `data/peta.csv`.

## Struktur

```text
2ez4u/
├── README.md
├── app.py
├── data/
│   ├── pesanan.csv
│   └── peta.csv
├── backend/
│   ├── __init__.py
│   ├── m1_pesanan.py
│   └── m2_antrean.py
├── frontend/
│   └── ui.py
└── tests/
    └── test_m1_m2.py
```

## Aturan implementasi

Sesuai petunjuk proyek, implementasi tidak memakai `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, atau dictionary/set comprehension. Struktur utama dibuat sendiri menggunakan list sebagai array, node linked list, stack, dan circular queue.

## Menjalankan

Python 3.11+.

```bash
python app.py
```

Untuk pengujian:

```bash
python tests/test_m1_m2.py
```

Output yang diharapkan:

```text
SEMUA TEST M1-M2 LULUS
```

## Fitur M1

1. Array - lihat pesanan
2. Linked List - lihat pesanan
3. Tambah REGULER ke belakang
4. Tambah PRIORITAS ke tengah
5. Tambah VIP ke depan
6. Hapus pesanan berdasarkan indeks

Array menggunakan kapasitas yang bertumbuh 2x ketika penuh. Linked List menyimpan `head` dan `tail`, sehingga penambahan di belakang tetap efisien.

## Fitur M2

### Stack kasir

Contoh:

```text
( 3 * 12000 ) + ( 2 * 8500 ) - 5000
```

menjadi:

```text
3 12000 * 2 8500 * + 5000 -
```

dan menghasilkan:

```text
Rp48.000
```

### Queue

Dibuat dua versi:

- `AntreanNaif`: dequeue memakai `pop(0)` dan menghitung jumlah elemen yang bergeser.
- `AntreanMelingkar`: dequeue hanya memajukan `front`, sehingga tidak perlu menggeser elemen.

### Undo/Redo

- aksi baru masuk ke stack undo;
- undo menjalankan kebalikan aksi;
- aksi yang di-undo masuk ke stack redo;
- aksi baru setelah undo mengosongkan redo.

## Kompleksitas utama

| Fitur | Struktur | Kompleksitas |
|---|---|---|
| Array get | Array | O(1) |
| Array tambah reguler | Array | amortized O(1) |
| Array tambah VIP | Array | O(n) |
| Linked List tambah reguler | Linked List + tail | O(1) |
| Linked List tambah VIP | Linked List | O(1) |
| Linked List get | Linked List | O(n) |
| Postfix | Stack | O(n) |
| Queue naif dequeue | Array | O(n) |
| Queue circular dequeue | Circular queue | O(1) |
| Undo/Redo | Stack | O(1) untuk aksi ujung |

## Catatan pengembangan

M1 dan M2 adalah fondasi. Milestone berikutnya dapat ditambahkan tanpa mengubah struktur dasar:

- M3: insertion sort, merge sort, linear search, binary search.
- M4: hash dan pencarian.
- M5: BST dan min-heap.
- M6: graf, BFS, dan Dijkstra.

## Bukti/demo yang perlu ditambahkan saat pengumpulan

Tambahkan screenshot UI, hasil test, grafik/tabel perbandingan waktu atau jumlah operasi yang diwajibkan dosen, serta video demo ke README sebelum final submission.
