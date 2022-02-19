import shutil, os
from settings import *


def delete_files():
    if os.path.exists("APIs"):
        shutil.rmtree("APIs")
    if os.path.exists("Kotlin"):
        shutil.rmtree("Kotlin")


def db_script_convert(name):

    with open(old_dbs[0], 'r', encoding="utf-16") as f:
        lines = f.readlines()
        script = "CREATE DATABASE [" + name + "]\n\n"

    first_time = True
    table_name = ""
    for line in lines:

        if "CREATE TABLE" in line:

            table_name = get_model_in_line(line)

            if not first_time:
                script += "\n);"
            else:
                first_time = False
            script += "\n\nCREATE TABLE " + table_name + " (\n"
        
        else:
            
            for type in variable_types:

                if type in line.upper() and "NULL" in line and "ALTER DATABASE" not in line:

                    custom_line = line.strip()
                    variable_name = custom_line.split("]")[0]
                    variable_name = variable_name[1:]

                    if type == "VARCHAR":
                        quant = get_varchar_quantity(line)
                        script += "\n\t" + variable_name + " " + type + "(" + quant + ")"
                    else:
                        script += "\n\t" + variable_name + " " + type
                    
                    if "NOT NULL" in line:
                        script += " NOT NULL,"
                    else:
                        script += ","


    script += "\n);"
    create_file(name, script)


def create_file(name, script):

    file = open("dataBases/" + name + ".sql", "w")
    file.close()

    write_in_file(name, script)


def write_in_file(name, script):

    with open("dataBases/" + name + ".sql", "w") as f:
        f.write(script)


def get_model_in_line(line):
    new_model = line
    new_model = line.replace("CREATE TABLE [dbo].[", "")
    new_model = new_model.replace("](", "")
    #new_model = new_model.replace("_", "")
    new_model = new_model.replace("\n", "")
    return new_model

def get_varchar_quantity(line):
    result = line.split("(")[1]

    result = result.split(")")[0]

    return result