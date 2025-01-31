# Ind(ier) Survey Tool<!-- omit from toc -->

This repository forks the [Indy Survey Tool](https://github.com/VisDunneRight/Indy-Survey-Tool) and introduces a number of changes for web responsiveness and flexibility of the survey dataset format. Since the overall style is different than that of the original, we host it separately. Big props to the folks at the [Khoury Vis Lab](https://github.com/VisDunneRight) for their initiative. 

## Table of Contents<!-- omit from toc -->

- [Running the Webpage](#running-the-webpage)
- [Uploading Survey Papers](#uploading-survey-papers)
  - [Upload in Bulk](#upload-in-bulk)
  - [Manually Upload Paper](#manually-upload-paper)
  - [Adding a New Paper Categorization](#adding-a-new-paper-categorization)
- [Configuring the Webpage](#configuring-the-webpage)
  - [Overview of survey-config.json](#overview-of-survey-configjson)
  - [Modifying the Paper Detail View](#modifying-the-paper-detail-view)
  - [Modifying the Title \& Top Panel Information](#modifying-the-title--top-panel-information)

## Running the Webpage

1. `npm install` installs all the libraries you need to get the app running using the list from `package.json`.
2. `npm run build` updates and exports `index.html`, and the files in `dist/assets` for a static website. 
3. `npm run dev` the site locally (see link to localhost) in development mode (updates to src files reload the site).

## Uploading Survey Papers

The easiest method of uploading survey papers in bulk is using our CSV converter, but it is also possible to add papers individually.

### Upload in Bulk

1. Create an export of your corpus: 
   1. Create an export from your library manager (e.g. Zotero, Airtable, Notion)
   2. Save the file to the `src/data` directory with the name [Survey-Info.csv](Survey-Info.csv).
   3. Add your taxonomy columns as headers and values as either lists of strings (comma separated), or marks ("x") for values that apply. 
   4. `Name`, `Year`, `Authors` (comma separated), `DOI`, and `Bibtex` are required. 
2. Create the config and data json files: 
   1. Modify the dictionaries `includeProp`, `categories`, and `groups` in `src/data/create-jsons.py` to match your taxonomy columns. This depends on your columns from the previous step:
      1. If the column name matches an entry in `includeProp`, it will look for values directly (as list of comma separated strings)
      2. If the column name is not in `includeProp`, it will look for `x` and create lists based on the headers using the `categories` dictionary.
      3. Finally, the `groups` dictionary specifies the grouping of filters in the website as dictionary values, and thus the keys should match the keys of `includeProp`.
   2. Run the script to generate [survey-data.json](src/data/survey-data.json) and [survey-config.json](src/data/survey-config.json) --- WARNING: The script deletes the existing files---if entries have been manually added to these files, they will be lost. 
        ```bash
        python3 create-jsons.py
        ```
   3. The script prints out warnings for empty fields from the `includeProp` dictionary. You may use this to enforce value combinations (e.g. "at least one column from group A and one from group B"), or to identify edge cases. 
3. Build the website as explained in [Running the Webpage](#running-the-webpage) to see the created entries. 

### Manually Upload Paper

To add papers one-by-one, open [src/data/survey-data.json](src/data/survey-data.json). Then, add a new paper object to the list under the `"data"` tag using the template below as a guide. Note that the `"Name"`, `"Year"`, `"Authors"`, `"DOI"`, and `"Bibtex"` tags are required, but more can be added.
```json
"data": [  // array of paper objects
    {
        "Name"   : "[Poster] Visualization of solar radiation data in augmented reality",
        "Year"   : "2014",
        "Bibtex" : "'@INPROCEEDINGS{6948437,\n  author={Beatriz Carmo, Maria and Cl\u00e1udio, ....",
        "DOI"    : "10.1109/ISMAR.2014.6948437",
        "Authors": [
            "M. Beatriz Carmo; A. P. Cl\u00e1udio; A. Ferreira; A. P. Afonso; ...."
        ]
    },
]
```

### Adding a New Paper Categorization

If your survey papers are categorized by some tag, `<NEW_TAG>`, you should follow these steps to ensure it is displayed properly on the webpage:

1. Open [src/data/survey-data.json](src/data/survey-data.json).
2. Under `"meta"`, add a new object defining the properties of this tag:
    ```json
        {
            "name": "NEW_TAG",
            "type": "MultiSelect"  // categorization type: String or MultiSelect
        },
    ```
    Note that the type of the tag affects what a user of your webpage sees when they go to add a new paper using the "Add Entry" button at the top right. `String` allows the user to enter a string, whereas `MultiSelect` gives the user a dropdown of options to choose from. The options will be all the values in current papers.
3. Add the same information to the `includeProp` dictionary at the top of [convertCSVtoJson.py](convertCSVtoJson.py) if you intend to use the [bulk paper import](#upload-in-bulk) method.

## Configuring the Webpage

Many aspects of the webpage, including colors, filter groups, tags on papers, and displayed icons are fully customizable.

### Overview of survey-config.json

[src/data/survey-config.json](src/data/survey-config.json) contains most of the configuration options for the webpage. It is structured as follows:

```json
{
    "filterBy"   : [],  // defines custom categories that can be used to filter the papers
    "detailView" : [],  // information displayed when a paper is clicked by the user
    "summaryView": [],  // information displayed in the paper view center panel
    "topView"    : []   // information displayed in the top panel of the webpage
}
```

### Modifying the Paper Detail View

To change what is displayed when a user clicks on a specific paper, open [src/data/survey-config.json](src/data/survey-config.json) and navigate to the `"detailView"` tag. Under `"show"`, a list of paper properties to be displayed when the paper is clicked can be provided. By default, the following properties are shown:

* Name
* Authors
* Year
* DOI
* BibTeX

### Modifying the Title & Top Panel Information

Open [src/data/survey-config.json](src/data/survey-config.json) and navigate to the `"topView"` tag. Here, important information displayed in the top panel can be modified:

* `"title"`: title of the survey displayed at the top of the webpage
* `"description"`: survey description
* `"authors"`: survey authors
* `"addEntry"`:
  * `"description"`: text displayed at the top of the Add Entry window
  * `"github"`: link to the survey GitHub repository, where users may open a GitHub issue to request that a paper be added

These strings can all be provided directly when executing the `create-jsons.py` script. 
