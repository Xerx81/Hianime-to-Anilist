
# Hianime to Anilist

The default export.xml file of Hianime cannot be directly imported into Anilist. Therefore, I wrote this python script which can restructure the xml document so that it can be easily imported by Anilist.

## Usage 1:

- Go to the [Hianime to Al](https://hianimetoal.pythonanywhere.com/).

- Upload your xml file. (make sure the file is name is "export.xml")

- Click on transform and download the new xml file, which can be directly imported by [Anilist](https://anilist.co/settings/import)

## Usage 2:
If for some reason site isn't working you can also follow these steps to use the program.

- Clone this repository.
```
git clone https://github.com/Xerx81/Hianime-to-Anilist.git
```

- Change the directory.
```
cd Hianime-to-Anilist
```

- Create Virtual enviornment.
```
python3 -m venv .venv
```
- Activate the venv.
```
source .venv/bin/activate
```

- Install flask.
```
pip install flask
```

- Run the flask app.
```
python3 app.py
```

- Click on the link of flask server, the site will open in your browser.

## Contribution:

- Report issues: If you encounter any bugs or unexpected behavior, please open an issue on the GitHub repository.

- Suggest features: If you have ideas for new features, feel free to open a feature request.

- Contribute code: Fork the repository, make your changes, and submit a pull request. Please follow the standard code style and formatting guidelines.


