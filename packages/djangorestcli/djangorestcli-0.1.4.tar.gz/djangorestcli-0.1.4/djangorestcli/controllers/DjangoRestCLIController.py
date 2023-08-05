import os


class DjangoRestCLIController(object):
    currentDirectory = os.getcwd()
    moduleDirectory = os.path.dirname(os.path.abspath(__file__))
    modelTemplatePath = os.path.join(
        moduleDirectory, '..', 'templates', 'modeltemplate.txt')
    viewTemplatePath = os.path.join(
        moduleDirectory, '..', 'templates', 'viewtemplate.txt')
    serializerTemplatePath = os.path.join(
        moduleDirectory, '..', 'templates', 'serializertemplate.txt')
    routerTemplatePath = os.path.join(
        moduleDirectory, '..', 'templates', 'routertemplate.txt')
    with open(modelTemplatePath, 'r') as file:
        modelTemplate = file.read()
        file.close()
    with open(viewTemplatePath, 'r') as file:
        viewTemplate = file.read()
        file.close()
    with open(serializerTemplatePath, 'r') as file:
        serializerTemplate = file.read()
        file.close()
    with open(routerTemplatePath, 'r') as file:
        routerTemplate = file.read()
        file.close()

    def isADjangoDirectory(self):
        projectName = os.path.basename(self.currentDirectory)
        return (os.path.exists(os.path.join(self.currentDirectory, projectName))
                and os.path.exists(os.path.join(self.currentDirectory, 'manage.py')))

    def appExists(self):
        return os.path.exists(os.path.join(self.currentDirectory, self.appName))

    def generateDirectoryInApplication(self, directoryName):
        if not os.path.exists(os.path.join(self.currentDirectory,
                                           self.appName, directoryName)):
            os.mkdir(os.path.join(self.currentDirectory,
                                  self.appName, directoryName))

    def generateModelFile(self):
        with open(os.path.join(self.currentDirectory, self.appName, 'models', self.modelName+"Model.py"), "w") as file:
            file.write(self.modelTemplate.format(
                model_name=self.modelName))
            file.close()

    def generateViewFile(self):
        with open(os.path.join(self.currentDirectory, self.appName, 'views', self.modelName+"View.py"), "w") as file:
            file.write(self.viewTemplate.format(
                model_name=self.modelName, app_name=self.appName))
            file.close()

    def generateSerializerFile(self):
        with open(os.path.join(self.currentDirectory, self.appName, 'serializers', self.modelName+"Serializer.py"), "w") as file:
            file.write(self.serializerTemplate.format(
                model_name=self.modelName, app_name=self.appName))
            file.close()

    def addToInitModel(self):
        with open(os.path.join(self.currentDirectory, self.appName, "models", "__init__.py"), "a") as file:
            file.write('from .{} import *\n'.format(self.modelName+"Model"))
            file.close()

    def addToInitView(self):
        with open(os.path.join(self.currentDirectory, self.appName, "views", "__init__.py"), "a") as file:
            file.write('from .{} import *\n'.format(self.modelName+"View"))
            file.close()

    def addToInitSerializer(self):
        with open(os.path.join(self.currentDirectory, self.appName, "serializers", "__init__.py"), "a") as file:
            file.write(
                'from .{} import *\n'.format(self.modelName+"Serializer"))
            file.close()

    def generateRouterMessage(self):
        print('Add the code below to your urls.py:\n\n')
        print(self.routerTemplate.format(app_name=self.modelName,
                                         model_capitalize=self.modelName, model_name=self.modelName.lower()))

    def generate(self, args):
        self.appName, self.modelName = args.make[0].split('.')
        self.modelName = self.modelName.capitalize()
        if not self.isADjangoDirectory():
            raise TypeError("Not a django application")
        if not self.appExists():
            raise TypeError("Application don't exists")

        self.generateDirectoryInApplication('models')
        self.generateDirectoryInApplication('views')
        self.generateDirectoryInApplication('serializers')

        self.generateModelFile()
        self.generateViewFile()
        self.generateSerializerFile()

        self.addToInitModel()
        self.addToInitView()
        self.addToInitSerializer()

        self.generateRouterMessage()
