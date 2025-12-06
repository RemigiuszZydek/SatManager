# SatManager - MVP i User Stories

## Funkcjonalności MVP

### Logowanie i użytkownicy
- Użytkownik może się zalogować (pracownik , admin, koordynator)\
- Koordynator może tworzyć nowych użytkowników tak samo jak admin
- Użytkownik może zmienić swoje hasło

### Zlecenia
- Koordynator może utworzyć nowe zlecenie (adres, data, materiały, opis)
- Koordynator może przypisać zlecenie do pracownika
- Pracownik widzi listę przypisanych zleceń
- Pracownik może oznaczyć zlecenie jako:
	- "wykonane"
	- "w trakcie"
	- "odrzucone"
- Pracownik może dodać krotkę na końcu zlecenia
# Materiały
- Rejestracja zużytych materiałów przy realizacji zlecenia
- Koordynator może zobaczyć raport zużytych materiałów ? 

# Przychody / Koszty
- Rejestracja dochodu z danego zlecenia ? 

## User Stories

| Rola | Chcę | Po co |
|------|------|-------|
| Admin | Zarządzać całym systemem, tworzyć konta, usuwać użytkowników, mieć dostęp do wszystkich zleceń i materiałów | Aby mieć pełną kontrolę nad systemem |
| Koordynator | Tworzyć i przypisywać zlecenia pracownikom | Aby efektywnie zarządzać pracą zespołu |
| Koordynator | Tworzyć konta pracowników | Aby dodać nowych członków zespołu do systemu |
| Koordynator | Widzieć statusy zleceń i zużyte materiały | Aby kontrolować postęp prac i koszty |
| Pracownik | Widzieć listę przypisanych zleceń | Aby wiedzieć, co mam do wykonania danego dnia |
| Pracownik | Oznaczać zlecenia jako „wykonane”, „w trakcie” lub „odrzucone” | Aby koordynator wiedział, na jakim etapie jest praca |
| Pracownik | Dodawać krótkie notatki do zlecenia | Aby przekazać dodatkowe informacje o realizacji |
| Pracownik | Zrezygnować z przypisanego zlecenia | Aby móc zwolnić zlecenie, którego nie mogę wykonać |
