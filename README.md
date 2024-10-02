# 🥞 Stack

- [Python v3.12](https://www.python.org/doc/)
- [Django v5.1](https://docs.djangoproject.com/en/5.1/)

## ⚙️ Configurando o projeto

### ⚠️ Requisitos

Para executar o projeto localmente basta possuir o [docker](https://docs.docker.com/engine/install/) e [docker compose](https://docs.docker.com/compose/install/) instalados.

## 🆙 Executando o projeto

Primeiro, clone o projeto:

### via HTTPS

```bash
git clone https://github.com/abc.git
```

### via SSH

```bash
git clone git@github.com:def/abc.git
```

Agora, rode o seguinte comando:

```bash
docker-compose up -d
```

Feito tudo isso, o projeto estará executando no endereço [localhost:8080/admin](http://localhost:8080/admin).

Acessar com usuário e senha "admin".

## Funcionalidades

### Importar arquivo csv

Entrar no container:
```bash
docker-compose exec web sh
```

Executar:
```bash
poetry run python manage.py load_data
```

### Cadastrar produtos, seu valor e quantidade em estoque

Para cadastrar acessar:
```bash
http://localhost:8080/admin/data_loader/product/
```

Para ver resumo de todos os produtos e "Valor Total em Estoque" acessar:

(É uma tela customizada via templates)
```bash
http://localhost:8080/admin/data_loader/product/product-summary/
```

Pelo fato do projeto estar sendo executado através de um container e com um volume configurado, qualquer alteração feita no código fonte será replicada automaticamente, sem necessidade de reiniciar o container.

## 👌 Boas práticas da equipe

- 🧼 Código limpo;
- 🤓 Commit dentro do [padrão](https://www.conventionalcommits.org/en/v1.0.0/#summary);
- 🤷 PR explicativa;
- 👀 Code Review construtivo;
