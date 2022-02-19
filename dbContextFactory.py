from settings import *

lines = []

model_list = []

def db_to_dbContext():

    with open(dbs[selected_db[""]], 'r') as f:
        lines = f.readlines()

    # Get all models
    for line in lines:

        if "CREATE TABLE" in line:
            model_list.append(get_model_in_line(line))

    # Imports
    dbContext[""] = "using ITTEKPremium_API.Models;\n"
    dbContext[""] += "using Microsoft.EntityFrameworkCore;\n"
    dbContext[""] += "using System;\n"
    dbContext[""] += "using System.Collections.Generic;\n"
    dbContext[""] += "using System.Linq;\n"
    dbContext[""] += "using System.Threading.Tasks;\n"
    
    dbContext[""] += "\nnamespace ITTEKPremium_API.Context\n{\n\t"
    dbContext[""] += "public class ITTEKPrintNeivacorDevDbContext : DbContext\n\t{\n\t\t"
    dbContext[""] += "public ITTEKPrintNeivacorDevDbContext(DbContextOptions<ITTEKPrintNeivacorDevDbContext> options)\n\t\t"
    dbContext[""] += ": base(options)\n\t\t{\n\t\t}\n\n\t\t"

    # FAZER LISTA DE MODELS
    for model in model_list:
        dbContext[""] += "public DbSet<" + model + "> " + model + " { get; set; }\n\t\t"

    dbContext[""] += "\n\t}\n}"


def create_dbContext(name, path):

    db_to_dbContext()

    file = open(path + ".cs", "w")
    file.close()

    write_in_dbContext(path)


def write_in_dbContext(path):

    with open(path + ".cs", "w") as f:
        f.write(dbContext[""])


def get_model_in_line(line):
    new_model = line
    new_model = line.replace("CREATE TABLE ", "")
    new_model = new_model.replace(" (", "")
    new_model = new_model.replace("_", "")
    new_model = new_model.replace("\n", "")
    return new_model