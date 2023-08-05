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
