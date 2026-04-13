# CLI

programa em python para converter base de dados CSV entre diferentes sistemas de geolocalização

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `geo2utm`: converte coordenadas geográficas...
* `utm2geo`: converte coordenadas UTM (EPSG:31983) para...
* `genmap`: gera um mapa interativo a partir de...

## `geo2utm`

converte coordenadas geográficas (EPSG:4326) para UTM (EPSG:31983).

**Usage**:

```console
$ geo2utm [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada (deve conter as colunas &quot;lat&quot; e &quot;lon&quot;)  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com os dados convertidos será salvo  [required]

**Options**:

* `--source-epsg TEXT`: EPSG code for source coordinate system  [default: EPSG:4326]
* `--target-epsg TEXT`: EPSG code for target coordinate system  [default: EPSG:31983]
* `--help`: Show this message and exit.

## `utm2geo`

converte coordenadas UTM (EPSG:31983) para geográficas (EPSG:4326).

**Usage**:

```console
$ utm2geo [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada (deve conter as colunas &quot;easting&quot; e &quot;northing&quot;)  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com os dados convertidos será salvo  [required]

**Options**:

* `--source-epsg TEXT`: EPSG code for source coordinate system  [default: EPSG:31983]
* `--target-epsg TEXT`: EPSG code for target coordinate system  [default: EPSG:4326]
* `--help`: Show this message and exit.

## `genmap`

gera um mapa interativo a partir de coordenadas em um arquivo CSV.

**Usage**:

```console
$ genmap [OPTIONS] INPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada  [required]

**Options**:

* `--zoom-start INTEGER`: nível de zoom inicial do mapa  [default: 2]
* `--help`: Show this message and exit.
