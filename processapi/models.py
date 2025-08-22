from django.db import models

class Host(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    last_seen = models.DateTimeField(auto_now=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    processor = models.CharField(max_length=255, null=True, blank=True)
    ram_total = models.FloatField(null=True, blank=True)  
    ram_used = models.FloatField(null=True, blank=True)   
    ram_available = models.FloatField(null=True, blank=True)  
    storage_total = models.FloatField(null=True, blank=True)  
    storage_free = models.FloatField(null=True, blank=True)   

    def __str__(self):
        return self.hostname

class Process(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='processes')
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    parent_pid = models.IntegerField(null=True)
    cpu_percent = models.FloatField(default=0.0)
    memory_percent = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    has_children = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (PID: {self.pid})"