import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
CODE = getenv('CODE', None)


def main():
    if CODE is None:
        print("Otwórz link:")
        print(
            f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&response_type=code&scope=https://www.googleapis.com/auth/youtube.force-ssl&redirect_uri=http://localhost&access_type=offline")
        input("\nKliknij aby kontynuować...\n")

        print("Skopiuj Code z linku i wklej do .env")
        print("Jeżeli link wyglądał tak:\n")
        print("http://localhost/?code=4/1239ufdsfsy7e8sh&scope=https://")
        print("\nto do .env wklejasz\n")
        print("CODE=4/1239ufdsfsy7e8sh")
        print("\nCode jest oczywiście dłuższy")
        print("uruchom ponownie ten skrypt")
        return

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = 'code='+CODE+'&client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET + \
        '&grant_type=authorization_code&redirect_uri=http://localhost'
    r = requests.post("https://www.googleapis.com/oauth2/v4/token",
                      headers=headers, data=data)
    print("do .env dopisz\n")
    refresh_token = r.json()['refresh_token']
    print(f"REFRESH_TOKEN={refresh_token}")


if __name__ == '__main__':
    main()
