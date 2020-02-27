"""

"""

import easysnmp

# SNMPVariable
class SNMPVariable(easysnmp.SNMPVariable):
    pass

# Session API

class Session(easysnmp.Session):

    # Type conversion functions. These can be overridden
    # in derived classes if desired.
    #
    def integer32(self, value):
        return int(value)

    def integer(self, value):
        return int(value)

    def unsigned32(self, value):
        return int(value)

    def gauge(self, value):
        return int(value)

    def ipaddr(self, value):
        # https://tools.ietf.org/html/rfc4001
        # IPv4 and IPv6 only
        import ipaddress
                
        if len(value) == 4:
            return ipaddress.IPv4Address('.'.join(['%d' % ord(o) for o in value]))
        elif len(value) == 16:
            return ipaddress.IPv6Address(':'.join(['%02x' % ord(o) for o in value]))
        else:
            # raise ValueError?
            return value

    def octetstr(self, value):
        # TODO: Come up with some clever logic!
        return value

    def ticks(self, value):
        # TODO: convert to datetime.timedelta
        return int(value)

    def opaque(self, value):
        return value

    def objectid(self, value):
        return value

    def netaddr(self, value):
        # What is this type?
        return value

    def counter(self, value):
        return int(value)

    def null(self, value):
        # TODO: correct?
        return None

    def bits(self, value):
        # TODO: Convert into list of True/False?
        return value

    def uinteger(self, value):
        return int(value)

    def default(self, value):
        return value

    def _convert(self, variable):
        # variable.oid, 
        # variable.oid_index, 
        # variable.snmp_type, 
        # variable.value

        if variable.snmp_type == 'INTEGER32':
            variable.value = self.integer32(variable.value)
        elif variable.snmp_type == 'INTEGER':
            variable.value = self.integer(variable.value)
        elif variable.snmp_type == 'UNSIGNED32':
            variable.value = self.unsigned32(variable.value)
        elif variable.snmp_type == 'IPADDR':
            variable.value = self.ipaddr(variable.value)
        elif variable.snmp_type == 'OCTETSTR':
            variable.value = self.octetstr(variable.value)
        elif variable.snmp_type == 'TICKS':
            variable.value = self.ticks(variable.value)
        elif variable.snmp_type == 'OPAQUE':
            variable.value = self.opaque(variable.value)
        elif variable.snmp_type == 'OBJECTID':
            variable.value = self.objectid(variable.value)
        elif variable.snmp_type == 'NETADDR':
            variable.value = self.netaddr(variable.value)
        elif variable.snmp_type == 'COUNTER':
            variable.value = self.counter(variable.value)
        elif variable.snmp_type == 'NULL':
            variable.value = self.null(variable.value)
        elif variable.snmp_type == 'BITS':
            variable.value = self.bits(variable.value)
        elif variable.snmp_type == 'UINTEGER':
            variable.value = self.uinteger(variable.value)
        else:
            variable.value = self.value(variable.value)

        # Morph the class
        variable.__class__ == SNMPVariable
        return variable
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._convert(super().get(*args, **kwargs))


# Easy API
