import typer
from pathlib import Path
from maps import convert_scale, generate_map, real_thickness
from formula import mineral_formula
from conversor import GeoToUtm, UtmToGeo
from petrology import color_index, rock_age

app = typer.Typer(
    help='toolkit de ferramentas relacionadas a geociências construídas por mim',
    add_completion=False
)

# default workflow
def workflow(processor):
    try:
        processor
        typer.secho(f'sucesso! arquivo final criado', fg=typer.colors.GREEN, bold=True)

    except Exception as e:
        typer.secho(f'ocorreu um erro inesperado: {e}', fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def geo2utm(
    input_file: Path = typer.Argument(
        ..., 
        help='caminho para o arquivo CSV de entrada (deve conter as colunas "lat" e "lon")',
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output_file: Path = typer.Argument(
        ..., 
        help='caminho onde o CSV final com os dados convertidos será salvo'
    ),
    source_epsg: str = typer.Option('EPSG:4326', help='EPSG code for source coordinate system'),
    target_epsg: str = typer.Option('EPSG:31983', help='EPSG code for target coordinate system'),
    ):
    '''
    converte coordenadas geográficas (EPSG:4326 como padrão) para UTM (EPSG:31983 como padrão).
    '''
    workflow(GeoToUtm(f_input=str(input_file), f_output=str(output_file), epsg_source=source_epsg, epsg_target=target_epsg).run())		


@app.command()
def utm2geo(
    input_file: Path = typer.Argument(
        ..., 
        help='caminho para o arquivo CSV de entrada (deve conter as colunas "easting" e "northing")',
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output_file: Path = typer.Argument(
        ..., 
        help='caminho onde o CSV final com os dados convertidos será salvo'
    ),
    source_epsg: str = typer.Option('EPSG:31983', help='EPSG code for source coordinate system'),
    target_epsg: str = typer.Option('EPSG:4326', help='EPSG code for target coordinate system'),
    ):
    '''
    converte coordenadas UTM (EPSG:31983 como padrão) para geográficas (EPSG:4326 como padrão).
    '''
    workflow(UtmToGeo(f_input=str(input_file), f_output=str(output_file), epsg_source=source_epsg, epsg_target=target_epsg).run())

@app.command()
def map(
    input_file: Path = typer.Argument(
        ..., 
        help='caminho para o arquivo CSV de entrada',
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    title: str = typer.Argument("Mapa", help='título do mapa'),
    id: str = typer.Argument(None, help='nome da coluna a ser usada como identificador dos pontos no mapa (opcional)'),
    zoom_start: int = typer.Option(2, help='nível de zoom inicial do mapa')
    ):
    '''
    gera um mapa interativo a partir de coordenadas em um arquivo CSV.
    '''
    workflow(generate_map(input_file, title, id, zoom_start))

@app.command()
def mineralformula(
    input_file: Path = typer.Argument(
        ..., 
        help='caminho para o arquivo CSV de entrada',
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output_file: Path = typer.Argument(
        ..., 
        help='caminho onde o CSV final com a tabela de fórmulas minerais será salvo'
    )
    ):
    '''
    constroe a tabela de formula mineral com base em um arquivo CSV contendo as colunas das moléculas e suas respectivas análises quimicas.
    '''
    workflow(mineral_formula(input_file, output_file))

@app.command()
def escala(
    escala: str = typer.Argument(..., help='escala cartográfica'),
    distancia_carta: float = typer.Argument(..., help='distância medida na carta (em cm)'),
    ):
    '''
    calcula a distância real correspondente a uma medida feita em uma carta, com base na escala fornecida.
    '''
    res = convert_scale(escala, distancia_carta)
    typer.secho(f'distância real: {res} cm ou {res/1000} km', fg=typer.colors.GREEN, bold=True)

@app.command()
def indicecor(
    olivina: float = typer.Option(0.0, "--olivina", "-o", help="Porcentagem visual de Olivina"),
    piroxenio: float = typer.Option(0.0, "--piroxenio", "-p", help="Porcentagem visual de Piroxênio"),
    biotita: float = typer.Option(0.0, "--biotita", "-b", help="Porcentagem visual de Biotita"),
    anfibolio: float = typer.Option(0.0, "--anfibolio", "-a", help="Porcentagem visual de Anfibólio"),
    opacos: float = typer.Option(0.0, "--opacos", help="Percentagem de minerais metálicos/opacos (Magnetite, Ilmenite)"),
    outros: float = typer.Option(0.0, "--outros", help="Outros minerais ferromagnesianos (Granada, Turmalina, etc.)")
    ):
    '''
    calcula o índice de cor de uma rocha com base na proporção de minerais escuros (m) presente nela.
    '''
    m = olivina + piroxenio + biotita + anfibolio + opacos + outros
    if m > 1.0:
        typer.secho(f'a soma das porcentagens de minerais escuros excede 100% (m = {m}). O índice de cor pode ser impreciso.', fg=typer.colors.YELLOW)
    elif m < 0.0:
        typer.secho(f'a soma das porcentagens de minerais escuros é negativa (m = {m}). O índice de cor pode ser impreciso.', fg=typer.colors.YELLOW)
    typer.secho(f'índice de cor: {color_index(m)}', fg=typer.colors.GREEN, bold=True)

@app.command()
def mergulho(
    length: float = typer.Argument(...,help='comprimento do afloramento na superfície'),
    angle: float = typer.Argument(..., help='ângulo de mergulho do afloramento')
    ):
    if angle > 90 or angle < 0:
        raise ValueError(f'o ângulo deve estar entre 0 e 90 graus')
        return
    typer.secho(f'espessura reais: {real_thickness(length, angle)}', fg=typer.colors.GREEN, bold=True)

@app.command()
def idaderocha(
    parent: float = typer.Option(..., "--pai", "-p", help="quantidade do isótopo pai"),
    daughter: float = typer.Option(..., "--filho", "-f", help="quantidade do isótopo filho"),
    hl: float = typer.Option(..., "--meia-vida", "-mv", help="meia-vida do isótopo pai")
    ):

    if parent <= 0:
        typer.secho("a quantidade do isótopo pai deve ser maior que zero.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"A idade calculada da rocha é: {rock_age(parent, daughter, hl)} anos", fg=typer.colors.GREEN)

@app.command()

if __name__ == '__main__':
    app()
