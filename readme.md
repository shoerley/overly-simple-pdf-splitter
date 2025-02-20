# Overly Simple PDF Splitter (OSPS)
20/02/2025

This tool has one single goal : allow splitting PDF files using parameters that are in a CSV file. No fancy stuff, and no extra checks.

## Usage

python pdf_splitter.py input_file split_config <output_folder>

**input_file** : path to the input PDF to be split

**split_config**: CSV file with splitting parameters (see “CSV file”)

**output_folder**:output folder where split files will be written.

## CSV File

CSV file should have three columns : file name, page start, page end. Page start and end are integers, and are included.

Example :

````csv
    couverture, 1, 1
    présentation de l'établissement, 4, 7
    états financiers, 115, 245
````

Will produde three files. The first one will have one single page and will be named "couverture.pdf"

## Dependancies

The script relies on PyPDF2 for PDF operations. Here is a list of all dependancies : 
- PyPDF2
- csv
- sys
- random
- string
- os

## Behavior to know

Please be warned :
The script will not overwrite any file. If a file with same name exists, the script will stop

You can provide an output folder. If you do so, it will be created if it does not exist. Otherwise, it will simply be used. If you don't provide an output folder, a folder will be created (in the working directory) with a random and (hopefully) unique name.


## Example

You can run the script using the resources in the `res``folder :

```
    python pdf_splitter.py ../res/document.pdf ../res/split_params.csv
```

This line will create an output folder (generated name) and create three files.


## Disclaimer

I am not responsible for any damage or data loss that this script could make. I used it with no issues to split several files without a GUI and found it wuite usefull and time saving. Hope you will find it usefull in some way. Improvements are welcome.