"""
Suíte de testes automatizados para geo-cli.

Este pacote contém testes unitários e de integração para todos os módulos
da aplicação CLI geo-cli, incluindo:

- test_conversor.py: Testes para conversão de coordenadas (Geo<->UTM)
- test_formula.py: Testes para análise de moléculas e minerais
- test_maps.py: Testes para geração de mapas e cálculos cartográficos
- test_petrology.py: Testes para cálculos de geologia (índice de cor, idade de rocha)
- test_main.py: Testes de CLI (interface de linha de comando)
- conftest.py: Fixtures e configurações compartilhadas

Executar testes:
    pytest                          # Executa toda a suíte
    pytest tests/test_conversor.py  # Executa testes específicos
    pytest -v                       # Modo verbose
    pytest --cov=src                # Com cobertura de código
"""
