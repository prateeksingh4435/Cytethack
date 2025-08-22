from rest_framework import serializers
from .models import Host, Process

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['pid', 'name', 'parent_pid', 'cpu_percent', 'memory_percent', 'memory_usage', 'has_children']

class HostSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True, read_only=True)

    class Meta:
        model = Host
        fields = ['hostname', 'os', 'processor', 'ram_total', 'ram_used', 'ram_available', 'storage_total', 'storage_free', 'last_seen', 'processes']