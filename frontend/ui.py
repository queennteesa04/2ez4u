import tkinter as tk
from tkinter import messagebox
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.m1_pesanan import baca_csv, ArrayPesanan, LinkedListPesanan, Pesanan
from backend.m2_antrean import evaluasi_kasir, jejak_ke_postfix, jejak_hitung_postfix, AntreanNaif, AntreanMelingkar, UndoRedoQueue
from backend.m3_laporan import insertion_sort, merge_sort, linear_search, binary_search

MENU_HINTS = {
    "M1 - Lihat Pesanan": "Kosongkan untuk ringkasan 20 pesanan pertama, atau isi indeks, mis. 0",
    "M1 - Tambah REGULER": "O-TEST-001,Budi,kafe-teknik,nasi-goreng,25000",
    "M1 - Tambah PRIORITAS": "O-TEST-002,Andi,kafe-teknik,ayam-geprek,30000",
    "M1 - Tambah VIP": "O-TEST-003,Sinta,kafe-teknik,steak,50000",
    "M1 - Hapus Indeks": "0",
    "M2 - Kasir Postfix": "( 3 * 12000 ) + ( 2 * 8500 ) - 5000",
    "M2 - Queue Enqueue": "0",
    "M2 - Queue Dequeue": "1",
    "M2 - Undo": "(tidak perlu input)",
    "M2 - Redo": "(tidak perlu input)",
    "M2 - Statistik": "(tidak perlu input)",
    "M3 - Insertion Sort": "10,harga  |  jumlah maksimal 20000; kunci: oid/harga/selesai",
    "M3 - Merge Sort": "semua,harga  |  atau mis. 2000,selesai; kunci: oid/harga/selesai",
    "M3 - Bandingkan Sort": "2000,harga  |  jumlah maksimal 20000; kunci: oid/harga/selesai",
    "M3 - Linear Search": "O-000002",
    "M3 - Binary Search": "O-000002",
}


def format_pesanan(p):
    if p is None:
        return "(pesanan tidak ditemukan)"
    selesai = "belum selesai" if p.t_selesai_detik is None else str(p.t_selesai_detik)
    return (f"{p.oid} | pelanggan={p.pelanggan} | resto={p.resto} | menu={p.menu} | "
            f"harga=Rp{p.harga:,} | prioritas={p.prioritas} | selesai={selesai} | status={p.status}")


