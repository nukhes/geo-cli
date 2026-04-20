"""
tests/test_petrology.py - Testes unitários para petrology.py

Cobre:
- color_index: Classificação de índice de cor de rocha baseado em proporção de minerais escuros
- rock_age: Cálculo de idade de rocha usando decaimento radioativo
"""

import pytest
import math
import sys
from pathlib import Path

# Adiciona src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from petrology import color_index, rock_age


class TestColorIndex:
    """Testes para função color_index."""

    def test_deve_retornar_hololeucocrática_para_m_ate_0_1(self):
        """
        Arrange: m entre 0 e 0.1 (0% a 10% minerais escuros)
        Act: Chama color_index
        Assert: Retorna "hololeucocrática"
        """
        # Act & Assert
        assert color_index(0.0) == "hololeucocrática"
        assert color_index(0.05) == "hololeucocrática"
        assert color_index(0.1) == "hololeucocrática"

    def test_deve_retornar_leucocrática_para_m_entre_0_1_0_3(self):
        """
        Arrange: m entre 0.1 e 0.3 (10% a 30% minerais escuros)
        Act: Chama color_index
        Assert: Retorna "leucocrática"
        """
        # Act & Assert
        assert color_index(0.15) == "leucocrática"
        assert color_index(0.25) == "leucocrática"
        assert color_index(0.3) == "leucocrática"

    def test_deve_retornar_mesocrática_para_m_entre_0_3_0_6(self):
        """
        Arrange: m entre 0.3 e 0.6 (30% a 60% minerais escuros)
        Act: Chama color_index
        Assert: Retorna "mesocrática"
        """
        # Act & Assert
        assert color_index(0.35) == "mesocrática"
        assert color_index(0.45) == "mesocrática"
        assert color_index(0.6) == "mesocrática"

    def test_deve_retornar_hipocrática_para_m_entre_0_6_0_9(self):
        """
        Arrange: m entre 0.6 e 0.9 (60% a 90% minerais escuros)
        Act: Chama color_index
        Assert: Retorna "hipocrática"
        """
        # Act & Assert
        assert color_index(0.65) == "hipocrática"
        assert color_index(0.75) == "hipocrática"
        assert color_index(0.9) == "hipocrática"

    def test_deve_retornar_ultramáfica_para_m_maior_que_0_9(self):
        """
        Arrange: m > 0.9 (>90% minerais escuros)
        Act: Chama color_index
        Assert: Retorna "ultramáfica"
        """
        # Act & Assert
        assert color_index(0.91) == "ultramáfica"
        assert color_index(0.95) == "ultramáfica"
        assert color_index(1.0) == "ultramáfica"

    def test_deve_aceitar_valores_float_precisos(self):
        """
        Arrange: Valores float com muitas casas decimais
        Act: Chama color_index
        Assert: Retorna classificação correta
        """
        # Act & Assert
        assert color_index(0.123456) == "leucocrática"
        assert color_index(0.456789) == "mesocrática"
        assert color_index(0.789012) == "hipocrática"

    def test_deve_lidar_com_valor_zero(self):
        """
        Arrange: m = 0 (nenhum mineral escuro)
        Act: Chama color_index
        Assert: Retorna "hololeucocrática"
        """
        # Act
        result = color_index(0)

        # Assert
        assert result == "hololeucocrática"

    def test_deve_lidar_com_valor_um(self):
        """
        Arrange: m = 1.0 (100% minerais escuros)
        Act: Chama color_index
        Assert: Retorna "ultramáfica"
        """
        # Act
        result = color_index(1.0)

        # Assert
        assert result == "ultramáfica"

    def test_deve_lançar_erro_para_valor_negativo(self):
        """
        Arrange: m < 0 (proporção negativa não faz sentido físico)
        Act: Chama color_index
        Assert: Lança ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError):
            color_index(-0.1)

    def test_deve_lançar_erro_para_valor_muito_alto(self):
        """
        Arrange: m > 1.0 (proporção maior que 100%)
        Act: Chama color_index
        Assert: Lança ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError):
            color_index(1.5)

    def test_deve_lançar_erro_para_tipo_invalido(self):
        """
        Arrange: Tipo não numérico passado
        Act: Chama color_index com string
        Assert: Lança TypeError ou ValueError
        """
        # Act & Assert
        with pytest.raises((TypeError, ValueError)):
            color_index("não_é_número")


