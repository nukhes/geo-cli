import typer
from pathlib import Path
from map import generate_map
from conversor import GeoToUtm, UtmToGeo


app = typer.Typer(
    help='programa em python para converter base de dados CSV entre diferentes sistemas de geolocalização',
    add_completion=False
)

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
    converte coordenadas geográficas (EPSG:4326) para UTM (EPSG:31983).
    '''
    
    try:
        processor = GeoToUtm(f_input=str(input_file), f_output=str(output_file), epsg_source=source_epsg, epsg_target=target_epsg)
        processor.run()
        
        typer.secho(f'sucesso! arquivo final salvo em: {output_file} 🎉', fg=typer.colors.GREEN, bold=True)
        
    except KeyError as e:
        typer.secho(f'erro: coluna não encontrada {e}', fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f'ocorreu um erro inesperado: {e}', fg=typer.colors.RED)
        raise typer.Exit(code=1)

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
    converte coordenadas UTM (EPSG:31983) para geográficas (EPSG:4326).
    '''
    
    try:
        processor = UtmToGeo(f_input=str(input_file), f_output=str(output_file), epsg_source=source_epsg, epsg_target=target_epsg)
        processor.run()
        
        typer.secho(f'sucesso! arquivo final salvo em: {output_file} 🎉', fg=typer.colors.GREEN, bold=True)
        
    except KeyError as e:
        typer.secho(f'erro: coluna não encontrada {e}', fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f'ocorreu um erro inesperado: {e}', fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def genmap(
    input_file: Path = typer.Argument(
        ..., 
        help='caminho para o arquivo CSV de entrada',
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    title: str = typer.Option("Mapa", help='título do mapa'),
    id: str = typer.Option(None, help='nome da coluna a ser usada como identificador dos pontos no mapa (opcional)'),
    zoom_start: int = typer.Option(2, help='nível de zoom inicial do mapa')
):
    '''
    gera um mapa interativo a partir de coordenadas em um arquivo CSV.
    '''
    
    try:
        generate_map(input_file, title, id, zoom_start)
        typer.secho(f'sucesso! mapa salvo como "mapa.html" 🎉', fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f'ocorreu um erro inesperado: {e}', fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == '__main__':
    app()