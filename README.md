# SatManager - System do delegowania zleceń dla firmy zajmującej się montażem telewizji satelitarnej i naziemnej

## Opis projektu
SatManager to aplikacja która ma wspierać delegowanie zleceń między pracowników w firmie zajmującej się montażem telewizji satelitarnej i naziemnej. Umożliwia tworzenie i przypisywanie zleceń konkretnemu pracownikowi. Koordynatorzy natomiast mają możliwość monitorowania stanu danego zlecenia. Projekt ma pomóc ograniczyć chaos oraz ułatwić dzienną pracę.

## Cele projektu
- Usprawnienie przydzielania zleceń pracownikom
- Monitorowanie statusu zlecenia w czasie rzeczywistym
- Śledzenie użycia materiałów i części montażowych
- Zapewnienie prostego i intuicyjnego interfejsu mobilnego dla pracowników

## Funkcjonalność MVP (minimum viable product)
- Logowanie użytkowników
- Tworzenie i edytowanie zleceń
- Przypisywanie zleceń konkretnym pracownikom
- Lista zleceń pracownika w aplikacji mobilnej
- Oznaczenie zleceń jako "wykonane", "w trakcie", "odrzucone"
- Dodawanie krótkich notatek na temat zlecenia
- Dane zlecenia - co jest do wykonania, co jest potrzebne? , adres, data
- Rejestracja użytych materiałów
- Rejestracja przychodu za dane zlecenie

## Flow działania
1. Admin loguje się do systemu
2. Tworzy nowe zlecenie (adres, data, materiały, opis)
3. Przypisuje zlecenie danemu pracownikowi lub sobie
4. Pracownik widzi zlecenie w aplikacji mobilnej
5. Pracownik wykonuje zlecenie i oznacza status
6. Admin widzi aktualny stan i zużyte materiały

## Technologie
- **Backend:** Python (FastAPI lub django) w zależności jak bardzo bede chciał rozwijać projekt
- **Frontend mobilny:** Flutter
- **Baza danych:** SQlite / PostgreSQL lub MariaDB jeszcze nie wiem

[[Funkcjonalności]]



[[Diagram działania]]



[[Struktura bazy danych]]
