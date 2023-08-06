# jdTranslationHelper
With jdTranslationHelper you can translate your programs. The translation files are .lang files which has ths format:
```
key=Hello World
test=This is a test
```
The files are in a folder named after the language code e.g. en_GB.lang

Here is a example how to use this API:
```
from jdTranslationHelper import jdTranslationHelper

translations = jdTranslationHelper()
translations.loadDirectory("/home/User/translations")
print(translatios.translate("test"))
```
If we place the above en_GB.lang file in /home/User/translations, it will print This is a test. You can create files for any language.

You can also call jdTranslationHelper with arguemnts:  
lang=The language which should be loaded. If not specified, it will use the system language.  
defaultLanguage=The language that will be usesd, if there is no file with the system language. Default is en_GB.  

translate takes this argument:  
default: That will be returned, if the given key doesn't exists.
