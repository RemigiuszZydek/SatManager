## Tabela: Users (Użytkownicy)
| Kolumna      | Typ       | Opis                               |
|--------------|-----------|-----------------------------------|
| id           | INT       | Unikalny identyfikator użytkownika|
| name         | TEXT      | Imię i nazwisko                   |
| role         | TEXT      | Rola: admin / koordynator / pracownik |
| login        | TEXT      | Login do aplikacji                |
| password     | TEXT      | Hasło (hashowane)                 |

---

## Tabela: Tasks (Zlecenia)
| Kolumna          | Typ       | Opis                                     |
|------------------|-----------|-----------------------------------------|
| id               | INT       | Unikalny identyfikator zlecenia         |
| title            | TEXT      | Krótka nazwa zlecenia                   |
| description      | TEXT      | Szczegóły zlecenia                       |
| status           | TEXT      | Status: nieprzypisane / w trakcie / wykonane / odrzucone |
| assigned_user_id | INT       | ID pracownika przypisanego do zlecenia (NULL jeśli nieprzypisane) |
| date             | DATE      | Data realizacji zlecenia                 |

---

## Tabela: Materials (Materiały)
| Kolumna      | Typ       | Opis                                     |
|--------------|-----------|-----------------------------------------|
| id           | INT       | Unikalny identyfikator materiału        |
| name         | TEXT      | Nazwa materiału                          |
| quantity     | INT       | Ilość użyta w zleceniu                   |
| task_id      | INT       | ID zlecenia, z którym materiał jest powiązany |

---

## Tabela: Revenue (Przychód)
| Kolumna      | Typ       | Opis                                     |
|--------------|-----------|-----------------------------------------|
| id           | INT       | Unikalny identyfikator                   |
| task_id      | INT       | ID zlecenia                               |
| amount       | FLOAT     | Kwota przychodu związana z zleceniem     |

## Relacje między tabelami

- `Users.id` → `Tasks.assigned_user_id` (1:N) – jeden użytkownik może mieć wiele zleceń
- `Tasks.id` → `Materials.task_id` (1:N) – jedno zlecenie może mieć wiele materiałów
- `Tasks.id` → `Revenue.task_id` (1:1 lub 1:N) – jedno zlecenie może mieć przychód


```mermaid
erDiagram
    USERS ||--o{ TASKS : assigned
    TASKS ||--o{ MATERIALS : uses
    TASKS ||--o{ REVENUE : generates
