Diagram działania

```mermaid
flowchart TD
    A[Start] --> B[Koordynator loguje się]
    B --> C[Tworzy nowe zlecenie]
    C --> D{Czy przypisane do pracownika?}
    D -- Tak --> E[Pracownik widzi zlecenie w aplikacji mobilnej]
    D -- Nie --> F[Zlecenie pozostaje nieprzypisane]
    F --> G[Pracownik może wziąć zlecenie do siebie]
    G --> E
    E --> H[Pracownik wykonuje zlecenie]
    H --> I{Status zlecenia?}
    I -- W trakcie --> E
    I -- Wykonane --> J[Koordynator widzi zaktualizowany status]
    I -- Odrzucone / Rezygnacja --> J
    J --> K[Koordynator sprawdza zużyte materiały i przychód]
    K --> L[End]
