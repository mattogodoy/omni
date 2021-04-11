import os
import psutil
import socket


class Stats():
    def __init__(self):
        psutil.PROCFS_PATH = '/rootfs/proc'
        self.hostname = os.getenv('OMNI_HOST_NAME', socket.gethostname())
        self.ip = os.getenv('OMNI_HOST_IP', '0.0.0.0')

    def get_cpu(self):
        cpu = {
            'count': psutil.cpu_count(),
            'frequency_mhz': psutil.cpu_freq().max,
            'usage_percent': psutil.cpu_percent()
        }

        return cpu

    def get_memory(self):
        mem = psutil.virtual_memory()
        memory = {
            'used_percent': mem.percent,
            'total_gb': round(mem.total / (1024.0 ** 3), 2),
        }

        return memory

    def get_disk(self):
        disk = psutil.disk_usage('/')
        disk = {
            'used_gb': round(disk.used / (1024.0 ** 3), 2),
            'available_gb': round(disk.free / (1024.0 ** 3), 2),
            'total_gb': round(disk.total / (1024.0 ** 3), 2)
        }

        return disk

    def get_temperature(self):
        """ Works in Raspberry Pi only """
        cpu_temp = 0
        try:
            cpu_temp = round(psutil.sensors_temperatures().get('cpu_thermal', {})[0].current, 1)
        except Exception:
            pass

        return {'temperature_c': cpu_temp}

    def get_network(self):
        net = {
            'hostname': self.hostname,
            'local_ip': self.ip
        }

        return net

    def get_all(self, influx_format=False):
        cpu = self.get_cpu()
        memory = self.get_memory()
        disk = self.get_disk()
        temperature = self.get_temperature()
        network = self.get_network()

        tags = {
            'hostname': network['hostname'],
            'ip': network['local_ip']
        }

        if influx_format:
            stats = [
                {
                    'measurement': 'cpu',
                    'tags': tags,
                    'fields': {
                        'count': cpu['count'],
                        'frequency_mhz': cpu['frequency_mhz'],
                        'usage_percent': cpu['usage_percent']
                    }
                },
                {
                    'measurement': 'memory',
                    'tags': tags,
                    'fields': {
                        'used_percent': memory['used_percent'],
                        'total_gb': memory['total_gb']
                    }
                },
                {
                    'measurement': 'disk',
                    'tags': tags,
                    'fields': {
                        'used_gb': disk['used_gb'],
                        'available_gb': disk['available_gb'],
                        'total_gb': disk['total_gb']
                    }
                },
                {
                    'measurement': 'temperature',
                    'tags': tags,
                    'fields': {
                        'temperature_c': temperature['temperature_c']
                    }
                }
            ]
        else:
            stats = {
                'cpu': cpu,
                'memory': memory,
                'disk': disk,
                'temperature': temperature,
                'network': network
            }

        return stats
