*easiersnmp* is a wrapper around [*easysnmp*](https://github.com/kamakazikamikaze/easysnmp) to make it even easier to use. 
It also includes an alternative implementation of [*easysnmptable*](https://github.com/wolcomm/easysnmptable).

While I really like *easysnmp*, it returns instances of ``SNMPVariable`` instead of of the basic Python data types. 
In addition the actual value (``SNMPVariable.value``) will always be a string, even if the underlying SNMP type is numeric.

SNMP GET in *easysnmp*
```python
import easysnmp
session = easysnmp.Session(hostname='localhost', community='public', version=2)
result = session.get('ifIndex.1')

# result is an instance of easysnmp.SNMPVariable
print(result.oid, result.oid_index, result.snmp_type, result.value)
# ifIndex 1 INTEGER 1

# The result.value is a string even though the snmp_type is INTEGER
print(type(result.value)
# str
```

*easiersnmp* changes this behaviour by converting ``SNMPVariable.value`` 

SNMP GET in *easiersnmp*
```python
import easiersnmp
session = easiersnmp.Session(hostname='localhost', community='public', version=2)
result = session.get('ifIndex.1')

# result is an instance of easiersnmp.SNMPVariable
print(result.oid, result.oid_index, result.snmp_type, result.value)
# ifIndex 1 INTEGER 1

# The result.value is an integer matching the snmp_type
print(type(result.value)
# int
```
