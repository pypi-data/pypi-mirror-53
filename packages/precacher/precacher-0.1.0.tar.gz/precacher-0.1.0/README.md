# precacher

Replays the top N queries from a Pi-hole or dnscrypt-proxy log
file against a specific nameserver.

## Examples

```bash
$ precacher --file /var/log/pihole.log --servers 192.168.1.1 --top=1000
$ precacher --file /var/log/dnscrypt-proxy-query.log --format dnscrypt-proxy
-tsv --servers 192.168.1.1 --top=1000
$ precacher -h
```

### Configuring Pi-hole

Enable QUERY_LOGGING in your `setupVars.conf` file. Example:

```
QUERY_LOGGING=true
```

### Configuring dnscrypt-proxy 

Enable logging in your `dnscrypt-proxy.toml` file. Example:

```toml
[query_log]
  file = '/var/log/dnscrypt-proxy-query.log'
  format = 'tsv'
  ignored_qtypes = ['DNSKEY', 'NS']
```
