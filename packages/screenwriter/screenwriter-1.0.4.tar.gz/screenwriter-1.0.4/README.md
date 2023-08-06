# screenwriter
Python Library for writing progress texts, echo messages, warnings and errors to standard output


**Examples:**

### 1 - Default prefix ###

```python
from screenwriter import Screenwriter

sw = Screenwriter ()
sw.echo ('my output')
```
```
Output:
2019-07-26-11:16:04 my output
```

### 2 - Date Time parts in prefix ###

```python
from screenwriter import Screenwriter

sw = Screenwriter ('%Y-%m-%d %H:%M:%S.%f ')
sw.echo ('my output')
```
```
Output:
2019-07-26 11:16:04 my output
```
 
### 3 - Error, Warning & Info standard prefixes ###

```python
from screenwriter import Screenwriter

sw = Screenwriter ()
sw.error ('an error message')
sw.warn  ('a warming message')
sw.info  ('an informational message')
```
```
Output:
2019-07-29-11:39:00 ERROR: an error message
2019-07-29-11:39:00 WARN:  a warming message
2019-07-29-11:39:00 INFO:  an informational message
```

### 4 - Trimming content length  ###
By default, log strings are trimmed to 120 chars.
You can change this setting:
```python
from screenwriter import Screenwriter
	
sw = Screenwriter ()
sw.set_maxlen (80) #Set maximum length to 80
```

### 5 - Dynamically toggele output ###

You can toggle the output between ON and OFF. 

```python
from screenwriter import Screenwriter

sw = Screenwriter ()
sw.echo ('print this line')
sw.set_verbose (False)
sw.echo ('do not print this line')
sw.set_verbose (True)
sw.echo ('print this line')
```
```
Output:
2019-10-05-20:09:10 print this line
2019-10-05-20:09:10 print this line
```


For format options, see http://strftime.org/

