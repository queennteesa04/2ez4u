import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.m1_pesanan import baca_csv, ArrayPesanan, LinkedListPesanan
from backend.m2_antrean import (
    evaluasi_kasir, AntreanNaif, AntreanMelingkar, UndoRedoQueue
)

class App:
    def __init__(self, master):
        self.master = master
        master.title("2EZ4U APP - M1 & M2")
        master.geometry("1000x650")

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

        self.menu = tk.Listbox(master, width=34)
        self.menu.pack(side="left", fill="y", padx=8, pady=8)
        for item in [
            "M1 - Lihat Pesanan",
            "M1 - Tambah REGULER",
            "M1 - Tambah PRIORITAS",
            "M1 - Tambah VIP",
            "M1 - Hapus Indeks",
            "M2 - Kasir Postfix",
            "M2 - Queue Enqueue",
            "M2 - Queue Dequeue",
            "M2 - Undo",
            "M2 - Redo",
            "M2 - Statistik"
        ]:
            self.menu.insert(tk.END, item)
        self.menu.bind("<<ListboxSelect>>", self.menu_changed)

        right = tk.Frame(master)
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.form = tk.Frame(right)
        self.form.pack(fill="x")
        self.label = tk.Label(self.form, text="Pilih menu")
        self.label.pack(anchor="w")
        self.entry = tk.Entry(self.form, width=70)
        self.entry.pack(fill="x", pady=5)
        self.entry.insert(0, "Contoh: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000")

        tk.Button(self.form, text="Jalankan", command=self.run).pack(anchor="w")

        self.output = tk.Text(right, height=28, wrap="word")
        self.output.pack(fill="both", expand=True, pady=8)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def menu_changed(self, event=None):
        selection = self.menu.curselection()
        if selection:
            self.label.config(text=self.menu.get(selection[0]))

    def run(self):
        selection = self.menu.curselection()
        if not selection:
            messagebox.showinfo("Info", "Pilih menu terlebih dahulu.")
            return

        pilihan = self.menu.get(selection[0])
        mulai = time.perf_counter()

        try:
            if pilihan == "M1 - Lihat Pesanan":
                indeks = int(self.entry.get())
                a = self.array.get(indeks)
                l = self.linked.get(indeks)
                self.log("Array  : " + str(a))
                self.log("Linked : " + str(l))

            elif pilihan.startswith("M1 - Tambah"):
                # Format input: oid,pelanggan,resto,menu,harga
                parts = self.entry.get().split(",")
                if len(parts) != 5:
                    raise ValueError("Isi: oid,pelanggan,resto,menu,harga")
                from backend.m1_pesanan import Pesanan
                prioritas = 3
                if "PRIORITAS" in pilihan:
                    prioritas = 2
                elif "VIP" in pilihan:
                    prioritas = 1
                p = Pesanan(parts[0], parts[1], parts[2], parts[3],
                            int(parts[4]), prioritas, 0, None, "ANTRE")
                self.array.tambah_berdasarkan_prioritas(p)
                self.linked.tambah_berdasarkan_prioritas(p)
                self.log("Ditambahkan ke kedua struktur: " + str(p))

            elif pilihan == "M1 - Hapus Indeks":
                indeks = int(self.entry.get())
                a = self.array.remove(indeks)
                l = self.linked.remove(indeks)
                self.log("Array hapus  : " + str(a))
                self.log("Linked hapus : " + str(l))

            elif pilihan == "M2 - Kasir Postfix":
                ekspresi = self.entry.get()
                postfix, total = evaluasi_kasir(ekspresi)
                self.log("Infix   : " + ekspresi)
                self.log("Postfix : " + " ".join(postfix))
                self.log("TOTAL   : Rp" + format(total, ",.0f").replace(",", "."))

            elif pilihan == "M2 - Queue Enqueue":
                # Input sederhana memakai indeks pesanan dari data.
                indeks = int(self.entry.get())
                p = self.data[indeks]
                self.naif.enqueue(p)
                self.history.enqueue(p)
                self.log("Enqueue: " + p.oid)
                self.log("Naif=" + str(len(self.naif)) + " Circular=" + str(len(self.history.antrean)))

            elif pilihan == "M2 - Queue Dequeue":
                jumlah = int(self.entry.get())
                i = 0
                while i < jumlah:
                    self.naif.dequeue()
                    i += 1
                keluar = self.history.dequeue_many(jumlah)
                self.log("Keluar: " + str(len(keluar)) + " pesanan")
                self.log("Geseran naif total: " + str(self.naif.total_geseran))

            elif pilihan == "M2 - Undo":
                self.log("Undo berhasil: " + str(self.history.undo_last()))
            elif pilihan == "M2 - Redo":
                self.log("Redo berhasil: " + str(self.history.redo_last()))
            elif pilihan == "M2 - Statistik":
                undo, redo = self.history.history()
                self.log("Naif      : " + str(len(self.naif)))
                self.log("Circular  : " + str(len(self.history.antrean)))
                self.log("Kapasitas : " + str(len(self.history.antrean.data)))
                self.log("Geseran naif: " + str(self.naif.total_geseran))
                self.log("Undo depth: " + str(undo))
                self.log("Redo depth: " + str(redo))

        except Exception as exc:
            messagebox.showerror("Error", str(exc))

        elapsed = (time.perf_counter() - mulai) * 1000
        self.log("[" + pilihan + "] " + format(elapsed, ".3f") + " ms")
        self.log("-" * 60)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
