
import easysnmp
import easysnmp.utils
import datetime
import string
import ipaddress
import collections


# SNMPVariable
class SNMPVariable(object):
    def __init__(self, v):
        assert isinstance(v, easysnmp.SNMPVariable)
        self.v = v

    def __repr__(self):
        return '<{0} value={1} (oid={2}, oid_index={3}, snmp_type={4}'.format(
                self.__class__.__name__, 
                self.value, 
                self.oid, 
                self.oid_index.encode('ascii', 'backslashreplace'),
                self.snmp_type)

    @property
    def oid(self):
        return self.v.oid

    @property
    def oid_index(self):
        return self.v.oid_index

    @property
    def snmp_type(self):
        return self.v.snmp_type

    @property
    def value(self):
        if self.snmp_type == 'INTEGER32':
            return int(self.v.value)
        elif self.snmp_type == 'INTEGER':
            return int(self.v.value)
        elif self.snmp_type == 'UNSIGNED32':
            return int(self.v.value)
        elif self.snmp_type == 'GAUGE':
            return int(self.v.value)
        elif self.snmp_type == 'IPADDR':
            return ipaddress.ip_address(self.v.value).exploded
        elif self.snmp_type == 'OCTETSTR':
            # Try to be clever here as we don't have access to the DISPLAY-HINT.
            if len(self.v.value) == 6:
                # MAC Address
                return ':'.join(['{:02x}'.format(ord(c)) for c in self.v.value])
            else:
                return self.v.value
        elif self.snmp_type == 'TICKS':
            return int(self.v.value)
        elif self.snmp_type == 'OPAQUE':
            return self.v.value
        elif self.snmp_type == 'OBJECTID':
            return self.v.value
        elif self.snmp_type == 'NETADDR':
            raise NotImplementedError(str(self))
            return self.ipaddress
        elif self.snmp_type == 'COUNTER':
            return int(self.v.value)
        elif self.snmp_type == 'NULL':
            return None
        elif self.snmp_type == 'BITS':
            return self.v.value
        elif self.snmp_type == 'UINTEGER':
            return int(self.v.value)
        else:
            return self.v.value


# Conversion functions
#
def value(v):
    if isinstance(v, SNMPVariable):
        return v.value
    else:
        return v

def valuedecorator(v):
    def wraper(v):
        return value(v)

@valuedecorator
def truthvalue(v):
    if v in (1,2):
        return v == 1
    else:
        raise ValueError('Not a valid TruthValue')

@valuedecorator
def ipaddr(v):
    return ipaddress.ip_address(v).exploded
netmask = ipaddr

@valuedecorator
def macaddress(v):
    if len(v) == 6:
        return ':'.join(['%02x' % (i) for i in v])
    else:
        raise ValueError('Not a valid MAC Address')
physaddress = macaddress

@valuedecorator
def displaystring(v, errors='replace'):
    return v.encode(encoding='ascii', errors=errors)


@valuedecorator
def hexstring(v):
    return ''.join(['{:02x}'.format(ord(c)) for c in s])


# Session API
#
class Session(easysnmp.Session):

  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _snmp(self, method, *args, **kwargs):
        v = method(*args, **kwargs)
        if isinstance(v, easysnmp.SNMPVariable):
            return SNMPVariable(v)
        elif isinstance(v, (easysnmp.variables.SNMPVariableList, list)):
            return [SNMPVariable( i) for i in v]
        else:
            raise TypeError('{} returned unknown type {}'.format(method, type(v)))
                    
    def get(self, *args, **kwargs):
        return self._snmp(super().get, *args, **kwargs)
    
    def get_bulk(self, *args, **kwargs):
        return self._snmp(super().get_bulk, *args, **kwargs)
    
    def bulkwalk(self, *args, **kwargs):
        return self._snmp(super().bulkwalk, *args, **kwargs)
    
    def walk(self, *args, **kwargs):
        return self._snmp(super().walk, *args, **kwargs)

    def set(self, *args, **kwargs):
        return super().set(*args, **kwargs) 
        raise NotImplementedError
    
    def set_multiple(self, *args, **kwargs):
        raise NotImplementedError
    
    def get_next(self, *args, **kwargs):
        raise NotImplementedError

    def bulktable(self, *args, **kwargs):
        table = collections.defaultdict(dict)
        for row in self._snmp(super().bulkwalk, *args, **kwargs):
            table[row.oid_index][row.oid] = row
        return table.values()

    def table(self, *args, **kwargs):
        table = collections.defaultdict(dict)
        for row in self._snmp(super().walk, *args, **kwargs):
            table[row.oid_index][row.oid] = row
        return table.values()
