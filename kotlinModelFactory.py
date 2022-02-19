import os
from struct import pack
from settings import *

variables = {}


def get_model_in_line(line):
    new_model = line
    new_model = line.replace("CREATE TABLE ", "")
    new_model = new_model.replace(" (", "")
    new_model = new_model.replace("_", "")
    new_model = new_model.replace("\n", "")
    return new_model

def bd_to_kotlin_variables():

    with open(dbs[selected_db[""]], 'r') as f:
        lines = f.readlines()

    current_model = ""
    for line in lines:

        if "CREATE TABLE" in line:
            current_model = get_model_in_line(line)
            variables[current_model] = {}

        if current_model != "null":

            type_found = False
            for type in variable_types:

                if type in line and not type_found:

                    type_found = True

                    variable_name = line.split(type)[0]
                    variable_name = variable_name.replace("    ", "")
                    variable_name = variable_name.replace(" ", "")

                    variables[current_model][variable_name] = type




def bd_to_kotlin_models(package):

    bd_to_kotlin_variables()

    with open(dbs[selected_db[""]], 'r') as f:
        lines = f.readlines()

    for line in lines:

        if "CREATE TABLE" in line:
            
            new_model = get_model_in_line(line)

            # Imports
            kotlin_models[new_model] = "package " + package # <- change
            kotlin_models[new_model] += "\n\nimport org.json.JSONObject\n\n"

            # Class Start
            kotlin_models[new_model] += "class " + new_model + " \n{"

            # Variables
            kotlin_models[new_model] += "\n\t//Variables"
            for variable in variables[new_model]:

                type = variable_types_kotlin[variables[new_model][variable]]
                #print("model: " + new_model + " | name: " + variable + " | type: " + type)

                kotlin_models[new_model] += "\n\tvar " + variable + ": " + type + "? = null"

            # Empty Constructor
            kotlin_models[new_model] += "\n\n\tconstructor(){ \n\t}\n"
            
            # Constructor with everything
            kotlin_models[new_model] += "\n\tconstructor("

            for variable in variables[new_model]:
                type = variable_types_kotlin[variables[new_model][variable]]
                kotlin_models[new_model] += "\n\t\t" + variable + ": " + type + ", "

            kotlin_models[new_model] += "\n\t){"
            
            for variable in variables[new_model]:
                kotlin_models[new_model] += "\n\t\tthis." + variable + " = " + variable + ""

            kotlin_models[new_model] += "\n\t}\n"

            # To Json
            kotlin_models[new_model] += "\n\tfun toJson(): JSONObject { \n\t"
            kotlin_models[new_model] += "\n\t\tval jsonObject = JSONObject()\n"

            # To Json variables
            for variable in variables[new_model]:
                kotlin_models[new_model] += "\n\t\tjsonObject.put(\"" + variable + "\", " + variable + ")"

            kotlin_models[new_model] += "\n\n\t\treturn jsonObject"
            kotlin_models[new_model] += "\n\t}\n"

            # From Json
            kotlin_models[new_model] += "\n\tcompanion object {"
            kotlin_models[new_model] += "\n\t\tfun fromJson(jsonObject: JSONObject) : " + new_model + " { \t"
            kotlin_models[new_model] += "\n\t\t\tval " + new_model.lower() + " = " + new_model + "()\n"

            # From Json variables
            for variable in variables[new_model]:
                
                type = variable_types_kotlin[variables[new_model][variable]]

                kotlin_models[new_model] += "\n\t\t\t" + new_model.lower() + "." + variable + " = if (!jsonObject.isNull(\"" + variable + "\")) jsonObject.get" + type + "(\"" + variable + "\") else null"

            kotlin_models[new_model] += "\n\n\t\t\treturn " + new_model.lower()
            kotlin_models[new_model] += "\n\t\t}"
            kotlin_models[new_model] += "\n\t}\n"

            # End
            kotlin_models[new_model] += "\n}"


def create_kotlin_model(name, path):

    file = open(path + "/" + name + ".kt", "w")
    file.close()

    write_in_kotlin_model(name, path)


def write_in_kotlin_model(name, path):

    with open(path + "/" + name + ".kt", "w") as f:
        f.write(kotlin_models[name])


def create_kotlin_folders():

    if not os.path.exists("Kotlin"):
        os.mkdir("Kotlin")

    for package in packages:
        if not os.path.exists("Kotlin/" + package):
            os.mkdir("Kotlin/" + package)