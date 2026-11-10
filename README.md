# Django POC

Python 3.13, Django 5.2 e PostgreSQL 17. Serve Docker Desktop avviato.

## Struttura

- `app/src/`: sorgenti Django.
- `app/tests/`: test organizzati per app.
- `app/requirements.txt`: dipendenze Python.
- `docker/`: Dockerfile, Compose e template di generazione.
- `data/postgres/`: dati persistenti del database, esclusi da Git.
- `.env`: configurazione locale, esclusa da Git.

## Primo avvio

Dalla radice della repo:

```bash
make init
make build
make generate
make migrate
make serve
```

`generate` richiede `app/src/` vuota. Crea il progetto e l'app `poc`,
configura PostgreSQL e prepara pagine e test. Se i sorgenti esistono già,
prosegui con `make migrate` e `make serve`.

Django ricarica i file Python quando li salvi. `Ctrl+C` ferma i servizi.

## Indirizzi

- [Homepage](http://localhost:8000/): pagina iniziale con link ad admin e API.
- [Django Admin](http://localhost:8000/admin/): pannello amministrativo.

Per creare un amministratore:

```bash
make superuser
```

Il database è raggiungibile dal tuo computer su `localhost:5433` e da Django su `db:5432`.
Nome, utente e password sono nel `.env`.

## Comandi principali

| Comando | Effetto |
| --- | --- |
| `make help` | Mostra tutti i comandi |
| `make test` | Esegue i test in `app/tests/` |
| `make app NAME=orders` | Crea e registra un'altra app, con la cartella dei test |
| `make migrations` | Genera migrazioni dopo modifiche ai model |
| `make migrate` | Applica le migrazioni al database |
| `make rebuild` | Ricostruisce e riavvia dopo modifiche alle dipendenze |
| `make shell` | Apre la console Python di Django |
| `make manage ARGS="..."` | Esegue un altro comando Django |

`app/` è montata in `/app` nel container. I dati PostgreSQL restano in
`data/postgres/`: eliminare questa cartella cancella il database.

Configurazione e credenziali di esempio sono destinate allo sviluppo locale.
