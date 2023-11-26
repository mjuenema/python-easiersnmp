# easiersnmp

*easiersnmp* is a wrapper around [*easysnmp*](https://github.com/kamakazikamikaze/easysnmp) to make it even easier to use. 
It also includes an alternative implementation of [*easysnmptable*](https://github.com/wolcomm/easysnmptable).

## Python types

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

*easiersnmp* changes this behaviour by converting ``SNMPVariable.value`` into the correct data type.

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

The table below shows how values are converted.

| ``SNMPVariable.snmp_type`` | Python type |
|---|---|
| ``INTEGER32`` | ``int`` |
| ``INTEGER`` | ``int`` |
| ``UNSIGNED32`` | ``int`` |
| ``GAUGE`` | ``int`` |
| ``IPADDR`` | ``ipaddress.IPv4Address``/``ipaddress.IPv6Address`` |
| ``OCTETSTR`` | (read note below) |
| ``TICKS`` | ``datetime.timedelta`` |
| ``OPAQUE`` | |
| ``OBJECTID`` | |
| ``NETADDR`` | ``ipaddress.IPv4Address``/``ipaddress.IPv6Address`` |
| ``COUNTER64`` | ``int`` |
| ``NULL`` | ``None`` |
| ``BITS`` | ``int`` |
| ``UINTEGER`` | ``int`` |

The ``OCTETSTR`` SNMP type is commonly used as a container for values that cannot be represented in any other
SNMP type. It is impossible to know the correct interpretation of an ``OCTETSTR`` without parsing the relevant
SNMP MIB. 

## Acknowledgements

I'd like to acknowledge the following projects.

* The [EasySNMP](https://pypi.org/project/easysnmp/) project of which EasierSNMP is just a thin wrapper.
* The [EasySNMP Table](https://pypi.org/project/easysnmptable/) project which inspired my own implementation of a ``table()`` method.