class TestRockAge:
    """Testes para função rock_age."""

    def test_deve_calcular_idade_rocha_valores_validos(self):
        """
        Arrange: Parent (1.0), Daughter (1.0), Half-life (1000 anos)
        Act: Chama rock_age
        Assert: Retorna valor numérico positivo
        """
        # Act
        result = rock_age(parent=1.0, daughter=1.0, hl=1000.0)

        # Assert
        assert isinstance(result, float)
        assert result > 0

    def test_deve_calcular_idade_rocha_com_parent_maior(self):
        """
        Arrange: Parent > Daughter (rocha jovem)
        Act: Chama rock_age
        Assert: Retorna idade positiva (jovem)
        """
        # Act
        result = rock_age(parent=100.0, daughter=10.0, hl=1000.0)

        # Assert
        assert isinstance(result, float)
        assert result >= 0

    def test_deve_calcular_idade_rocha_com_parent_igual_daughter(self):
        """
        Arrange: Parent = Daughter (1:1 ratio)
        Act: Chama rock_age
        Assert: Retorna idade > 0
        """
        # Act
        result = rock_age(parent=1.0, daughter=1.0, hl=1000.0)

        # Assert
        assert isinstance(result, float)
        assert result > 0

    def test_deve_calcular_idade_rocha_com_parent_menor(self):
        """
        Arrange: Parent < Daughter (rocha antiga)
        Act: Chama rock_age
        Assert: Retorna idade > calculada com parent > daughter
        """
        # Arrange
        result_young = rock_age(parent=100.0, daughter=10.0, hl=1000.0)
        result_old = rock_age(parent=10.0, daughter=100.0, hl=1000.0)

        # Assert: Rocha antiga deve ter idade maior
        assert result_old > result_young

    def test_deve_aceitar_diferentes_half_lives(self):
        """
        Arrange: Diferentes meia-vidas (U-238, K-40, C-14, etc.)
        Act: Chama rock_age com various half-lives
        Assert: Todas retornam valores válidos
        """
        # Arrange
        # Half-lives em anos
        u238_hl = 4.468e9  # 4.468 bilhões
        k40_hl = 1.251e9   # 1.251 bilhões
        c14_hl = 5730      # 5730

        # Act
        age_u238 = rock_age(1.0, 1.0, u238_hl)
        age_k40 = rock_age(1.0, 1.0, k40_hl)
        age_c14 = rock_age(1.0, 1.0, c14_hl)

        # Assert
        assert all(isinstance(x, float) for x in [age_u238, age_k40, age_c14])
        assert all(x > 0 for x in [age_u238, age_k40, age_c14])

    def test_deve_retornar_zero_quando_daughter_zero(self):
        """
        Arrange: Daughter = 0 (rocha recém formada)
        Act: Chama rock_age
        Assert: Retorna valor próximo a zero
        """
        # Act
        result = rock_age(parent=1.0, daughter=0.0, hl=1000.0)

        # Assert
        assert isinstance(result, float)
        assert result >= 0 or abs(result) < 1e-10  # Pode ser zero ou muito pequeno

    def test_deve_lançar_erro_parent_zero(self):
        """
        Arrange: Parent = 0 (divisão por zero)
        Act: Chama rock_age
        Assert: Lança erro (ValueError ou ZeroDivisionError)
        """
        # Act & Assert
        with pytest.raises((ValueError, ZeroDivisionError)):
            rock_age(parent=0.0, daughter=1.0, hl=1000.0)

    def test_deve_lançar_erro_half_life_zero(self):
        """
        Arrange: Half-life = 0 (inválido)
        Act: Chama rock_age
        Assert: Lança erro
        """
        # Act & Assert
        with pytest.raises((ValueError, ZeroDivisionError)):
            rock_age(parent=1.0, daughter=1.0, hl=0.0)

    def test_deve_lançar_erro_valores_negativos(self):
        """
        Arrange: Valores negativos (não fazem sentido físico)
        Act: Chama rock_age com valores negativos
        Assert: Lança erro
        """
        # Act & Assert
        with pytest.raises((ValueError, TypeError)):
            rock_age(parent=-1.0, daughter=1.0, hl=1000.0)

        with pytest.raises((ValueError, TypeError)):
            rock_age(parent=1.0, daughter=-1.0, hl=1000.0)

        with pytest.raises((ValueError, TypeError)):
            rock_age(parent=1.0, daughter=1.0, hl=-1000.0)

    def test_formula_correcao_manualmente(self):
        """
        Arrange: Calcular manualmente com a fórmula
        Act: Comparar resultado com cálculo manual
        Assert: Valores combinam
        """
        # Arrange
        parent = 1.0
        daughter = 1.0
        hl = 1000.0

        # Cálculo manual: age = (1/lambda) * ln(1 + daughter/parent)
        lambda_val = math.log(2) / hl
        expected = (1 / lambda_val) * math.log(1 + daughter / parent)

        # Act
        result = rock_age(parent, daughter, hl)

        # Assert
        assert abs(result - expected) < 1e-10  # Tolerância de erro numérico

    def test_deve_incrementar_idade_com_mais_daughter(self):
        """
        Arrange: Variar quantidade de daughter isotope
        Act: Chamar rock_age com increasing daughter
        Assert: Idade aumenta com mais daughter
        """
        # Arrange
        parent = 1.0
        hl = 1000.0

        # Act
        age1 = rock_age(parent, 0.5, hl)
        age2 = rock_age(parent, 1.0, hl)
        age3 = rock_age(parent, 2.0, hl)

        # Assert
        assert age1 < age2 < age3  # Idade aumenta com daughter


class TestColorIndexEdgeCases:
    """Testes para edge cases de color_index."""

    def test_limites_exatos_entre_categorias(self):
        """
        Arrange: Valores no limite exato entre categorias
        Act: Testa pontos de limite
        Assert: Categorização correta nos limites
        """
        # Limite entre hololeucocrática e leucocrática
        assert color_index(0.1) == "hololeucocrática"

        # Limite entre leucocrática e mesocrática
        assert color_index(0.3) == "leucocrática"

        # Limite entre mesocrática e hipocrática
        assert color_index(0.6) == "mesocrática"

        # Limite entre hipocrática e ultramáfica
        assert color_index(0.9) == "hipocrática"

    def test_valores_logo_apos_limites(self):
        """
        Arrange: Valores imediatamente após cada limite
        Act: Testa valores após cada threshold
        Assert: Muda de categoria corretamente
        """
        epsilon = 0.00001

        # Logo após 0.1
        assert color_index(0.1 + epsilon) == "leucocrática"

        # Logo após 0.3
        assert color_index(0.3 + epsilon) == "mesocrática"

        # Logo após 0.6
        assert color_index(0.6 + epsilon) == "hipocrática"

        # Logo após 0.9
        assert color_index(0.9 + epsilon) == "ultramáfica"
