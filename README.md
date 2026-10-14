# 2EZ4U APP

proyek Struktur Data & Analisa Algoritma. Aplikasi engine backend layanan antar makanan/barang

## Progress proyek

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

## Fitur M1 - Data pesanan

Di bagian M1, data pesanan disimpan menggunakan Array dan Linked List. Beberapa operasi yang tersedia adalah melihat pesanan, menambah pesanan reguler, prioritas, atau VIP, serta menghapus pesanan berdasarkan indeks.

Pada menu lihat pesanan, kolom input bisa dikosongkan untuk melihat ringkasan dan 20 pesanan pertama. jika ingin melihat pesanan tertentu, masukkan indeksnya, misalnya `0`.

![Tambah Prioritas](screenshots/screenshot-postfix.png)

## Fitur M2 - Antrean dan kasir

M2 berisi implementasi queue biasa dan circular queue. Keduanya dipakai untuk mencoba proses masuk dan keluarnya data dari antrean.

terdapat juga fitur perhitungan total belanja menggunakan stack. Contoh ekspresi yang bisa dicoba:

```text
( 3 * 12000 ) + ( 2 * 8500 ) - 5000
```

Ekspresi tersebut diubah dari bentuk infix ke bentuk postfix sebelum dihitung, dengan hasil `48000` atau Rp48.000.

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
