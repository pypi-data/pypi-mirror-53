# pygrouplib
Library for dividing entities into groups based on numeric or text value


## Quick start
```python
from pygrouplib import NumericGrouper, TextGrouper

# Example data list
employees = []
employees.append({'name':'John','title':'Cardiologist','age':46})
employees.append({'name':'Ryan','title':'Cardiology','age':34})
employees.append({'name':'Kate','title':'Child Cardiologist', 'age':56})
employees.append({'name':'Anna','title':'Neurology', 'age':33})
employees.append({'name':'Mike','title':'Neurologist', 'age':38})

# Group by title, ignoring "Child" and allowing 1 different character for each 5 characters in title.
tg = TextGrouper()
groups = tg.group(employees, key=lambda x:x['title'], chars_per_error=5, ignore_list=['Child'])
print(*groups, sep='\n')

''' 
[{'name': 'John', 'title': 'Cardiologist', 'age': 46}, {'name': 'Ryan', 'title': 'Cardiology', 'age': 34}, {'name': 'Kate', 'title': 'Child Cardiologist', 'age': 56}]
[{'name': 'Mike', 'title': 'Neurologist', 'age': 38}, {'name': 'Anna', 'title': 'Neurology', 'age': 33}]
'''

# Group by age into 3 subgroups
ng = NumericGrouper()
groups = ng.group(employees, key=lambda x:x['age'], groups=3)
print(*groups, sep="\n")

'''
[{'name': 'Anna', 'title': 'Neurology', 'age': 33}, {'name': 'Ryan', 'title': 'Cardiology', 'age': 34}, {'name': 'Mike', 'title': 'Neurologist', 'age': 38}]
[{'name': 'John', 'title': 'Cardiologist', 'age': 46}]
[{'name': 'Kate', 'title': 'Child Cardiologist', 'age': 56}]
'''


```


## Installation
Pygrouplib is published through PyPi so you can install it with `easy_install` or `pip`. The package name is `pygrouplib`, and the same package works on Python 2 and Python 3. Make sure you use the right version of `pip` or `easy_install` for your Python version (these may be named `pip3` and `easy_install3` respectively if you’re using Python 3).
```bash
$ easy_install pygrouplib
```
```
$ pip install pygrouplib
```


## Documentation


### NumericGrouper
#### group()
- Groups elements into soubgroups based on numeric value.
- Arguments:
  - **entities** - List of entities to be divided into groups.
  - **groups** - Number of resulting subgroups. The default value is None, in which case it is calculated based on provided values from entities.
  - **key** Function of one argument that is used to extract comparison key from each element in iterable (for example, `key=lambda x: x['value']`). The default value is None (compare the elements directly).
- Returns a list of entities grouped into lists.

### TextGrouper
#### group()
- Groups elements into soubgroups based on text value. Similarity is calculated using Levenshtein algorithm.
- Arguments:
  - **entities** - List of elements to be divided into groups.
  - **similarity_limit** - Maximum Levenshtein distance between words to be consiedered as similar. The default value is calculated as 1 + (1 for each chars_per_error characters).
  - **chars_per_error** - Number of characters per 1 error allowed. Levenshtein distance is considered as a number of errors. The default value is 8 (1 error is allowed for each 8 characters). 
  - **ignore_list** - List of patterns to ignore when calculating text similarity. For example, with `ignore_list=['\\d']`, *'word123'* and *'123word45'* are considered equal.
  - **key** - Function of one argument that is used to extract comparison key from each element in iterable (for example, `key=str.lower`). The default value is None (compare the elements directly).
- Returns a list of entities grouped into lists.
#### levenshtein_distance()
- Calculates Leveshtein distance between two strings. Levenshtein distance between two words is the minimum number of single-character edits (i.e. insertions, deletions, or substitutions) required to change one word into the other. Comparison is case sensitive.
- Arguments:
  - **s1**, **s2** - Strings to be compared. Leading and trailing spaces are ignored.
  - **ignore_list** - List of patterns to be ignored when comparing strings. For example, with `ignore_list=['\\d']`, distance between *'word123'* and *'123word45'* is 0. Default value is empty list.
