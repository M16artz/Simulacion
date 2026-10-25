import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = ["tiempo", "susceptibles", "infectados", "recuperados"]
STATES = ("susceptibles", "infectados", "recuperados")


def _read_csv(name):
    with (ROOT / "netlogo" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_integer_csvs():
    for name in ["resultados_python.csv", "resultados_netlogo.csv"]:
        rows = _read_csv(name)
        assert len(rows) == 101
        assert list(rows[0]) == HEADER
        assert rows[0] == dict(tiempo="0", susceptibles="95", infectados="5", recuperados="0")
        assert rows[-1]["tiempo"] == "100"
        for t, row in enumerate(rows):
            assert int(row["tiempo"]) == t
            assert sum(int(row[k]) for k in STATES) == 100


def test_euler_reference():
    rows = _read_csv("resultados_euler_python.csv")
    assert len(rows) == 101
    assert list(rows[0]) == HEADER
    assert rows[0] == dict(
        tiempo="0",
        susceptibles="95.00000000",
        infectados="5.00000000",
        recuperados="0.00000000",
    )
    assert rows[-1]["tiempo"] == "100"
    for t, row in enumerate(rows):
        assert int(float(row["tiempo"])) == t
        assert abs(sum(float(row[k]) for k in STATES) - 100.0) < 1e-6
