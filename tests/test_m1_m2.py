import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.m1_pesanan import Pesanan, ArrayPesanan, LinkedListPesanan
from backend.m2_antrean import (
    ke_postfix, hitung_postfix, AntreanNaif, AntreanMelingkar
)

def test_m1():
    a = ArrayPesanan()
    l = LinkedListPesanan()
    p1 = Pesanan("A", "x", "r", "m", 1000, 3, 0, None, "ANTRE")
    p2 = Pesanan("B", "x", "r", "m", 1000, 2, 0, None, "ANTRE")
    p3 = Pesanan("C", "x", "r", "m", 1000, 1, 0, None, "ANTRE")
    for p in [p1, p2, p3]:
        a.tambah_berdasarkan_prioritas(p)
        l.tambah_berdasarkan_prioritas(p)
    assert a.get(0).oid == "C"
    assert l.get(0).oid == "C"
    assert a.get(1).oid == "B"
    assert l.get(1).oid == "B"

def test_postfix():
    p = ke_postfix("( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
    assert " ".join(p) == "3 12000 * 2 8500 * + 5000 -"
    assert hitung_postfix(p) == 48000

def test_queue():
    q = AntreanMelingkar(4)
    q.enqueue("A"); q.enqueue("B"); q.enqueue("C")
    assert q.dequeue() == "A"
    q.enqueue("D"); q.enqueue("E")
    assert q.dequeue() == "B"
    assert q.dequeue() == "C"
    assert q.dequeue() == "D"
    assert q.dequeue() == "E"
    assert q.dequeue() is None

def test_naif():
    q = AntreanNaif(["A", "B", "C"])
    assert q.dequeue() == "A"
    assert q.total_geseran == 2

if __name__ == "__main__":
    test_m1()
    test_postfix()
    test_queue()
    test_naif()
    print("SEMUA TEST M1-M2 LULUS")
