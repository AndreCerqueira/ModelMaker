
dbs = ["dataBases/bd_create.sql", "dataBases/new_db_create.sql"]
old_dbs = ["dataBases/old_db_create.sql"]
selected_db = {}

packages = {
    "ITTEK_Production": "com.ittekpremium.ittekproduction.Models", 
    "ITTEK_Manager": "com.ittekpremium.ittekmanager.Models"
    }

default_controller_name = "ITTEKNeivacorDevDbContext"

lines = []

models = {}
controllers = {}
kotlin_models = {}
dbContext = {}

variable_types = {"INT": "int", "BIT": "bool", "DATE": "DateTime", "TIME": "DateTime", "VARCHAR": "string", "FLOAT": "float"}

variable_types_kotlin = {"INT": "Int", "BIT": "Boolean", "DATE": "String", "TIME": "String", "VARCHAR": "String", "FLOAT": "Double"}

especial_variable_types = {"NVARCHAR": "string"}


