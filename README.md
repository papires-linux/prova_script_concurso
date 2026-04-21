

# Criacao de um banco de dados

```bash
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
```


### Conectar 
```bash
docker exec -ti some-postgres bash
```

# 
# Estrutura da tabela concursos_all no banco de dados:


```sql
CREATE TABLE concursos_all (
    id SERIAL PRIMARY KEY,
    url TEXT,
    cargo TEXT,
    ano VARCHAR(4),
    orgao TEXT,
    instituicao TEXT
);

```