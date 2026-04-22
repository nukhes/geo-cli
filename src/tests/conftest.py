"""
conftest.py - Fixtures compartilhadas para toda a suíte de testes do geo-cli.

Carrega dados reais dos arquivos CSV no diretório examples/ para alimentar
testes de integração sem usar mocks hardcoded.
"""

import csv
import pytest
from pathlib import Path
import pandas as pd


# Caminhos base
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
SRC_DIR = Path(__file__).parent.parent / "geociencias_cli"


@pytest.fixture(scope="session")
def capitais_mundo_csv_path():
    """Retorna o caminho completo para capitais_mundo.csv."""
    path = EXAMPLES_DIR / "capitais_mundo.csv"
    assert path.exists(), f"Arquivo não encontrado: {path}"
    return str(path)


@pytest.fixture(scope="session")
def mineral_csv_path():
    """Retorna o caminho completo para mineral.csv."""
    path = EXAMPLES_DIR / "mineral.csv"
    assert path.exists(), f"Arquivo não encontrado: {path}"
    return str(path)


@pytest.fixture(scope="session")
def municipios_coordgeo_csv_path():
    """Retorna o caminho completo para municipios_coordgeo.csv."""
    path = EXAMPLES_DIR / "municipios_coordgeo.csv"
    assert path.exists(), f"Arquivo não encontrado: {path}"
    return str(path)


@pytest.fixture(scope="session")
def municipios_utm_csv_path():
    """Retorna o caminho completo para municipios_utm.csv."""
    path = EXAMPLES_DIR / "municipios_utm.csv"
    assert path.exists(), f"Arquivo não encontrado: {path}"
    return str(path)


@pytest.fixture(scope="session")
def elements_csv_path():
    """Retorna o caminho completo para elements.csv."""
    path = SRC_DIR / "data" / "elements.csv"
    assert path.exists(), f"Arquivo não encontrado: {path}"
    return str(path)


@pytest.fixture(scope="session")
def capitais_mundo_data(capitais_mundo_csv_path):
    """Carrega dados de capitais_mundo.csv como lista de dicts."""
    data = []
    with open(capitais_mundo_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


@pytest.fixture(scope="session")
def capitais_mundo_df(capitais_mundo_csv_path):
    """Carrega capitais_mundo.csv como DataFrame pandas."""
    df = pd.read_csv(capitais_mundo_csv_path)
    # Converte lat e lon para float
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)
    return df


@pytest.fixture(scope="session")
def mineral_data(mineral_csv_path):
    """Carrega dados de mineral.csv como lista de dicts."""
    data = []
    with open(mineral_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


@pytest.fixture(scope="session")
def municipios_coordgeo_data(municipios_coordgeo_csv_path):
    """Carrega dados de municipios_coordgeo.csv como lista de dicts."""
    data = []
    with open(municipios_coordgeo_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


@pytest.fixture(scope="session")
def municipios_utm_data(municipios_utm_csv_path):
    """Carrega dados de municipios_utm.csv como lista de dicts."""
    data = []
    with open(municipios_utm_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


@pytest.fixture(scope="session")
def elements_data(elements_csv_path):
    """Carrega dados de elements.csv como lista de dicts."""
    data = []
    with open(elements_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


@pytest.fixture
def temp_output_csv(tmp_path):
    """
    Fornece um caminho temporário para arquivo CSV de saída.

    Útil para testes de transformação/conversão de dados.
    """
    return str(tmp_path / "output.csv")


@pytest.fixture
def temp_html_file(tmp_path):
    """
    Fornece um caminho temporário para arquivo HTML.

    Útil para testes de geração de mapas.
    """
    return str(tmp_path / "mapa.html")


@pytest.fixture
def sample_geographic_csv(tmp_path):
    """
    Cria um arquivo CSV temporário com coordenadas geográficas (lat/lon).

    Usado em testes de conversão geo2utm.
    """
    csv_file = tmp_path / "sample_geo.csv"
    rows = [
        {"id": "1", "lat": "-23.550520", "lon": "-46.633309"},  # São Paulo, SP
        {"id": "2", "lat": "-19.920682", "lon": "-43.938677"},  # Belo Horizonte, MG
        {"id": "3", "lat": "-22.903756", "lon": "-43.209881"},  # Rio de Janeiro, RJ
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "lat", "lon"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(csv_file)


@pytest.fixture
def sample_utm_csv(tmp_path):
    """
    Cria um arquivo CSV temporário com coordenadas UTM (easting/northing).

    Usado em testes de conversão utm2geo.
    """
    csv_file = tmp_path / "sample_utm.csv"
    rows = [
        {"id": "1", "easting": "325848", "northing": "7394832"},
        {"id": "2", "easting": "567835", "northing": "7796545"},
        {"id": "3", "easting": "689234", "northing": "7465234"},
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "easting", "northing"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(csv_file)


@pytest.fixture
def sample_mineral_csv(tmp_path):
    """
    Cria um arquivo CSV temporário com fórmulas minerais.

    Usado em testes de análise de minerais.
    """
    csv_file = tmp_path / "sample_mineral.csv"
    rows = [
        {
            "molecula": "H2O",
            "analise quimica": "100.0",
        },
        {
            "molecula": "Ca(OH)2",
            "analise quimica": "74.1",
        },
        {
            "molecula": "MgSiO3",
            "analise quimica": "100.0",
        },
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["molecula", "analise quimica"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(csv_file)
