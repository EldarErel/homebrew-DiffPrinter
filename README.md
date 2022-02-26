# DiffPrinter
CLI tool to print the difference between two YAML or JSON files

## Pre-requirements:

homebrew installed

## Installation process:

1. Create a tap to connect the repo: `brew tap eldarerel/diffprinter`

2. Install the script: `brew install diffprinter`

 NOTE: The installation process may take a few minutes.

## For further help please type `pdiff --help` in the terminal.
```bash
Usage: pdiff [OPTIONS] PATH_TO_BASE_FILE PATH_TO_OTHER_FILE

 Print the difference between two items (JSON or YAML files):

 1. keys that are missing from the base item compared to the other item.

 2. keys that appear in the base item and not in the other item.

 3. the difference in values for keys that appear in both items.

# Options:
-m, --missing BOOLEAN           If set to true, prints only missing keys. (1)
                                                      [default: False]
-ig, --ignore_order BOOLEAN  If set to true, ignores the order of values for
                                                      list items (a Set).  [default: True]
-t, --type [json|yaml]                 The type of items you want to compare.
                                                      [default: json]
--help                                           Show this message and exit.
```
## Examples:

`pdiff --missing=True --type=yaml base_file.yaml other_file.yaml`
```bash
the missing keys are:
    "['field']['in']['field']['w']" 
    "['field']['in']['field']['z']"
```

`pdiff -type yaml base_file.yaml other_file.yaml`
```bash
the missing keys are:
    "['field']['in']['field']['w']" 
    "['field']['in']['field']['z']"
the extra keys are: 
    "['field']['subfield']" 
    "['field']['subfield']"         
    "['field2']['sub2']"                
 the diffrence in values between the files are:
    "['field3']['sub']":         
        'other_value': 1         
        'base_value': 2
    ""['field3']['sub2']":        
        'other_value': 'another example'         
        'base_value': 'of the same thing'
 ```


`pdiff -type yamlbase_file.yaml other_file.yaml`
```bash
Files are equal
```
