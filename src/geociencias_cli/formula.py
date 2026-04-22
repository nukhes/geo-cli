import csv
import re
import itertools


def load_data(input_file):
    props = {}
    with open(input_file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            charges = [int(c) for c in row["carga"].split("/")]
            props[row["simbolo"]] = {
                "mass": float(row["massa"]),
                "charge": charges[0],
                "all_charges": charges,
            }
    return props


def get_ions(molecule, elements):
    mask = (
        r"(?P<element>[A-Z][a-z]*)(?P<quantity>\d*\.?\d*)"
        r"|(?P<open>\()"
        r"|(?P<close>\))(?P<close_quantity>\d*\.?\d*)"
    )

    items = re.finditer(mask, molecule)
    stack = [{}]

    for item in items:
        if item.group("element"):
            el = item.group("element")
            qt = float(item.group("quantity") or 1)
            stack[-1][el] = stack[-1].get(el, 0) + qt
        elif item.group("open"):
            stack.append({})
        elif item.group("close"):
            group = stack.pop()
            mult = float(item.group("close_quantity") or 1)
            for el, qt in group.items():
                stack[-1][el] = stack[-1].get(el, 0) + qt * mult

    atoms = stack[0]
    best_balance = float("inf")
    best_combo = {}

    el_list = [el for el in atoms if el in elements]
    options = [elements[el]["all_charges"] for el in el_list]

    for combo in itertools.product(*options):
        current = dict(zip(el_list, combo))
        balance = sum(atoms[el] * current[el] for el in el_list)
        if abs(balance) < abs(best_balance):
            best_balance = balance
            best_combo = current
            if abs(best_balance) < 1e-6:
                break

    cations, anions = {}, {}
    for el, qt in atoms.items():
        val = best_combo.get(el, 0)
        if val > 0:
            cations[el] = qt
        else:
            anions[el] = qt

    return cations, anions, best_balance


def mineral(input_file, output_file):
    elements = load_data("./src/geociencias_cli/data/elements.csv")

    with (
        open(input_file, mode="r", encoding="utf-8") as f_in,
        open(output_file, mode="w", newline="", encoding="utf-8") as f_out,
    ):
        reader = csv.DictReader(f_in)
        fields = [
            "molecula",
            "analise quimica",
            "massa molar",
            "prop molecular",
            "prop cations",
            "prop anions",
        ]
        writer = csv.DictWriter(f_out, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()

        for row in reader:
            mol = list(row.values())[0]
            raw = list(row.values())[1]

            if not mol or not raw:
                continue

            try:
                val = float(str(raw).replace(",", "."))
            except ValueError:
                continue

            cats, anis, balance = get_ions(mol, elements)
            all_atoms = {**cats, **anis}
            mass = sum(
                elements[el]["mass"] * qt
                for el, qt in all_atoms.items()
                if el in elements
            )

            if mass == 0:
                continue

            pmol = val / mass
            pcat = pmol * sum(cats.values())
            pani = pmol * sum(anis.values())

            writer.writerow(
                {
                    fields[0]: mol,
                    fields[1]: round(val, 3),
                    fields[2]: round(mass, 3),
                    fields[3]: round(pmol, 3),
                    fields[4]: round(pcat, 3),
                    fields[5]: round(pani, 3),
                }
            )
