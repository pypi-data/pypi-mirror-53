
<h1 align="center">
  PyPonto
  <br>
</h1>

<h4 align="center">Plataforma para Registrar Pontos de Funcionários</h4>

<p align="center">

  <a href="https://travis-ci.org/hendrixcosta/pyponto">
    <img src="https://travis-ci.org/hendrixcosta/pyponto.svg?branch=master&style=flat-square" alt="Version">
  </a>
  
  <a href='https://coveralls.io/github/hendrixcosta/pyponto?branch=master'>
    <img src='https://coveralls.io/repos/github/hendrixcosta/pyponto/badge.svg?branch=master' alt='Coverage Status' />
  </a>

  <a href='https://pyponto.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/pyponto/badge/?version=latest' alt='Documentation Status' />
  </a>

  <a href="https://badge.fury.io/py/pyponto">
    <img src="https://badge.fury.io/py/pyponto.svg" alt="PyPI version" height="18">
  </a>
  
  
<p align="center">
  <a href="#recursos">Recursos</a> |
  <a href="#instalação">Instalação</a> |
  <a href="#como-usar">Como Usar</a> |
  <a href="#créditos">Créditos</a>
</p>


## Recursos

-   Registrar novos Funcionários
-   Registrar Pontos (horários) de funcionários
-   Calcular horas trabalhadas no mês do funcionário


## Subir plataforma com Docker

O PyPonto pode ser facilmente inicializado com o comando a seguir:

```shell
docker-compose up
```


## Desenvolvimento


```shell

git clone git@github.com:hendrixcosta/pyponto.git

cd pyponto/

./run-dev.sh

```



## Utilização


Para adicionar Novo Colaborador:
```shell
curl -X POST -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/colaborador/" -d '{"name":"Colaborador1","registration":"0001"}'
```

Para visualizar todos colaboradores:
```shell
curl -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/colaborador/"
```

Para adicionar registro de ponto:
```shell
curl -X POST -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/ponto/" -d '{"colaborador_id":"1","tipo":"entrada", "horario":"2019-01-01 12:00:00"}'

curl -X POST -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/ponto/" -d '{"colaborador_id":"1","tipo":"saida", "horario":"2019-01-01 17:00:00"}'
```

Para visualizar todos registros de Pontos
```shell
curl -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/ponto/"
```

Para visualizar detalhes de registro de ponto do mês

    Paramêtros: id do funcionario e mes para detalhes

```shell
curl -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/pontomes/?id=1&mes=1"


curl -X POST -H 'Content-Type: application/json' -u admin:admin "http://127.0.0.1:8000/pontomes/" -d '{"colaborador_id":"1","mes":"1"}'
```


## Créditos

Copyright (C) 2019 por Hendrix Costa
