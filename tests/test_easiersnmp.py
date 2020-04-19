
# TODO: 
# All tests use the SNMPLabs  
# (http://snmplabs.com/snmpsim/)
#
SNMP_HOSTNAME = 'markus5'
SNMPV2_COMMUNITY = 'public'
SNMPV3_AUTHPASS = ''
SNMPV3_PRIVPASS = ''
SNMPV3_AUTHPROTO = 'SHA'
SNMPV3_PRIVPROTO = 'DES'

SNMP_GET_OIDS = [
    'SNMPv2-MIB::sysName.0'
]


SNMP_WALK_OID = 'SNMPv2-MIB::system'

import easiersnmp
import ipaddress
import datetime


class SNMPv2(object):

    def __init__(self):
        self.session = easiersnmp.Session(SNMP_HOSTNAME, version=2, 
                                          community=SNMPV2_COMMUNITY)

class TestSNMPv2Session(SNMPv2):
        
    def test_get_octetstr(self):
        value = self.session.get('SNMPv2-MIB::sysName.0')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, str)

    def test_get_integer(self):
        value = self.session.get('IF-MIB::ifNumber.0')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, int)
        
    def test_get_gauge(self):
        value = self.session.get('IF-MIB::ifSpeed.1')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, int)
        
    def test_get_ipaddress(self):
        value = self.session.get('IP-MIB::ipAdEntAddr.10.1.1.101')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, ipaddress.IPv4Address)
        
    def test_get_ticks(self):
        value = self.session.get('SNMPv2-MIB::sysORLastChange.0')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, datetime.timedelta)
        
#    def test_get_opaque(self):
#        value = self.session.get('UCD-SNMP-MIB::laLoadFloat.1')
#        assert isinstance(value, easiersnmp.SNMPVariable)
#        assert isinstance(value.value, datetime.timedelta)

    def test_get_objectid(self):
        value = self.session.get('SNMPv2-MIB::sysObjectID.0')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, str)
        
#    def test_get_netaddr(self):
#        value = self.session.get('
#        assert isinstance(value, easiersnmp.SNMPVariable)
#        assert isinstance(value.value, str)
        
    def test_get_counter(self):
        value = self.session.get('IF-MIB::ifInOctets.1')
        assert isinstance(value, easiersnmp.SNMPVariable)
        assert isinstance(value.value, int)
    
#    def test_get_null(self):
#        value = self.session.get('
#        assert isinstance(value, easiersnmp.SNMPVariable)
#        assert isinstance(value.value, str)
        
#    def test_get_bits(self):
#        value = self.session.get('
#        assert isinstance(value, easiersnmp.SNMPVariable)
#        assert isinstance(value.value, str)
        
#    def test_get_uinteger(self):
#        value = self.session.get('
#        assert isinstance(value, easiersnmp.SNMPVariable)
#        assert isinstance(value.value, int)

    def test_multioid_get(self):
        values = self.session.get(['SNMPv2-MIB::sysName.0', 
                                        'SNMPv2-MIB::sysObjectID.0'])                                        
        assert len(values) > 1               
        for value in values:
            assert isinstance(value, easiersnmp.SNMPVariable)

    def test_multioid_getbulk(self):
        values = self.session.get_bulk(['SNMPv2-MIB::sysName.0', 
                                        'SNMPv2-MIB::sysObjectID.0'])
        assert len(values) > 1               
        for value in values:
            assert isinstance(value, easiersnmp.SNMPVariable) 
            
    def test_getbulk(self):
        values = self.session.get_bulk('SNMPv2-MIB::sysName.0')
        assert len(values) > 1               
        for value in values:
            assert isinstance(value, easiersnmp.SNMPVariable)
            
    def test_bulkwalk(self):
        values = self.session.bulkwalk('SNMPv2-MIB::system')
        assert len(values) > 1               
        for value in values:
            assert isinstance(value, easiersnmp.SNMPVariable)    
            
    def test_walk(self):
        values = self.session.walk('SNMPv2-MIB::system')
        assert len(values) > 1               
        for value in values:
            assert isinstance(value, easiersnmp.SNMPVariable)          
      