class App:
    def __init__(self, master):
        self.master = master
        master.title("2EZ4U APP - M1, M2, M3")
        master.geometry("1120x720")

        self.data = baca_csv(ROOT / "data" / "pesanan.csv")
        self.array = ArrayPesanan(max(4, len(self.data)))
        self.linked = LinkedListPesanan()
        i = 0
        while i < len(self.data):
            self.array.append(self.data[i])
            self.linked.append(self.data[i])
            i += 1

        antre = []
        i = 0
        while i < len(self.data):
            if self.data[i].status == "ANTRE":
                antre.append(self.data[i])
            i += 1
        self.naif = AntreanNaif(antre)
        self.circular = AntreanMelingkar(max(8, len(antre) * 2))
        i = 0
        while i < len(antre):
            self.circular.enqueue(antre[i])
            i += 1
        self.history = UndoRedoQueue(self.circular)

        left = tk.Frame(master)
        left.pack(side="left", fill="y", padx=8, pady=8)
        tk.Label(left, text="Pilih fitur", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.menu = tk.Listbox(left, width=32, height=27, exportselection=False)
        self.menu.pack(side="left", fill="y")
        scrollbar = tk.Scrollbar(left, command=self.menu.yview)
        scrollbar.pack(side="right", fill="y")
        self.menu.config(yscrollcommand=scrollbar.set)
        self.menu_items = list(MENU_HINTS.keys())
        for item in self.menu_items:
            self.menu.insert(tk.END, item)
        self.menu.bind("<<ListboxSelect>>", self.menu_changed)

        right = tk.Frame(master)
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        self.label = tk.Label(right, text="Pilih menu di sebelah kiri", anchor="w", font=("Segoe UI", 11, "bold"))
        self.label.pack(fill="x")
        self.hint = tk.Label(right, text="Petunjuk input akan tampil di sini.", anchor="w", fg="#555555")
        self.hint.pack(fill="x", pady=(2, 4))
        self.entry = tk.Entry(right, font=("Consolas", 10))
        self.entry.pack(fill="x", pady=4)
        tk.Button(right, text="Jalankan", command=self.run, width=16).pack(anchor="w", pady=4)
        self.output = tk.Text(right, height=30, wrap="word", font=("Consolas", 9))
        self.output.pack(fill="both", expand=True, pady=8)
        self.log(f"Data dimuat: {len(self.data):,} pesanan. Pilih fitur di kiri, lalu tekan Jalankan.")
        self.menu.selection_set(0)
        self.menu_changed()

    def log(self, text):
        self.output.insert(tk.END, str(text) + "\n")
        self.output.see(tk.END)

    def menu_changed(self, event=None):
        selection = self.menu.curselection()
        if not selection:
            return
        pilihan = self.menu.get(selection[0])
        self.label.config(text=pilihan)
        self.hint.config(text=MENU_HINTS.get(pilihan, ""))
        self.entry.delete(0, tk.END)
        # Untuk fitur yang tidak butuh input, kolom dibiarkan kosong.
        if pilihan not in ("M1 - Lihat Pesanan", "M2 - Undo", "M2 - Redo", "M2 - Statistik"):
            self.entry.insert(0, MENU_HINTS[pilihan].split("  |")[0])
        self.entry.focus_set()

    def _pesanan_saat_ini(self):
        hasil = []
        i = 0
        while i < len(self.array):
            hasil.append(self.array.get(i))
            i += 1
        return hasil

    def _parse_sort_input(self, text, default_count, default_key):
        text = text.strip()
        if text == "":
            return default_count, default_key
        parts = text.split(",")
        if len(parts) != 2:
            raise ValueError("Format input: jumlah,kunci. Contoh: 2000,harga")
        jumlah_text = parts[0].strip().lower()
        kunci = parts[1].strip().lower()
        if kunci not in ("oid", "harga", "selesai"):
            raise ValueError("Kunci harus oid, harga, atau selesai")
        jumlah = None if jumlah_text in ("semua", "all", "full") else int(jumlah_text)
        if jumlah is not None and jumlah < 0:
            raise ValueError("Jumlah tidak boleh negatif")
        return jumlah, kunci

    def run(self):
        selection = self.menu.curselection()
        if not selection:
            messagebox.showinfo("Info", "Pilih menu terlebih dahulu.")
            return
        pilihan = self.menu.get(selection[0])
        teks = self.entry.get().strip()
        mulai = time.perf_counter()
        try:
            if pilihan == "M1 - Lihat Pesanan":
                if teks == "":
                    self.log(f"Total pesanan di Array: {len(self.array):,}")
                    self.log(f"Total pesanan di Linked List: {len(self.linked):,}")
                    batas = min(20, len(self.array))
                    i = 0
                    while i < batas:
                        self.log(f"[{i}] {format_pesanan(self.array.get(i))}")
                        i += 1
                    if len(self.array) > batas:
                        self.log(f"... {len(self.array) - batas:,} pesanan lainnya tidak ditampilkan. Isi kolom dengan indeks untuk melihat satu pesanan.")
                else:
                    indeks = int(teks)
                    if indeks < 0 or indeks >= len(self.array):
                        raise ValueError(f"Indeks harus antara 0 dan {len(self.array) - 1}")
                    self.log(f"Indeks {indeks} — Array : {format_pesanan(self.array.get(indeks))}")
                    self.log(f"Indeks {indeks} — Linked: {format_pesanan(self.linked.get(indeks))}")

            elif pilihan.startswith("M1 - Tambah"):
                parts = [x.strip() for x in teks.split(",")]
                if len(parts) != 5 or any(x == "" for x in parts):
                    raise ValueError("Format: oid,pelanggan,resto,menu,harga")
                prioritas = 3
                if "PRIORITAS" in pilihan:
                    prioritas = 2
                elif "VIP" in pilihan:
                    prioritas = 1
                p = Pesanan(parts[0], parts[1], parts[2], parts[3], int(parts[4]), prioritas, 0, None, "ANTRE")
                self.array.tambah_berdasarkan_prioritas(p)
                self.linked.tambah_berdasarkan_prioritas(p)
                self.log("Pesanan berhasil ditambahkan ke Array dan Linked List:")
                self.log(format_pesanan(p))

            elif pilihan == "M1 - Hapus Indeks":
                indeks = int(teks)
                a = self.array.remove(indeks)
                l = self.linked.remove(indeks)
                if a is None or l is None:
                    raise ValueError("Indeks tidak valid atau data tidak ditemukan")
                self.log("Berhasil menghapus dari kedua struktur:")
                self.log("Array : " + format_pesanan(a))
                self.log("Linked: " + format_pesanan(l))

            elif pilihan == "M2 - Kasir Postfix":
                postfix, jejak_konversi = jejak_ke_postfix(teks)
                total, jejak_evaluasi = jejak_hitung_postfix(postfix)
                self.log("INfix: " + teks)
                self.log("\nTAHAP 1 - KONVERSI INFIX KE POSTFIX")
                self.log(f"{'Token':<10} {'Tindakan':<55} {'Stack operator':<22} Keluaran")
                self.log("-" * 120)
                for token, tindakan, stack, keluaran in jejak_konversi:
                    self.log(f"{token:<10} {tindakan:<55} {stack:<22} {keluaran}")
                self.log("\nPostfix akhir: " + " ".join(postfix))
                self.log("\nTAHAP 2 - EVALUASI POSTFIX")
                self.log(f"{'Token':<10} {'Tindakan':<55} Stack nilai")
                self.log("-" * 100)
                for token, tindakan, stack in jejak_evaluasi:
                    self.log(f"{token:<10} {tindakan:<55} {stack}")
                self.log("TOTAL: Rp" + format(total, ",.0f").replace(",", "."))

            elif pilihan == "M2 - Queue Enqueue":
                indeks = int(teks)
                if indeks < 0 or indeks >= len(self.data):
                    raise ValueError(f"Indeks harus antara 0 dan {len(self.data) - 1}")
                p = self.data[indeks]
                self.naif.enqueue(p)
                self.history.enqueue(p)
                self.log("Enqueue: " + p.oid)
                self.log(f"Naif={len(self.naif)} | Circular={len(self.history.antrean)}")

            elif pilihan == "M2 - Queue Dequeue":
                jumlah = int(teks)
                if jumlah < 1:
                    raise ValueError("Jumlah dequeue harus minimal 1")
                i = 0
                while i < jumlah:
                    self.naif.dequeue()
                    i += 1
                keluar = self.history.dequeue_many(jumlah)
                self.log(f"Dequeued: {len(keluar)} pesanan")
                self.log(f"Geseran naif total: {self.naif.total_geseran}")

            elif pilihan == "M2 - Undo":
                self.log("Undo berhasil: " + str(self.history.undo_last()))
            elif pilihan == "M2 - Redo":
                self.log("Redo berhasil: " + str(self.history.redo_last()))
            elif pilihan == "M2 - Statistik":
                undo, redo = self.history.history()
                self.log(f"Naif: {len(self.naif)} | Circular: {len(self.history.antrean)}")
                self.log(f"Kapasitas circular: {len(self.history.antrean.data)}")
                self.log(f"Geseran naif total: {self.naif.total_geseran}")
                self.log(f"Undo depth: {undo} | Redo depth: {redo}")

            elif pilihan in ("M3 - Insertion Sort", "M3 - Merge Sort", "M3 - Bandingkan Sort"):
                default_count = 10 if pilihan == "M3 - Insertion Sort" else (2000 if pilihan == "M3 - Bandingkan Sort" else None)
                default_key = "harga"
                jumlah, kunci = self._parse_sort_input(teks, default_count, default_key)
                semua = self._pesanan_saat_ini()
                if jumlah is None:
                    jumlah = len(semua)
                if jumlah > len(semua):
                    raise ValueError(f"Jumlah maksimal saat ini {len(semua)}")
                if pilihan in ("M3 - Insertion Sort", "M3 - Bandingkan Sort") and jumlah > 20000:
                    raise ValueError("Insertion sort dibatasi 20.000 pesanan. Gunakan Merge Sort untuk data penuh.")
                sampel = semua[:jumlah]
                if pilihan == "M3 - Insertion Sort":
                    hasil, comp, moves = insertion_sort(sampel, kunci)
                    self.log(f"Insertion sort | jumlah={jumlah:,} | kunci={kunci}")
                    self.log(f"Perbandingan={comp:,} | pemindahan={moves:,}")
                    for i in range(min(20, len(hasil))):
                        self.log(f"[{i}] {format_pesanan(hasil[i])}")
                elif pilihan == "M3 - Merge Sort":
                    hasil, comp, moves = merge_sort(sampel, kunci)
                    self.log(f"Merge sort | jumlah={jumlah:,} | kunci={kunci}")
                    self.log(f"Perbandingan={comp:,} | pemindahan={moves:,}")
                    for i in range(min(20, len(hasil))):
                        self.log(f"[{i}] {format_pesanan(hasil[i])}")
                    if len(hasil) > 20:
                        self.log(f"... {len(hasil) - 20:,} baris lainnya sudah diurutkan tetapi tidak ditampilkan.")
                else:
                    hasil_i, comp_i, moves_i = insertion_sort(sampel, kunci)
                    hasil_m, comp_m, moves_m = merge_sort(sampel, kunci)
                    identik = len(hasil_i) == len(hasil_m)
                    i = 0
                    while identik and i < len(hasil_i):
                        if hasil_i[i].oid != hasil_m[i].oid:
                            identik = False
                        i += 1
                    self.log(f"Bandingkan sort | jumlah={jumlah:,} | kunci={kunci}")
                    self.log(f"Insertion: perbandingan={comp_i:,} | pemindahan={moves_i:,}")
                    self.log(f"Merge    : perbandingan={comp_m:,} | pemindahan={moves_m:,}")
                    self.log("Hasil identik baris demi baris: " + ("YA" if identik else "TIDAK"))

            elif pilihan == "M3 - Linear Search":
                target = teks.upper()
                idx, comp = linear_search(self._pesanan_saat_ini(), target)
                self.log(f"Linear search target={target}")
                self.log(f"Indeks={idx} | perbandingan={comp:,}")
                if idx >= 0:
                    self.log(format_pesanan(self.array.get(idx)))
                else:
                    self.log("Pesanan tidak ditemukan.")

            elif pilihan == "M3 - Binary Search":
                target = teks.upper()
                data = self._pesanan_saat_ini()
                mulai_sort = time.perf_counter()
                terurut, comp_sort, moves_sort = merge_sort(data, "oid")
                waktu_sort = (time.perf_counter() - mulai_sort) * 1000
                idx, comp_search = binary_search(terurut, target)
                self.log(f"Binary search target={target}")
                self.log(f"Pembuatan daftar oid terurut: {waktu_sort:.3f} ms | perbandingan sort={comp_sort:,}")
                self.log(f"Indeks pada daftar terurut={idx} | perbandingan search={comp_search:,}")
                if idx >= 0:
                    self.log(format_pesanan(terurut[idx]))
                else:
                    self.log("Pesanan tidak ditemukan.")

            elapsed = (time.perf_counter() - mulai) * 1000
            self.log(f"[{pilihan}] {elapsed:.3f} ms")
            self.log("-" * 72)
        except (ValueError, IndexError, ZeroDivisionError) as exc:
            messagebox.showerror("Input atau operasi tidak valid", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
