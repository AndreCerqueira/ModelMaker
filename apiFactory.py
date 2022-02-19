import os, shutil
from modelFactory import bd_to_models, create_model
from controllerFactory import bd_to_controllers, create_controller
from dbContextFactory import create_dbContext
from settings import *

def create_api(name, name_db):

    MODELS_PATH = "APIs/" + name + "/models"
    CONTROLLERS_PATH = "APIs/" + name + "/controllers"
    DB_CONTEXT_PATH = "APIs/" + name + "/" + name_db + "DbContext"

    create_folders(name, MODELS_PATH, CONTROLLERS_PATH)

    # Create a dbContext
    create_dbContext(name_db, DB_CONTEXT_PATH)

    # Create a model for each table
    bd_to_models()
    for model in models:
        create_model(model, MODELS_PATH)

    # Create a controller for each table
    bd_to_controllers()
    for model in models:
        create_controller(model, CONTROLLERS_PATH)


def create_folders(name, MODELS_PATH, CONTROLLERS_PATH):

    if not os.path.exists("APIs"):
        os.mkdir("APIs")
    
    if not os.path.exists("APIs/" + name):
        os.mkdir("APIs/" + name)
        os.mkdir(CONTROLLERS_PATH)
        os.mkdir(MODELS_PATH)

