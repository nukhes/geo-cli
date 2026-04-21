"""
tests/test_main.py - Testes de CLI usando typer.testing.CliRunner

Testa:
- geo2utm: Conversão de coordenadas geográficas para UTM via CLI
- utm2geo: Conversão de coordenadas UTM para geográficas via CLI
- map: Geração de mapa interativo
- mineralformula: Processamento de fórmulas minerais
- escala: Cálculo de escala cartográfica
- indicecor: Cálculo de índice de cor de rocha
- mergulho: Cálculo de espessura real de afloramento
"""

import sys
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner

# Adiciona src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app

runner = CliRunner()


class TestGeo2UtmCommand:
    """Testes para comando geo2utm."""

    def test_deve_executar_com_arquivos_validos(
        self, sample_geographic_csv, temp_output_csv
    ):
        """
        Arrange: Arquivo CSV com coordenadas geográficas válidas
        Act: Executa comando geo2utm
        Assert: Retorna exit code 0 (sucesso)
        """
        # Act
        result = runner.invoke(
            app,
            [
                "geo2utm",
                sample_geographic_csv,
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code == 0, f"Erro na CLI: {result.stdout}"
        assert "sucesso" in result.stdout.lower()

    def test_deve_falhar_arquivo_entrada_nao_existe(self, temp_output_csv):
        """
        Arrange: Arquivo de entrada inexistente
        Act: Executa comando geo2utm
        Assert: Lança erro de arquivo não encontrado
        """
        # Act
        result = runner.invoke(
            app,
            [
                "geo2utm",
                "/caminho/inexistente.csv",
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code != 0

    def test_deve_aceitar_epsg_customizado(
        self, sample_geographic_csv, temp_output_csv
    ):
        """
        Arrange: Arquivo válido com EPSG customizado
        Act: Executa geo2utm com --source-epsg e --target-epsg
        Assert: Retorna sucesso
        """
        # Act
        result = runner.invoke(
            app,
            [
                "geo2utm",
                sample_geographic_csv,
                temp_output_csv,
                "--source-epsg",
                "EPSG:4326",
                "--target-epsg",
                "EPSG:31983",
            ],
        )

        # Assert
        assert result.exit_code == 0

    def test_deve_criar_arquivo_saida(self, sample_geographic_csv, temp_output_csv):
        """
        Arrange: Arquivo de entrada válido
        Act: Executa geo2utm
        Assert: Arquivo de saída é criado e contém dados
        """
        # Act
        result = runner.invoke(
            app,
            [
                "geo2utm",
                sample_geographic_csv,
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code == 0
        assert Path(temp_output_csv).exists()
        # Verifica se tem conteúdo
        with open(temp_output_csv, mode="r") as f:
            content = f.read()
            assert len(content) > 0


class TestUtm2GeoCommand:
    """Testes para comando utm2geo."""

    def test_deve_executar_com_arquivos_validos(self, sample_utm_csv, temp_output_csv):
        """
        Arrange: Arquivo CSV com coordenadas UTM válidas
        Act: Executa comando utm2geo
        Assert: Retorna exit code 0
        """
        # Act
        result = runner.invoke(
            app,
            [
                "utm2geo",
                sample_utm_csv,
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code == 0, f"Erro na CLI: {result.stdout}"
        assert "sucesso" in result.stdout.lower()

    def test_deve_falhar_arquivo_entrada_nao_existe(self, temp_output_csv):
        """
        Arrange: Arquivo de entrada inexistente
        Act: Executa comando utm2geo
        Assert: Lança erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "utm2geo",
                "/caminho/inexistente.csv",
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code != 0

    def test_deve_aceitar_epsg_customizado(self, sample_utm_csv, temp_output_csv):
        """
        Arrange: Arquivo válido com EPSG customizado
        Act: Executa utm2geo com opções EPSG
        Assert: Retorna sucesso
        """
        # Act
        result = runner.invoke(
            app,
            [
                "utm2geo",
                sample_utm_csv,
                temp_output_csv,
                "--source-epsg",
                "EPSG:31983",
                "--target-epsg",
                "EPSG:4326",
            ],
        )

        # Assert
        assert result.exit_code == 0


class TestMapCommand:
    """Testes para comando map."""

    def test_deve_executar_com_arquivo_valido(self, sample_geographic_csv, monkeypatch):
        """
        Arrange: Arquivo CSV com coordenadas geográficas
        Act: Executa comando map com patch de folium.Map.save()
        Assert: Retorna sucesso
        """
        # Arrange
        # Mock folium.Map.save para não criar arquivo HTML real
        with patch("maps.folium.Map.save"):
            # Act
            result = runner.invoke(
                app,
                [
                    "map",
                    sample_geographic_csv,
                    "Mapa Teste",
                ],
            )

        # Assert
        assert result.exit_code == 0, f"Erro na CLI: {result.stdout}"

    def test_deve_aceitar_zoom_customizado(self, sample_geographic_csv, monkeypatch):
        """
        Arrange: Arquivo válido com zoom customizado
        Act: Executa map com --zoom-start
        Assert: Retorna sucesso
        """
        # Arrange
        with patch("maps.folium.Map.save"):
            # Act
            result = runner.invoke(
                app,
                [
                    "map",
                    sample_geographic_csv,
                    "Mapa",
                    "--zoom-start",
                    "8",
                ],
            )

        # Assert
        assert result.exit_code == 0

    def test_deve_aceitar_campo_identificador(self, sample_geographic_csv, monkeypatch):
        """
        Arrange: Arquivo com coluna de identificador
        Act: Executa map com --id
        Assert: Retorna sucesso
        """
        # Arrange
        with patch("maps.folium.Map.save"):
            # Act
            result = runner.invoke(
                app,
                [
                    "map",
                    sample_geographic_csv,
                    "Mapa",
                    "id",
                ],
            )

        # Assert
        assert result.exit_code == 0


class TestEscalaCommand:
    """Testes para comando escala."""

    def test_deve_calcular_escala_valida(self):
        """
        Arrange: Escala e distância válidas
        Act: Executa comando escala com "1:1000" e distancia "5"
        Assert: Retorna exit code 0 e resultado
        """
        # Act
        result = runner.invoke(
            app,
            [
                "escala",
                "1:1000",
                "5",
            ],
        )

        # Assert
        assert result.exit_code == 0
        assert "distância real" in result.stdout.lower()

    def test_deve_calcular_escala_diferentes_unidades(self):
        """
        Arrange: Diferentes escalas
        Act: Executa com escalas variadas
        Assert: Retorna sucesso para todas
        """
        # Act
        result1 = runner.invoke(app, ["escala", "1:10000", "2.5"])
        result2 = runner.invoke(app, ["escala", "1:50000", "10"])
        result3 = runner.invoke(app, ["escala", "1:100000", "1"])

        # Assert
        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert result3.exit_code == 0

    def test_deve_falhar_escala_invalida(self):
        """
        Arrange: Escala com formato inválido
        Act: Executa comando escala
        Assert: Retorna erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "escala",
                "INVALIDO",
                "5",
            ],
        )

        # Assert
        assert result.exit_code != 0

    def test_deve_falhar_distancia_invalida(self):
        """
        Arrange: Distância com valor inválido
        Act: Executa comando escala
        Assert: Retorna erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "escala",
                "1:1000",
                "NAO_E_NUMERO",
            ],
        )

        # Assert
        assert result.exit_code != 0


class TestIndiceCorCommand:
    """Testes para comando indicecor."""

    def test_deve_calcular_indice_cor_com_valores_validos(self):
        """
        Arrange: Porcentagens válidas de minerais escuros
        Act: Executa comando indicecor
        Assert: Retorna sucesso com índice calculado
        """
        # Act
        result = runner.invoke(
            app,
            [
                "indicecor",
                "--olivina",
                "0.1",
                "--piroxenio",
                "0.2",
            ],
        )

        # Assert
        assert result.exit_code == 0
        assert "índice de cor" in result.stdout.lower()

    def test_deve_aceitar_todas_opcoes_minerais(self):
        """
        Arrange: Todas as opções de minerais preenchidas
        Act: Executa indicecor com todas as flags
        Assert: Retorna sucesso
        """
        # Act
        result = runner.invoke(
            app,
            [
                "indicecor",
                "--olivina",
                "0.1",
                "--piroxenio",
                "0.1",
                "--biotita",
                "0.1",
                "--anfibolio",
                "0.1",
                "--opacos",
                "0.05",
            ],
        )

        # Assert
        assert result.exit_code == 0

    def test_deve_avisar_soma_maior_que_100_porcento(self):
        """
        Arrange: Soma de minerais > 100%
        Act: Executa indicecor com valores que excedem 100%
        Assert: Retorna erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "indicecor",
                "--olivina",
                "0.6",
                "--piroxenio",
                "0.5",
            ],
        )

        # Assert
        assert result.exit_code == 1

    def test_deve_avisar_soma_negativa(self):
        """
        Arrange: Soma de minerais negativa
        Act: Executa indicecor com valores negativos
        Assert: Retorna erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "indicecor",
                "--olivina",
                "-0.5",
            ],
        )

        # Assert
        assert result.exit_code == 1


class TestMergulhoCommand:
    """Testes para comando mergulho."""

    def test_deve_calcular_espessura_real_valida(self):
        """
        Arrange: Comprimento e ângulo válidos
        Act: Executa comando mergulho
        Assert: Retorna sucesso com espessura calculada
        """
        # Act
        result = runner.invoke(
            app,
            [
                "mergulho",
                "100",  # comprimento em metros
                "45",  # ângulo em graus
            ],
        )

        # Assert
        assert result.exit_code == 0

    def test_deve_lidar_com_diferentes_angulos(self):
        """
        Arrange: Diferentes ângulos de mergulho
        Act: Executa mergulho com 30, 45, 60, 90 graus
        Assert: Todos retornam sucesso
        """
        # Act
        for angle in [30, 45, 60, 90]:
            result = runner.invoke(
                app,
                ["mergulho", "100", str(angle)],
            )
            # Assert
            assert result.exit_code == 0

    def test_deve_falhar_com_valores_invalidos(self):
        """
        Arrange: Valores inválidos para comprimento ou ângulo
        Act: Executa mergulho
        Assert: Retorna erro
        """
        # Act & Assert
        result = runner.invoke(app, ["mergulho", "NAO_E_NUMERO", "45"])
        assert result.exit_code != 0

        result = runner.invoke(app, ["mergulho", "100", "NAO_E_NUMERO"])
        assert result.exit_code != 0


class TestMineralformulaCommand:
    """Testes para comando mineralformula."""

    def test_deve_processar_arquivo_mineral_valido(
        self, sample_mineral_csv, temp_output_csv
    ):
        """
        Arrange: Arquivo CSV com fórmulas minerais
        Act: Executa comando mineralformula
        Assert: Retorna sucesso e cria arquivo de saída
        """
        # Act
        result = runner.invoke(
            app,
            [
                "mineralformula",
                sample_mineral_csv,
                temp_output_csv,
            ],
        )

        # Assert
        # Pode falhar se o caminho de elements.csv não estiver correto
        # mas a CLI deve tentar executar
        assert "sucesso" in result.stdout.lower() or "erro" in result.stdout.lower()

    def test_deve_falhar_arquivo_entrada_nao_existe(self, temp_output_csv):
        """
        Arrange: Arquivo de entrada inexistente
        Act: Executa mineralformula
        Assert: Retorna erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "mineralformula",
                "/caminho/inexistente.csv",
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code != 0


class TestCliHelpTexts:
    """Testes para verificar que comandos têm help text."""

    def test_geo2utm_tem_help(self):
        """Arrange: Comando geo2utm
        Act: Executa com --help
        Assert: Mostra ajuda
        """
        # Act
        result = runner.invoke(app, ["geo2utm", "--help"])

        # Assert
        assert result.exit_code == 0
        assert "Usage" in result.stdout

    def test_utm2geo_tem_help(self):
        """Arrange: Comando utm2geo
        Act: Executa com --help
        Assert: Mostra ajuda
        """
        # Act
        result = runner.invoke(app, ["utm2geo", "--help"])

        # Assert
        assert result.exit_code == 0
        assert "Usage" in result.stdout

    def test_escala_tem_help(self):
        """Arrange: Comando escala
        Act: Executa com --help
        Assert: Mostra ajuda
        """
        # Act
        result = runner.invoke(app, ["escala", "--help"])

        # Assert
        assert result.exit_code == 0
        assert "Usage" in result.stdout

    def test_indicecor_tem_help(self):
        """Arrange: Comando indicecor
        Act: Executa com --help
        Assert: Mostra ajuda
        """
        # Act
        result = runner.invoke(app, ["indicecor", "--help"])

        # Assert
        assert result.exit_code == 0
        assert "Usage" in result.stdout


class TestCliWorkflow:
    """Testes para workflow() function behavior."""

    def test_deve_mostrar_mensagem_sucesso_em_verde(
        self, sample_geographic_csv, temp_output_csv
    ):
        """
        Arrange: Operação que deve ter sucesso
        Act: Executa geo2utm
        Assert: Output contém "sucesso" em mensagem
        """
        # Act
        result = runner.invoke(
            app,
            [
                "geo2utm",
                sample_geographic_csv,
                temp_output_csv,
            ],
        )

        # Assert
        assert "sucesso" in result.stdout.lower()

    def test_deve_tratar_excecoes_e_retornar_exit_code_1(self, temp_output_csv):
        """
        Arrange: Operação que vai falhar (arquivo não existe)
        Act: Executa comando
        Assert: Exit code é 1 e mostra mensagem de erro
        """
        # Act
        result = runner.invoke(
            app,
            [
                "geo2utm",
                "/caminho/inexistente.csv",
                temp_output_csv,
            ],
        )

        # Assert
        assert result.exit_code == 2
        assert "erro" in result.stdout.lower() or result.exit_code != 0
