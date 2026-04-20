# geo-cli

toolkit de ferramentas construídas por mim durante a graduação em geologia na unicamp

**Usage**:

```console
$ geo-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `geo2utm`: converte coordenadas geográficas...
* `utm2geo`: converte coordenadas UTM (EPSG:31983 como...
* `map`: gera um mapa interativo a partir de...
* `mineralformula`: constroe a tabela de formula mineral com...
* `escala`: calcula a distância real correspondente a...
* `indicecor`: calcula o índice de cor de uma rocha com...
* `mergulho`
* `idaderocha`

## `geo-cli geo2utm`

converte coordenadas geográficas (EPSG:4326 como padrão) para UTM (EPSG:31983 como padrão).

**Usage**:

```console
$ geo-cli geo2utm [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada (deve conter as colunas &quot;lat&quot; e &quot;lon&quot;)  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com os dados convertidos será salvo  [required]

**Options**:

* `--source-epsg TEXT`: EPSG code for source coordinate system  [default: EPSG:4326]
* `--target-epsg TEXT`: EPSG code for target coordinate system  [default: EPSG:31983]
* `--help`: Show this message and exit.

## `geo-cli utm2geo`

converte coordenadas UTM (EPSG:31983 como padrão) para geográficas (EPSG:4326 como padrão).

**Usage**:

```console
$ geo-cli utm2geo [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada (deve conter as colunas &quot;easting&quot; e &quot;northing&quot;)  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com os dados convertidos será salvo  [required]

**Options**:

* `--source-epsg TEXT`: EPSG code for source coordinate system  [default: EPSG:31983]
* `--target-epsg TEXT`: EPSG code for target coordinate system  [default: EPSG:4326]
* `--help`: Show this message and exit.

## `geo-cli map`

gera um mapa interativo a partir de coordenadas em um arquivo CSV.

**Usage**:

```console
$ geo-cli map [OPTIONS] INPUT_FILE [TITLE] [ID]
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada  [required]
* `[TITLE]`: título do mapa  [default: Mapa]
* `[ID]`: nome da coluna a ser usada como identificador dos pontos no mapa (opcional)

**Options**:

* `--zoom-start INTEGER`: nível de zoom inicial do mapa  [default: 2]
* `--help`: Show this message and exit.

## `geo-cli mineralformula`

constroe a tabela de formula mineral com base em um arquivo CSV contendo as colunas das moléculas e suas respectivas análises quimicas.

**Usage**:

```console
$ geo-cli mineralformula [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: caminho para o arquivo CSV de entrada  [required]
* `OUTPUT_FILE`: caminho onde o CSV final com a tabela de fórmulas minerais será salvo  [required]

**Options**:

* `--help`: Show this message and exit.

## `geo-cli escala`

calcula a distância real correspondente a uma medida feita em uma carta, com base na escala fornecida.

**Usage**:

```console
$ geo-cli escala [OPTIONS] ESCALA DISTANCIA_CARTA
```

**Arguments**:

* `ESCALA`: escala cartográfica  [required]
* `DISTANCIA_CARTA`: distância medida na carta (em cm)  [required]

**Options**:

* `--help`: Show this message and exit.

## `geo-cli indicecor`

calcula o índice de cor de uma rocha com base na proporção de minerais escuros (m) presente nela.

**Usage**:

```console
$ geo-cli indicecor [OPTIONS]
```

**Options**:

* `-o, --olivina FLOAT`: Porcentagem visual de Olivina  [default: 0.0]
* `-p, --piroxenio FLOAT`: Porcentagem visual de Piroxênio  [default: 0.0]
* `-b, --biotita FLOAT`: Porcentagem visual de Biotita  [default: 0.0]
* `-a, --anfibolio FLOAT`: Porcentagem visual de Anfibólio  [default: 0.0]
* `--opacos FLOAT`: Percentagem de minerais metálicos/opacos (Magnetite, Ilmenite)  [default: 0.0]
* `--outros FLOAT`: Outros minerais ferromagnesianos (Granada, Turmalina, etc.)  [default: 0.0]
* `--help`: Show this message and exit.

## `geo-cli mergulho`

**Usage**:

```console
$ geo-cli mergulho [OPTIONS] LENGTH ANGLE
```

**Arguments**:

* `LENGTH`: comprimento do afloramento na superfície  [required]
* `ANGLE`: ângulo de mergulho do afloramento  [required]

**Options**:

* `--help`: Show this message and exit.

## `geo-cli idaderocha`

**Usage**:

```console
$ geo-cli idaderocha [OPTIONS]
```

**Options**:

* `-p, --pai FLOAT`: quantidade do isótopo pai  [required]
* `-f, --filho FLOAT`: quantidade do isótopo filho  [required]
* `-mv, --meia-vida FLOAT`: meia-vida do isótopo pai  [required]
* `--help`: Show this message and exit.
