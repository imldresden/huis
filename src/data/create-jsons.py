import csv
import json
import argparse
import logging

# properties without a filter or view
excludeProp = ["Name", "Authors", "Year", "DOI", "Bibtex", "source"]

optionals = ["Secondary Contribution"]

# properties that will be shown in the website
includeProp = {
  # fixed
  "Name":"String",
  "Authors": "MultiSelect",
  "Bibtex": "String",
  "source": "String",
  "DOI": "String",
  "source": "String",
  "Year": "Timeline",
  
  # custom categories
  "2D Devices": "MultiSelect",
  "MR Devices": "MultiSelect",
  "Configuration": "MultiSelect",
  "Temporal": "MultiSelect",
  "Relationship": "MultiSelect",
  "Range": "MultiSelect",
  "Device Dependency": "MultiSelect",
  "Space": "MultiSelect",
  "Interaction Dynamics": "MultiSelect",
  "Anchoring": "MultiSelect",

  "Use Case": "MultiSelect", 
  "Main Contribution": "MultiSelect",
  "Secondary Contribution": "MultiSelect",
  "Evaluation": "MultiSelect",

  "Terminology": "MultiSelect",
  "Edge Case": "MultiSelect",
}

# properties that will be read from the csv, indexed to their supergroups
categories = {
  "AR OST HWD": "MR Devices",
  "AR VST HWD": "MR Devices",
  "Handheld AR (Smartphone)": "MR Devices",
  "Handheld AR (Tablet)": "MR Devices",
  "Spatial AR (projector based)": "MR Devices",
  "Stereoscopic Projection": "MR Devices",
  "CAVE": "MR Devices",
  "VR HWD": "MR Devices",

  "Smartwatch": "2D Devices",
  "Smartphone": "2D Devices",
  "Tablet": "2D Devices",
  "Laptop": "2D Devices",
  "Desktop": "2D Devices",
  "Projection": "2D Devices",
  "Large Display": "2D Devices",
  "Tabletop": "2D Devices",

  "Symmetric": "Configuration",
  "Asymmetric": "Configuration",
  "Remote Control": "Configuration",
  "Dynamic Lens": "Configuration",
  "Augmented Display": "Configuration",
  "VESAD": "Configuration",
  "Logical Distribution": "Configuration",
  "Migratory Interface": "Configuration",

  "Parallel": "Temporal", 
  "Serial": "Temporal", 
  "Exclusive": "Temporal", 
          
  "Single User": "Relationship",
  "Multi-user - Indvidual Component": "Relationship",
  "Multi-user - Shared Component": "Relationship",
          
  "Near": "Range", 
  "Personal": "Range", 
  "Social": "Range", 
  "Public": "Range",
  
  "Flexible": "Device Dependency", 
  "Semi-Fixed": "Device Dependency", 
  "Fixed": "Device Dependency",
          
  "Co-Located": "Space", 
  "Remote": "Space",
          
  "Unidirectional (2D-centric)": "Interaction Dynamics",
  "Unidirectional (MR-centric)": "Interaction Dynamics",
  "Bidirectional": "Interaction Dynamics",

  "Component-coupled": "Anchoring", 
  "Free": "Anchoring", 
  "Dynamic": "Anchoring",

  "Term: Hybrid UI": "Terminology",
  "Term: Hybrid <other>": "Terminology",
  "Term: Cross-Device": "Terminology",
  "Term: Cross-Reality": "Terminology",
  "Term: Multi-Device": "Terminology",
  "Term: Augmented Display": "Terminology",
  "Term: Transitional": "Terminology",
  "Undefined": "Terminology",
  "Other Terms": "Terminology",

  "Empirical": "Main Contribution",
  "Artifact": "Main Contribution",
  "Method": "Main Contribution",
  "Theory": "Main Contribution",
  "Dataset": "Main Contribution",
  "Survey": "Main Contribution",
  "Opinion": "Main Contribution",

  "Empirical (-)": "Secondary Contribution",
  "Artifact (-)": "Secondary Contribution",
  "Method (-)": "Secondary Contribution",
  "Theory (-)": "Secondary Contribution",
  "Dataset (-)": "Secondary Contribution",
  "Survey (-)": "Secondary Contribution",
  "Opinion (-)": "Secondary Contribution",

  "Informative": "Evaluation",
  "Demonstration": "Evaluation",
  "Technical Evaluation": "Evaluation",
  "Usage": "Evaluation",
  "Heuristic": "Evaluation",
  "No Evaluation": "Evaluation", 

  "Development/Authoring": "Use Case", 
  "Gaming": "Use Case", 
  "DataVis/Data Analysis": "Use Case", 
  "SciVis": "Use Case", 
  "Medical": "Use Case", 
  "Productivity": "Use Case", 
  "Collaboration": "Use Case", 
  "Entertainment": "Use Case", 
  "3D Object Manipulation": "Use Case", 
  "3D Design/Sketching": "Use Case", 
  "Text Entry / Annotations": "Use Case", 
  "Study": "Use Case", 
  "Other / None": "Use Case"
}

groups = { 
  "2D Devices": "Technology",
  "MR Devices": "Technology",

  "Configuration": "Taxonomy",
  "Temporal": "Taxonomy",
  "Relationship": "Taxonomy",
  "Range": "Taxonomy",
  "Device Dependency": "Taxonomy",
  "Space": "Taxonomy",
  "Interaction Dynamics": "Taxonomy",
  "Anchoring": "Taxonomy",

  "Main Contribution": "Theory and Contribution", 
  "Secondary Contribution": "Theory and Contribution", 
  "Use Case": "Theory and Contribution", 
  "Evaluation": "Theory and Contribution", 

  "Terminology": "Meta", 
  "Edge Case": "Meta"
}

