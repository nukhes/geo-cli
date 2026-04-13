# geocoordenadas

programa em python para converter base de dados CSV entre diferentes sistemas de geolocalização

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `geo2utm`: converte coordenadas geográficas...
* `utm2geo`: converte coordenadas UTM (EPSG:31983 como...
* `map`: gera um mapa interativo a partir de...

## `geo2utm`

converte coordenadas geográficas (EPSG:4326 como padrão) para UTM (EPSG:31983 como padrão).

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

converte coordenadas UTM (EPSG:31983 como padrão) para geográficas (EPSG:4326 como padrão).

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

## `map`

gera um mapa interativo a partir de coordenadas em um arquivo CSV.

**Usage**:

```console
$ map [OPTIONS] INPUT_FILE [TITLE] [ID]
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada  [required]
* `[TITLE]`: título do mapa  [default: Mapa]
* `[ID]`: nome da coluna a ser usada como identificador dos pontos no mapa (opcional)

**Options**:

* `--zoom-start INTEGER`: nível de zoom inicial do mapa  [default: 2]
* `--help`: Show this message and exit.
