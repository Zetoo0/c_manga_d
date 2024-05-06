from dotenv import load_dotenv,dotenv_values,set_key
import os
import manga
import argparse
load_dotenv()

#at start set the login stuffs for auth
username = os.getenv("USERNAME")
pw = os.getenv("PASSWORD")
personal_key = os.getenv("CLIENT_KEY")
secret_key = os.getenv("SECRET_KEY")

#get the access and refresh token
acc_token,refr_token = manga.Manga.authenticate(personal_key,secret_key,username,pw)

"""
EXAMPLE FOR LATER
# Parancssori argumentumok definiálása
parser = argparse.ArgumentParser(description='A program leírása')
parser.add_argument('-p', '--param', help='A -p opció leírása')
parser.add_argument('-t', '--another', help='A -t opció leírása')

# Parancssori argumentumok beolvasása
args = parser.parse_args()

# Argumentumok kezelése
if args.param:
    print('A -p opció értéke:', args.param)

if args.another:
    print('A -t opció értéke:', args.another)

"""