from settings import *

lines = []

without_key = False

def write_line(line, model_catched, type, variable_type):
    variable_name = line.split(type)[0]
    variable_name = variable_name.replace("    ", "")
    new_line = ""

    # Add Data Anotations

    if type == "VARCHAR":
        quantity = line.split('VARCHAR(')[1].split(')')[0]
        if (quantity == "max"):
            quantity = 250
        new_line += "\n\t\t[StringLength(" + quantity + ", ErrorMessage = \"Max Characters Limit Reached\")]"
        
    if variable_type == "DateTime":
        new_line += "\n\t\t[DataType(DataType.Date)]"
        new_line += "\n\t\t[DisplayFormat(DataFormatString = \""

        if "DATETIME" in line:
            new_line += "{00:00:00:yyyy-MM-dd}"
        else:
            if type == "DATE":
                new_line += "{0:yyyy-MM-dd}"
            else:
                if type == "TIME":
                    new_line += "{00:00:00:0}"
                
        new_line += "\", ApplyFormatInEditMode = true)]"

    new_line += "\n\t\tpublic " + variable_type

    if "NOT NULL" in line or "PRIMARY KEY" in line :
        new_line += " "
    else:
        new_line += "? "

    new_line += variable_name + "{ get; set; }\n"

    models[model_catched] += new_line


def bd_to_models():
    
    with open(dbs[selected_db[""]], 'r') as f:
        lines = f.readlines()

    model_catched = ""
    for line in lines:

        if model_catched != "":

            type_found = False
            for type in variable_types:

                if type in line and not type_found and "FOREIGN KEY" not in line:

                    for especial_type in especial_variable_types:

                        if especial_type not in line:
                            type_found = True
                            write_line(line, model_catched, type, variable_types[type])
                        else:
                            type_found = True
                            write_line(line, model_catched, especial_type, especial_variable_types[especial_type])


            if ");" in line:
                models[model_catched] += "\n\t}\n}"
                model_catched = ""


        if "CREATE TABLE" in line:
            
            new_model = line
            new_model = line.replace("CREATE TABLE ", "")
            new_model = new_model.replace(" (", "")
            new_model = new_model.replace("_", "")
            new_model = new_model.replace("\n", "")

            models[new_model] = "using System;\n"
            models[new_model] += "using System.ComponentModel.DataAnnotations;\n"
            models[new_model] += "using System.ComponentModel.DataAnnotations.Schema;\n\n"

            models[new_model] += "namespace ITTEKPremium_API.Models\n{\n\tpublic class " + new_model + " \n\t{"

            if not without_key:
                models[new_model] += "\n\t\t[Key]"
            
            model_catched = new_model


def create_model(name, path):

    file = open(path + "/" + name + ".cs", "w")
    file.close()

    write_in_model(name, path)


def write_in_model(name, path):

    with open(path + "/" + name + ".cs", "w") as f:
        f.write(models[name])

