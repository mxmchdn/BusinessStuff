# SAP-Table

## Modules
You need for run this file, xlwt (for xls files), PyQt5 (for a user interface) and requests (for GET requests)

  [xlwt](https://pypi.org/project/xlwt/) -- `pip install xlwt`
  
  [requests](https://pypi.org/project/requests/) -- `pip install requests`
  
  [PyQt5](https://pypi.org/project/PyQt5/) -- `pip install PyQt5`

## Files

Application.py script works on the user interface and the installation of all module.

Argument 1: the path for scan a directory <str>

Argument 2: the splitter in filename <str>

Argument 3: the position of the name in filename <int>

Argument 4: the splitter in the file <str>

Argument 5: if you want unicode (True = *2, False = *1) <bool>

Argument 6: the type (extension) of file to scan (.txt or .csv) <str>

Argument 7: the default value if length equal to zero <int>
  
Rappatriement_Longueur.py script works on arguments and the manipulation of them.

## Functions
1) Save_directory(<str: path>, <str: Name splitter>, <int: Name position>, <str: file type>) => Scan a directory fot find file with the good extension and the good pattern: return a tuple list of name and path

2) Fields_Len_Extraction(<tuple list: previous function output>, <str: delimiter>) => Scan each file and for study fields and len: return a tuple list of name and tuple list of field and length 

3) GET_requests(<tuple list: first function output>) => For all Files name, search his HTML page with a GET requests: return HTML files
  
4) Fields_Len_HTML_Extractions(<tuple list: first function output>) => Run on all get requests files for extract field and len of each table: return a tuple list of name and tuple list of field and length
  
5) MergeTwoList(<tuple list: 2nd function output>, <tuple list: 4th function output>) => Merge two list with keep just the max size and field present in the first argument: return the final tuple list of name and tuple list of field and size

6) SaveAll(<tuple list: 5th function output>, <bool: is_unicode>, <int: default length>, <str: extension of files scan>) => Save all data in an xls file, if is_unicode = true, we multiplicate by 2 all length, and if length = 0, we replace it by a default value
4) 
