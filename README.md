# Hybrid User Interfaces 

This repository hosts the survey data and website from the survey paper "Hybrid User Interfaces: Past, Present, and Future of Complementary Cross-Device Interaction in Mixed Reality" authored by Sebastian Hubenschmid, Marc Satkowski, Johannes Zagermann, Julián Méndez, Niklas Elmqvist, Steven Feiner, Tiare Feuchtner, Jens Emil Grønbæk, Benjamin Lee, Dieter Schmalstieg, Raimund Dachselt, and Harald Reiterer. 

## Reconstruction instructions: 

### To develop and deploy the website

1. `npm install` installs all the libraries you need to get the app running using the list from `package.json`.
2. `npm run build` updates and exports `index.html`, and the files in `dist/assets` for a static website. 
3. `npm run dev` the site locally (localhost) in development mode (updates to src files reload the site).
4. To deploy to Github Pages, push the `index.html` on `/dist` (created by `npm run build`) onto the `gh-pages` branch. The folder is in `.gitignore` so that `git checkout` does not affect it. 

### To create data files (python script) 

1. The [`Survey-Info.csv`](/src/data/Survey-Info.csv) file contains the core corpus described in the paper. 
   2. The taxonomy columns accept lists of strings (comma separated), or marks ("x") for values that apply. 
   3. `Name`, `Year`, `Authors` (comma separated), `DOI`, `Bibtex`, and `source` (default "handpicked") are required. 
2. Create the config and data json files: 
   1. [create-jsons.py](/src/data/create-jsons.py) describes the survey categories using the `includeProp`, `categories`, and `groups` dictionaries. 
   2. Running the script generates [survey-data.json](src/data/survey-data.json) and [survey-config.json](src/data/survey-config.json). 
   WARNING: The script deletes the existing files, if entries have been [manually added](#to-manually-add-papers), they will be lost. 
        ```bash
        python create-jsons.py -n "Hybrid User Interfaces" -d "Past, Present, and Future of Complementary Cross-Device Interaction in Mixed Reality" -a "Sebastian Hubenschmid, Marc Satkowski, Johannes Zagermann, Julián Méndez, Niklas Elmqvist, Steven Feiner, Tiare Feuchtner, Jens Emil Grønbæk, Benjamin Lee, Dieter Schmalstieg, Raimund Dachselt, Harald Reiterer" -g "https://github.com/imldresden/huis"
        ```
   3. The script prints out warnings for empty fields from the `includeProp` dictionary. You may use this to enforce value combinations (e.g. "at least one column from group A and one from group B"), or to identify edge cases. 
3. Note that the "topView" entry of `survey-config.json` must be updated to include orcids and further details about citation (see existing versions in the repository).  
4. Build the website as explained in [Running the Webpage](#running-the-webpage) to see the created entries. 

### To manually add papers 

After the 10.12.2025 cut off date, papers should be added by editing the [src/data/survey-data.json](src/data/survey-data.json), under the `"data"` tag. You can use this template: 
```json
"data": [  // array of paper objects
    {
        "Name"   : "[Poster] Visualization of solar radiation data in augmented reality",
        "Year"   : "2014",
        "Bibtex" : "'@INPROCEEDINGS{6948437,\n  author={Beatriz Carmo, Maria and Cl\u00e1udio, ....",
        "DOI"    : "10.1109/ISMAR.2014.6948437",
        "Authors": [
            "M. Beatriz Carmo; A. P. Cl\u00e1udio; A. Ferreira; A. P. Afonso; ...."
        ],
        "source": "handpicked",
    },
]
```
We welcome such updates via pull requests (which can be generated using the website itself, too)!

## Ackwnowledgements: 
The website is produced using [this survey tool](https://github.com/imldresden/survey-tool). It is a fork of the [Indy Survey Tool](https://github.com/VisDunneRight/Indy-Survey-Tool) from [Khoury Vis Lab](https://github.com/VisDunneRight) that differs in style and responsive behavior, which is why it's hosted separately. Big props to them for their initiative!  
