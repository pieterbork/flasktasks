DEBUG = False
LOGIN = True
LDAP = False
#Anonymous bind
LDAP_SERVER = ""
#ou=Users,DC=example,DC=com
LDAP_CONN = ""
#uid
LDAP_SEARCH = ""
#{{LDAP_SEARCH}}={},{{LDAP_CONN}} => uid={},ou=Users,DC=example,DC=com
