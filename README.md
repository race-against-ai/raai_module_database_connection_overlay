# RAAI Module Database Overlay
A Small QML Overlay intended for debugging the database Connection

## Stuff you need to change
- Change the ```README.md``` according to your project
- rename the ```your_project_folder``` to the name of your project
- edit the ```setup.cfg``` and change `your_project_folder` to the name of your project
- edit ```.gitattributes``` to the new folder
- put your GitHub or Volkswagen email in the ```setup.py```
- import and execute your main file from the project folder into the root ```main.py```
- adjust the ```pyinstaller.spec``` according to your project (mainly the name)

## Code Syntax
To test your code type syntax run

```
tox -e type
```

or to check the style syntax run
```
tox -e style
```

to run a lint check, enter
```
tox -e lint_check
```

To update your code when encountering errors on lint check, just run
```
tox -e lint_update
```
