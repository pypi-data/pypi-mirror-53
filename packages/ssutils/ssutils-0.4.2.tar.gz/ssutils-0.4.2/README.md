# ssutils
collection of useful python functions


## Screenwriter

Use Screenwriter to prefix screen prints

**Examples:**

### 1 - Default prefix ###

```python
from ssutils import Screenwriter

sw = Screenwriter ()
sw.echo ('my output')
```
```
Output:
2019-07-26-11:16:04 my output
```

### 2 - Date Time parts in prefix ###

```python
from ssutils import Screenwriter

sw = Screenwriter ('%Y-%m-%d %H:%M:%S.%f ')
sw.echo ('my output')
```
```
Output:
2019-07-26 11:16:04 my output
```
 
### 3 - Error, Warning & Info standard prefixes ###

```python
from ssutils import Screenwriter

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
By default, log strings are trimmed to 1000 chars.
You can change this setting:
```python
from ssutils import Screenwriter
	
sw = Screenwriter ()
sw.set_maxlen (80) #Set maximum length to 80
```

For format options, see http://strftime.org/

## Sfdc

Use Sfdc to Query SFDC.

**Examples:**

### 1 - List Objects ###

```python

from ssutils import Sfdc

sf = Sfdc('userid', 'password', 'token', False) # last Param turns off verbose
sf.connect ()
sf.load_metadata ()
for apin in sf.object_labels.keys():
        print ("API Name [" + apin + "], Label [" + sf.object_labels[apin] + "]")
for apin in sf.standard_object_names:
        print ("Standard Object [" + apin + "]")
for apin in sf.custom_object_names:
        print ("Custom Object [" + apin + "]")
for apin in sf.custom_setting_names:
        print ("Custom Setting [" + apin + "]")

```

### 2 - Describe Objects ###

```python
from ssutils import Sfdc
sf = Sfdc('userid', 'password', 'token')
sf.connect ()
sf.load_metadata ()

def print_line (a, b, c, d, e):
        s = '{:7}'.format(a) + '{:50}'.format(b)
	s += '{:20}'.format(c) + '{:20}'.format(d) + e
        print (s)

print_line ('Seq', 'API Name', 'Type', 'Length', 'Label')
print_line ('---', '--------', '----', '------', '-----')
fn = 1
for fld in sf.describe_object ('Contact'):
	pfx = "#" + str(fn).ljust(3) + " - "
        print_line (pfx, fld['name'], fld['type'], str(fld['length']), fld['label'])
        fn += 1

```

### 3 - Forex Rate Conversions ###

```python
from ssutils import Sfdc
sf = Sfdc('userid', 'password', 'token')
sf.connect ()

sf.load_fx_rates ()
print (sf.get_amount_in_USD (999, 'EUR'))
```

### 4 - Querying from a table based on passed filters ###

```python
from ssutils import Sfdc
sf = Sfdc('userid', 'password', 'token')
sf.connect ()

tcols = ['Id', 'Account.Name']
conds = []
conds.append ("CloseDate >= " + str(date.today() + timedelta(days=-7)))
conds.append ("CloseDate <= " + str(date.today()))
conds.append ("StageName IN ('7. Closed Won')")
sf.load_data ('Opportunity', tcols, conds)

for rec in sf.table_data['Opportunity']:
        print (rec)
```

### 5 - Querying from a table with matching values (JOIN) in another table ###

In the example below, the variable jcond is a 3 member array depicting a JOIN criteria
* 1st Value is the column that needs to be Joined
* 2nd Value is the Table to join with
* 3rd Value is the Column in the Join table to match against

```python
from ssutils import Sfdc
sf = Sfdc('userid', 'password', 'token')
sf.connect ()

tcols = ['Id', 'Product2Id', 'TotalPrice', 'OpportunityId', 'CurrencyIsoCode']
conds = ["TotalPrice > 0"]
jcond = ['OpportunityId', 'Opportunity', 'Id']
sf.load_data ('OpportunityLineItem', tcols, conds, jcond)
```


## Date

Use Date to do some calculations on Dates

**Examples:**

### 1 - Get Financial Quarter, Month from Date ###

```python
from ssutils import Date

sd = Date()
print ('Quarter = '         + sd.get_quarter()) # Use current date
print ('Quarter = '         + sd.get_quarter('2019-04-15')) #Use Specified date

print ('Month Full = '      + sd.get_month())
print ('Month Short = '     + sd.get_mon())
print ('WeekNumber = '      + str(sd.get_week_number()))
print ('Year WeekNumber = ' + sd.get_year_week_number())
```
```
Output (when run in September 2019):
Quarter = Q3
Quarter = Q2
Month Full = September
Month Short = Sep
WeekNumber = 37
Year WeekNumber = 2019/37
```

### 2 - Get Financial Year Bounds from Date ###

```python

from ssutils import Date

sd = Date()
print ('Finacial Year Start = ' + sd.get_year_start ('2018-04-15'))
print ('Finacial Year End = '   + sd.get_year_end   ('2018-04-15'))
print ('Finacial Year Start = ' + sd.get_year_start ())
print ('Finacial Year End = '   + sd.get_year_end   ())
```
```
Output (when run in 2019):
Finacial Year Start = 2018-01-01
Finacial Year End = 2018-12-31
Finacial Year Start = 2019-01-01
Finacial Year End = 2019-12-31

```
