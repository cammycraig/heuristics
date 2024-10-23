from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'NLSN', 'NLSN.urls', name='NLSN'),
                         )
