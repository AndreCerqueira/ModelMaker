from settings import *

lines = []

variables = {}

def bd_to_variables():

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

                if type in line and not type_found and "FOREIGN KEY" not in line:

                    type_found = True

                    variable_name = line.split(type)[0]
                    variable_name = variable_name.replace("    ", "")
                    variable_name = variable_name.replace(" ", "")

                    variables[current_model][variable_name] = variable_name



def bd_to_controllers():

    bd_to_variables()

    with open(dbs[selected_db[""]], 'r') as f:
        lines = f.readlines()

    for line in lines:

        if "CREATE TABLE" in line:
            
            new_model = line
            new_model = line.replace("CREATE TABLE ", "")
            new_model = new_model.replace(" (", "")
            new_model = new_model.replace("_", "")
            new_model = new_model.replace("\n", "")

            model_sql = line
            model_sql = line.replace("CREATE TABLE ", "")
            model_sql = model_sql.replace(" (", "")
            model_sql = model_sql.replace("\n", "")

            # Imports
            controllers[new_model] = "using ITTEKPremium_API.Context;\n"
            controllers[new_model] += "using ITTEKPremium_API.Models;\n"
            controllers[new_model] += "using Microsoft.AspNetCore.Mvc;\n"
            controllers[new_model] += "using Microsoft.EntityFrameworkCore;\n"
            controllers[new_model] += "using System;\n"
            controllers[new_model] += "using System.Collections.Generic;\n"
            controllers[new_model] += "using System.Linq;\n"
            controllers[new_model] += "using System.Threading.Tasks;\n\n"

            # Class Start
            controllers[new_model] += "namespace ITTEKPremium_API.Controllers\n{\n\t"
            controllers[new_model] += "[Route(\"api/\")]\n\t"
            controllers[new_model] += "[ApiController]\n\t"
            controllers[new_model] += "public class " + new_model + "Controller : Controller \n\t{\n\t\t"

            # Get All function
            controllers[new_model] += "\n\t\t//GET ALL"
            controllers[new_model] += "\n\t\t[HttpGet]\n\t\t"
            controllers[new_model] += "[Route(\"[controller]\")]\n\t\t"

            controllers[new_model] += "public async Task<ActionResult<List<" + new_model + ">>> Get([FromServices] " + default_controller_name + " context)\n\t\t{\n\t\t\t"

            controllers[new_model] += "var all" + new_model + " = await context." + new_model + ".FromSqlRaw(\"SELECT * FROM " + model_sql + ";\").ToListAsync();\n\t\t\t"
            controllers[new_model] += "return all" + new_model + ".ToList();\n\t\t}"

            # Get By ID function
            controllers[new_model] += "\n\n\n\t\t//GET BY ID"
            controllers[new_model] += "\n\t\t[HttpGet]\n\t\t"
            controllers[new_model] += "[Route(\"[controller]/{id:int}\")]\n\t\t"
            
            controllers[new_model] += "public async Task<ActionResult<List<" + new_model + ">>> GetById([FromServices] " + default_controller_name + " context, int id)\n\t\t{\n\t\t\t"

            controllers[new_model] += "var " + new_model + "Id = await context." + new_model + ".FromSqlRaw(\"SELECT * FROM " + model_sql + "; WHERE ID=\"+ id).ToListAsync();\n\t\t\t"
            controllers[new_model] += "return " + new_model + "Id;\n\t\t}"

            # Post function
            controllers[new_model] += "\n\n\n\t\t//POST"
            controllers[new_model] += "\n\t\t[HttpPost]\n\t\t"
            controllers[new_model] += "[Route(\"[controller]\")]\n\t\t"

            controllers[new_model] += "public async Task<ActionResult<" + new_model + ">> Post([FromServices] " + default_controller_name + " context, [FromBody] " + new_model + " model) \n\t\t{\n\t\t\t"
            controllers[new_model] += "if (ModelState.IsValid) \n\t\t\t{\n\t\t\t\t"
            controllers[new_model] += "context." + new_model + ".Add(model);\n\t\t\t\t"
            controllers[new_model] += "await context.SaveChangesAsync();\n\t\t\t\t"
            controllers[new_model] += "return model; \n\t\t\t}\n\t\t\t"
            controllers[new_model] += "else \n\t\t\t{\n\t\t\t\t return BadRequest(ModelState); \n\t\t\t} \n\t\t}"
            
            # Put
            controllers[new_model] += "\n\n\n\t\t//PUT"
            controllers[new_model] += "\n\t\t[HttpPut(\"[controller]/{id}\")]\n\t\t"
            controllers[new_model] += "public async Task<ActionResult<" + new_model + ">> Put([FromServices] " + default_controller_name + " context, [FromBody] " + new_model + " model, int id)\n\t\t"
            controllers[new_model] += "{\n\t\t\ttry\n\t\t\t{\n\t\t\t\tif (ModelState.IsValid)\n\t\t\t\t{\n\t\t\t\t\tvar entity = context." + new_model + ".FirstOrDefault(e => e.id == id);"
            controllers[new_model] += "\n\t\t\t\t\tif (entity == null)\n\t\t\t\t\t{\n\t\t\t\t\t\treturn BadRequest(ModelState);\n\t\t\t\t\t}\n\t\t\t\t\telse\n\t\t\t\t\t{"
            for variable in variables[new_model]:
                controllers[new_model] += "\n\t\t\t\t\t\tentity." + variable + " = model." + variable + ";"

            controllers[new_model] += "\n\n\t\t\t\t\t\tawait context.SaveChangesAsync();\n\t\t\t\t\t\treturn model;\n\t\t\t\t\t}"

            controllers[new_model] += "\n\t\t\t\t}\n\t\t\t\telse\n\t\t\t\t{\n\t\t\t\t\treturn BadRequest(ModelState);\n\t\t\t\t}\n\t\t\t}"
            controllers[new_model] += "\n\t\t\tcatch (Exception ex)\n\t\t\t{\n\t\t\t\treturn BadRequest(ModelState);\n\t\t\t}\n\t\t}"

            # Delete
            controllers[new_model] += "\n\n\n\t\t//DELETE"
            controllers[new_model] += "\n\t\t[HttpDelete(\"[controller]/{id}\")]"
            controllers[new_model] += "\n\t\tpublic void Delete(int id)\n\t\t{\n\t\t}"

            # End
            controllers[new_model] += "\n\t}\n}"

            model_catched = new_model


def create_controller(name, path):

    file = open(path + "/" + name + "Controller.cs", "w")
    file.close()

    write_in_controller(name, path)


def write_in_controller(name, path):

    with open(path + "/" + name + "Controller.cs", "w") as f:
        f.write(controllers[name])


def get_model_in_line(line):
    new_model = line
    new_model = line.replace("CREATE TABLE ", "")
    new_model = new_model.replace(" (", "")
    new_model = new_model.replace("_", "")
    new_model = new_model.replace("\n", "")
    return new_model
