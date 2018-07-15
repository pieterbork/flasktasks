from flasktasks import config
from ldap3 import Server, Connection, ALL

def ldap_login(username, password):
    server = Server(config.LDAP_SERVER, get_info=ALL, use_ssl=False)
    conn = Connection(server, 'uid={0},ou=Users,{1}'.format(username, config.LDAP_DC), password)
    conn.bind()	#must be separate or conn throws runtime errors
    record = conn.result
    if record['result'] == 0 and record['description'] == 'success':
        r = conn.search(config.LDAP_DC, '(uid={})'.format(username), attributes=['*'])
        result = conn.entries
        return result
    else:
        return None
