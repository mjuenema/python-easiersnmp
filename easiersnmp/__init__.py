
import easysnmp
import datetime

# SNMPVariable
class SNMPVariable(object):
    def __init__(self, session, variable):
        """The interface of `easiersnmp.SNMPVariable` is different from
           `easysnmp.SNMPVariable`. It is not meant to be instantiated 
           directly by other modules than `easiersnmp`.
           
           :param session: Instance of `easiersnmp.Session` as it contains
                the conversion functions which may be overwritten by
                derived classes.
            :param variable: Instance of `easysnmp.SNMPVariable` whose 
                attributes will be extracted to populate this class.
           
        """
        
        
        # Copy `oid`, `oid_index` and `snmp_type`. 
        #
        self.oid = variable.oid
        self.oid_index = variable.oid_index
        self.snmp_type = variable.snmp_type
        
        
        # Convert value.
        #
        if self.snmp_type == 'INTEGER32':
            self.value = session.integer32(variable.value)
        elif self.snmp_type == 'INTEGER':
            self.value = session.integer(variable.value)
        elif self.snmp_type == 'UNSIGNED32':
            self.value = session.unsigned32(variable.value)
        elif self.snmp_type == 'GAUGE':
            self.value = session.gauge(variable.value)
        elif self.snmp_type == 'IPADDR':
            self.value = session.ipaddr(variable.value)
        elif self.snmp_type == 'OCTETSTR':
            self.value = session.octetstr(variable.value)
        elif self.snmp_type == 'TICKS':
            self.value = session.ticks(variable.value)
        elif self.snmp_type == 'OPAQUE':
            self.value = session.opaque(variable.value)
        elif self.snmp_type == 'OBJECTID':
            self.value = session.objectid(variable.value)
        elif self.snmp_type == 'NETADDR':
            self.value = session.netaddr(variable.value)
        elif self.snmp_type == 'COUNTER':
            self.value = session.counter(variable.value)
        elif self.snmp_type == 'NULL':
            self.value = session.null(variable.value)
        elif self.snmp_type == 'BITS':
            self.value = session.bits(variable.value)
        elif self.snmp_type == 'UINTEGER':
            self.value = session.uinteger(variable.value)
        else:
            self.value = session.default(variable.value)
        
        

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
        import ipaddress
        return ipaddress.ip_address(value)
                
    def octetstr(self, value):
        # TODO: Come up with some clever logic!
        return value

    def ticks(self, value):
        # TODO: convert to datetime.timedelta
        return datetime.timedelta(seconds=int(value))
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
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _snmp(self, method, *args, **kwargs):
        v = method(*args, **kwargs)
        if isinstance(v, easysnmp.SNMPVariable):
            return SNMPVariable(self, v)
        elif isinstance(v, (easysnmp.variables.SNMPVariableList, list)):
            return [SNMPVariable(self, i) for i in v]
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

    def set(selfs, *args, **kwargs):
        raise NotImplementedError
    
    def set_multiple(selfs, *args, **kwargs):
        raise NotImplementedError
    
    def get_next(selfs, *args, **kwargs):
        raise NotImplementedError




# Easy API
