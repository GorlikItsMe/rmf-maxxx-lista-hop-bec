# Skrypt nie działa ponieważ zmieniono wygląd strony.

# rmf-maxxx-lista-hop-bec

Automatyczne parsowanie listy hop bec i akutalizowanie playlisty na youtube

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Setup

### Google cloud

1. Utwórz nowy projekt https://console.cloud.google.com/projectcreate
2. Aktywuj api https://console.cloud.google.com/apis/library/youtube.googleapis.com
3. Ekran akceptacji OAuth. User Type wybieramy zewnętrzny i potem klikamy Utwórz. Podajemy nazwe, mail i inne wymagane dane. W zakresach nic nie musisz wybierać. Zapisz.
4. Nie zapomnij dodać do Użytkownicy testowi swój adres email
5. Dane logowania > Utwórz dane logowania > OAuth > Aplikacja komputerowa. Nazwa to: `rmf maxx bot`. Dostałeś identyfikator klienta (CLIENT_ID) oraz tajny klucz klienta (CLIENT_SECRET) zapisz je do `.env`

### User credentials

6. Dane logowania > Utwórz dane logowania. Wybieramy `YouTube Data API v3` i `Dane użytkownika` aby utworzyć klienta OAuth
7. Uruchom `generate_keys.py`. Otwórz wygenerowany link. Potwierdz że ufasz developerowi (sobie XD) kliknij Dalej. Zostaniesz przekierowany na stronę localhost?code=..... Skopiuj `Code` i wklej do `.env`
8. Uruchom ponownie `generate_keys.py` tym razem dostaniesz `REFRESH_TOKEN` który musisz wkleić do `.env`

### Run bot

9. Utwórz playliste na youtube i skopiuj id playlisty do `.env` do `PLAYLIST_ID`
10. Aby aktualizować playliste uruchamiaj cyklicznie `rmfmaxxx_hopbec.py`
