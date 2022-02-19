import os
from apiFactory import create_api
from kotlinModelFactory import bd_to_kotlin_models, create_kotlin_model, create_kotlin_folders
from helper import delete_files, db_script_convert
from settings import *

# To Do 
# Insert Data in SQL Script
# Backup code from Controllers
# When changing Data Dases Change id to ID and chose to remove or not the [Key]


# Options
default_new_db_script_name = "new_db_create"
selected_db[""] = 0

default_db_name = "ITTEKNeivacorDev"
default_api_name = "ITTEKPremium_API"

def main():
    
    os.system('cls')

    print("Bem-Vindo ao ModelMaker [Version 2.0]!")
    print("Para mais informações: help\n\n")

    run = True
    while run:

        command = input()

        switcher = {
            "help":help,
            "cls":cls,
            "q":exit,
            "del-all":del_all,
            "gen-api":gen_api,
            "gen-kt":gen_kt,
            "gen-db":gen_db,
            "change-db":change_db,
            "exit":exit
        }

        if command == "q" or command == "exit":
            run = False
        else:
            func = switcher.get(command, lambda: "")
            func()


def help():
    print("Command List\n")
    print("help       ->  Show all commands.\n")
    print("exit | q   ->  Exit Program.\n")
    print("cls        ->  Clear Screen.\n")
    print("del-all    ->  Delete all Local Files.\n")
    print("gen-api    ->  Generate API Models, Controllers, Db Context based on a given db.\n")
    print("gen-kt     ->  Generate Kotlin Models based on a given db.\n")
    print("gen-db     ->  Generate New Db based on a given auto generated db.\n")
    print("change-db  ->  Change Selected Data Base. > Selected [" , selected_db[""] , "] [" , dbs[selected_db[""]] , "].\n")


def cls():
    os.system('cls')


def gen_api():
    create_api(default_api_name, default_db_name)


def gen_kt():
    
    create_kotlin_folders()
    
    for package in packages:
        bd_to_kotlin_models(packages[package])
        for model in kotlin_models:   
            create_kotlin_model(model, "Kotlin/" + package)

def del_all():
    delete_files()


def gen_db():
    db_script_convert(default_new_db_script_name)


def change_db():

    if selected_db[""] == 0:
        selected_db[""] = 1
    else:
        selected_db[""] = 0

    print("Current Db Selected -> [" , selected_db[""] , "] [" , dbs[selected_db[""]] , "].\n")


if __name__ == "__main__":
    main()