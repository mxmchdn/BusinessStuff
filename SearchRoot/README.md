# RootSearch

## Principle
  Go back to the root of a file with its ID

## Python's modules use:
  [xlwt](https://pypi.org/project/xlwt/) -- `pip install xlwt`
  
## Input files:
  
  ### [With 2 files](https://github.com/mxmchdn/SearchRoot/blob/master/SearchRoot_TwoFiles.py):
   *  One file with id. Be careful about the separator, if there are many arguments in a line! (I use .csv files, so its ; separator)
   *  One file with some file informations like:
      ```
      - id
      - parentid
      - size
      - type
      - name
   Be careful about the separator, if there are many arguments in a line! (I use .csv files, so its ; separator)
     
  ### [With one file](https://github.com/mxmchdn/SearchRoot/blob/master/SearchRoot_OneFile.py):
   *  One file with some file informations like:
      ```
      - id
      - parentid
      - size
      - type
      - name 
   In this case I start with TB file's type.
   
   Be careful about the separator, if there are many arguments in a line! (I use .csv files, so its ; separator)
      
 ## Output file:
 All the output file is a .csv file
