import os
from dbstream.tunnel import create_ssh_tunnel


class DBStream:

    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.instance_type_prefix = ""
        self.ssh_init_port = ""
        self.ssh_tunnel = None

    def prefix(self):
        return self.instance_type_prefix + "_" + self.instance_name

    def remote_host(self):
        return os.environ[self.prefix() + "_HOST"]

    def remote_port(self):
        return os.environ[self.prefix() + "_PORT"]

    def credentials(self):
        if self.ssh_tunnel:
            host = self.ssh_tunnel.local_bind_host
            port = self.ssh_tunnel.local_bind_port
        else:
            host = self.remote_host()
            port = self.remote_port()
        return {
            'database': os.environ[self.prefix() + "_DATABASE"],
            'user': os.environ[self.prefix() + "_USERNAME"],
            'host': host,
            'port': port,
            'password': os.environ[self.prefix() + "_PASSWORD"],
        }

    def create_tunnel(self):
        self.ssh_tunnel = create_ssh_tunnel(
            instance=self.instance_name,
            port=self.ssh_init_port,
            remote_host=self.remote_host(),
            remote_port=self.remote_port()
        )
        return self.ssh_tunnel

    def execute_query(self, query):
        pass

    def send_data(self, data, replace=True):
        pass

    def _send(self, data, replace, batch_size=1000):
        pass
