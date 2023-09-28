import configparser
import shutil
from os.path import exists

mainConfigPath = 'config.ini'
defaultMainConfigPath = 'defaultConfig.ini'
mainConfigTokenKeys = {"TOKEN", "E6TOKEN", "SAUCENAOTOKEN"}
mainConfigSections = {
    "Tokens": mainConfigTokenKeys
}
def ensureConfigWithSectionsAtPath(keysSectionsDict, path, defaultPath):
    newConfig = configparser.ConfigParser()
    newConfig.read(path)
    configIsGood = True
    if exists(mainConfigPath):
        for section in keysSectionsDict:
            keysThisSection = keysSectionsDict[section]
            for option in keysThisSection:
                try:
                    keyValue = newConfig.get("Tokens", option)
                    if "your-" in keyValue and "-here" in keyValue:
                        print(f'key {path}, {section}: {option} is default!')
                except configparser.NoOptionError:
                    configIsGood = False
                    newConfig.set(section, option, None)
                    print(f'key {path}, {section}: {option}  is missing')
    else:
        print(f'{path} does not exist! copying..')
        shutil.copy(defaultPath, path)
        return ensureConfigWithSectionsAtPath(keysSectionsDict, path, defaultPath)

    if not configIsGood:
        with open(path, 'wb') as configfile:
            newConfig.write(configfile)

    return newConfig

mainConfig = ensureConfigWithSectionsAtPath(mainConfigSections, mainConfigPath, defaultMainConfigPath)
def getConfig(which):
    if which == "main":
        return mainConfig