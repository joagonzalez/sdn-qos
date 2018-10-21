config = {
  'ari': {
    'host': 'http://asterisk:8088/',
    'username': 'asterisk',
    'password': 'asterisk',
  },
  'ryu': {
    'baseurl': 'http://ryu:8080',
  },
  'frontService': {
    'host': 'call_admission_control_backend',
    'listen': 8000
  },
  'client': {
    'baseurl': 'ws://call_admission_control_backend:8000',
  }
}
