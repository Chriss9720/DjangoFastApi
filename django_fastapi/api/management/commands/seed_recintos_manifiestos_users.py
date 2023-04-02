from logging import exception
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from api.models import User

import json, os

REFRESH = "refresh"
CLEAR = "clear"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    help = "Seed the database's catalogues"

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        run_seed(self, options["mode"])
        self.stdout.write("Finished data seeding.")

def user_test():
    with open(f'{BASE_DIR}/commands/json/listos/user_test.json', encoding='utf-8-sig') as json_file:
        data = json.load(json_file)
        password = make_password("12345")
        for value in data:
            try:
                User.objects.get_or_create(
                    username = value["username"],
                    password = password
                )
            except:
                print("")

def run_seed(self, mode):
    print("Usuarios")
    user_test()