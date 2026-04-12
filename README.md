# `geocoordenadas`

programa em python para converter base de dados CSV entre diferentes sistemas de geolocalização

**Usage**:

```console
$ geocoordenadas [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `geo2utm`: converte coordenadas geográficas...
* `utm2geo`: converte coordenadas UTM (EPSG:31983) para...

## `geocoordenadas geo2utm`

converte coordenadas geográficas (EPSG:4326) para UTM (EPSG:31983).

**Usage**:

```console
$ geocoordenadas geo2utm [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada (deve conter a estrutura padrão ./examples/geo.csv)  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com os dados convertidos será salvo  [required]

**Options**:

* `--help`: Show this message and exit.

## `geocoordenadas utm2geo`

converte coordenadas UTM (EPSG:31983) para geográficas (EPSG:4326).

**Usage**:

```console
$ geocoordenadas utm2geo [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada (deve conter a estrutura padrão ./examples/utm.csv)  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com os dados convertidos será salvo  [required]

**Options**:

* `--help`: Show this message and exit.
