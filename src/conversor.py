import csv
import re
from pyproj import Transformer


class ProcessCsv:
    def __init__(self, f_input, f_output, epsg_source, epsg_target):
        self.f_input = f_input
        self.f_output = f_output
        self.epsg_source = epsg_source
        self.epsg_target = epsg_target
        self.transformer = Transformer.from_crs(
            epsg_source, epsg_target, always_xy=True
        )
        self.fields_in = []
        self.fields_out = []

    def run(self):
        if self.fields_in is None or self.fields_out is None:
            raise NotImplementedError(
                "fields_in and fields_out must be defined in subclasses."
            )

        with (
            open(self.f_input, mode="r", encoding="utf-8") as f_input,
            open(self.f_output, mode="w", newline="", encoding="utf-8") as f_output,
        ):
            reader = csv.DictReader(f_input)

            output_fieldnames = [
                f for f in reader.fieldnames if f not in self.fields_in
            ] + self.fields_out

            writer = csv.DictWriter(
                f_output, fieldnames=output_fieldnames, extrasaction="ignore"
            )
            writer.writeheader()
            for row in reader:
                new_line = self.__trans(row)
                if new_line:
                    writer.writerow(new_line)

    def __trans(self, row):
        row_copy = row.copy()
        output_x, output_y = self.transformer.transform(
            float(row_copy[self.fields_in[0]]), float(row_copy[self.fields_in[1]])
        )

        row_copy[self.fields_out[0]] = round(output_x, 3)
        row_copy[self.fields_out[1]] = round(output_y, 3)

        return row_copy


class GeoUtm(ProcessCsv):
    def __init__(
        self, f_input, f_output, epsg_source="EPSG:4326", epsg_target="EPSG:31983"
    ):
        super().__init__(f_input, f_output, epsg_source, epsg_target)
        self.fields_in = ["lon", "lat"]
        self.fields_out = ["easting", "northing"]


class UtmGeo(ProcessCsv):
    def __init__(
        self, f_input, f_output, epsg_source="EPSG:31983", epsg_target="EPSG:4326"
    ):
        super().__init__(f_input, f_output, epsg_source, epsg_target)
        self.fields_in = ["easting", "northing"]
        self.fields_out = ["lon", "lat"]


def get_quad(angle):
    """
    recebe um ângulo em graus e retorna o quadrante correspondente (NE, SE, SW ou NW).
    """
    angle = angle % 360
    if 0 <= angle <= 90:
        return "NE"
    elif 90 < angle <= 180:
        return "SE"
    elif 180 < angle <= 270:
        return "SW"
    else:
        return "NW"


def strikedip(input):
    """
    converte um dado de rumo e mergulho no formato "QA R QB / DIP QF" para o formato "DIP_DIRECTION/DIP", onde:
    - QA: sentido inicial do rumo (N ou S)
    - R: ângulo do rumo (em graus)
    - QB: sentido inicial do rumo (E ou W)
    - DIP: ângulo do mergulho (em graus)
    - QF: quadrante final do rumo (NE, SE, SW ou NW)
    - DIP_DIRECTION: direção do mergulho (em graus, no intervalo [0;360])
    """
    # coleta os dados brutos em regex e joga pra variáveis temporárias
    mask = r"(?P<qa>[A-Z])(?P<r>\d+)(?P<qb>[A-Z])\s*/\s*(?P<dip>\d+)(?P<qf>[A-Z][A-Z])"
    qa, r, qb, dip, qf = re.match(mask, input).groups()

    q_inicial = f"{qa}{qb}".upper()
    q_final = qf.upper()
    r = int(r)
    dip = int(dip)

    # essa tabela é importante para converter o angulo do rumo, de acordo com o quadrante
    # para garantir que o valor final esteja no intervalo [0;90].
    azimute_table = {"NE": r, "SE": 180 - r, "SW": 180 + r, "NW": 360 - r}
    az_r = azimute_table[q_inicial]

    dip_direction = (az_r + 90) % 360
    q_dip_direction = get_quad(dip_direction)

    if q_dip_direction != q_final:
        dip_direction = (az_r - 90) % 360

    return f"{str(int(dip_direction)).zfill(3)}/{dip}"