def get_arguments():
    """ Get parsed CLI arguments """
    parser = argparse.ArgumentParser(description='Python script for converting csv to JSON for Indy.'
                                                 'Generates a config and data file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input-file', type=str, default="Survey-Info.csv",
                        dest="filename", help='The files that gets parsed.')
    parser.add_argument('-o','--only-data', action='store_true', default=False,
                        dest="onlydata", help='generate only the data file')
    parser.add_argument('-n','--name', type=str, 
                        default="Example Title",
                        dest="surveyname", help='sets the website title')
    parser.add_argument('-d','--desc', type=str, 
                        default="Example Description",
                        dest="surveydesc", help='sets the website description')
    parser.add_argument('-a','--authors', type=str, 
                        default="<anonymized for submission>",
                        dest="surveyauthors", help='sets the website authors')
    parser.add_argument('-g','--github', type=str, 
                        default="<anonymized for submission>",
                        dest="github", help='sets the website link to Github')

    return parser.parse_args()

class CustomFormatter(logging.Formatter):    
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def main():
  args = get_arguments()
  
  logger = logging.getLogger(__name__)
  
  stdout_handler = logging.StreamHandler()
  stdout_handler.setFormatter(CustomFormatter('%(levelname)8s | %(message)s'))
  logger.addHandler(stdout_handler)

  with open(args.filename, encoding='utf-8-sig') as csvfile:
    spamreader = csv.reader(csvfile)
    jsonfile = {"meta":[], "data":[]}
    configfile = {"filterBy":[], "filterBy":[], "detailView":{
        "view" : "normal",
        "show":[] #Add properties that you want to view on summary view
      }, 
      "summaryView": {
        "view": "text",
        "showImg": True,
        "show":[] #Add properties that you want to view on summary view
      },
      "topView":{
        "title":args.surveyname,
        "description":args.surveydesc,
        "authors":args.surveyauthors,
        "addEntry": {
          "description":[
            "If you know a peer-reviewed published work that presents a contribution missing in our browser, please submit an entry!", 
            "Filling out the form below will create a json entry that can be added to an issue in our Github repository."],
          "github":args.github
        }
      }
    }

    header = []
    uniques = set()

    # get header information
    for row in spamreader:
      for name in row:
        header.append(name)
        if name in includeProp:
          jsonfile["meta"].append({'name': name, "type":includeProp[name]})
          if (includeProp[name] == 'MultiSelect' or includeProp[name] == 'String') and name not in excludeProp :
            configfile["filterBy"].append(name)
          if name not in excludeProp:
            configfile["detailView"]["show"].append(name)
        elif name in categories: 
          catname = categories[name]
          nametype = includeProp[catname]
          
          if catname not in uniques: 
            uniques.add(catname)
            jsonfile["meta"].append({'name': catname, "type": nametype})
            if (nametype == 'MultiSelect' or nametype == 'String') and catname not in excludeProp :
              configfile["filterBy"].append(catname)
            if catname not in excludeProp:
              configfile["detailView"]["show"].append(catname)
      break

    propStructure = {}
    for prop in includeProp:
      propStructure[prop] = {"name":prop, "values":set()}

    # reads every paper 
    for row in spamreader:
      entry = {}
      for index, prop in enumerate(row):

        # read and collect values with "x" in them 
        if header[index] in categories:  
          catname = categories[header[index]]
          nametype = includeProp[catname]

          if catname not in entry: 
            entry[catname] = set()
          
          if (prop != ""):
            entry[catname].add(header[index])
                
          for doc in entry[catname]:
            propStructure[catname]['values'].add(doc)
        
        # read as lists of strings (comma separated)
        elif header[index] in includeProp:
            catname = header[index]

            # handle edge cases
            if (catname == "Edge Case"): 
              if (prop == "x"): 
                entry[catname] = ["Yes"]
              elif (prop == ""):       
                entry[catname] = ["No"]
            
            else: 
              if includeProp[catname] == "MultiSelect":
                entry[catname] = [x.strip() for x in prop.split(",")]
              else:
                entry[catname] = prop.strip()
              
            if includeProp[catname] == "MultiSelect":
              propList = entry[catname]
              for doc in propList:
                propStructure[catname]['values'].add(doc)

        
        
      for k in entry: 
        if isinstance(entry[k], set):
          entry[k] = list(entry[k])

      for k in includeProp: 
        if (not k in entry or (len(entry[k]) == 0)) and (not k in optionals):
          logger.warning(
            "Prop: \"" + k + "\" empty for: \"" + entry["Name"] + "\". " + 
            "Check for duplicate headings, or this may be an edge case."
          )
      jsonfile["data"].append(entry)
    
    dataObject = json.dumps(jsonfile, indent=4)
    
    # writing to survey-data.json
    with open("survey-data.json", "w") as outfile:
        outfile.write(dataObject)
    
    filterGroups = {}
    if args.onlydata == False:
      for i in range(len(configfile["filterBy"])):
        name = configfile["filterBy"][i]
        propStructure[name]['values'] = list(propStructure[name]['values'] )

        
        if not groups[name] in filterGroups: 
          filterGroups[groups[name]] = { "groupName": groups[name], "categories": [] }
        filterGroups[groups[name]]["categories"].append(propStructure[name])

      configfile["filterBy"] = [x for x in filterGroups.values()]

      with open("survey-config.json", "w") as outfile:
          configObject= json.dumps(configfile, indent=4)
          outfile.write(configObject)

if __name__ == '__main__':
  main()