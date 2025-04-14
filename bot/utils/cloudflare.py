import CloudFlare

class CloudflareManager:
    def __init__(self, api_key, email):
        self.cf = CloudFlare.CloudFlare(email=email, token=api_key)

    def list_zones(self):
        return self.cf.zones.get()

    def purge_cache(self, zone_id, urls=None):
        data = {"purge_everything": True} if urls is None else {"files": urls}
        return self.cf.zones.purge_cache.post(zone_id, data=data)

    def list_dns_records(self, zone_id):
        return self.cf.zones.dns_records.get(zone_id)

    def add_dns_record(self, zone_id, record_type, name, content, ttl=120):
        data = {"type": record_type, "name": name, "content": content, "ttl": ttl}
        return self.cf.zones.dns_records.post(zone_id, data=data)

    def delete_dns_record(self, zone_id, record_id):
        return self.cf.zones.dns_records.delete(zone_id, record_id)

    def toggle_developer_mode(self, zone_id, enable=True):
        value = "on" if enable else "off"
        data = {"value": value}
        return self.cf.zones.settings.development_mode.patch(zone_id, data=data)

    def list_firewall_rules(self, zone_id):
        return self.cf.zones.firewall.rules.get(zone_id)

    def toggle_firewall_rule(self, zone_id, rule_id, enable=True):
        action = "allow" if enable else "block"
        data = {"action": action}
        return self.cf.zones.firewall.rules.patch(zone_id, rule_id, data=data)

    def list_ssl_tls_settings(self, zone_id):
        return self.cf.zones.settings.ssl.get(zone_id)

    def toggle_https_rewrite(self, zone_id, enable=True):
        value = "on" if enable else "off"
        data = {"value": value}
        return self.cf.zones.settings.automatic_https_rewrites.patch(zone_id, data=data)

    def get_analytics_report(self, zone_id, since="24 hours ago"):
        params = {"since": since}
        return self.cf.zones.analytics.dashboard.get(zone_id, params=params)