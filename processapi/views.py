from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Host, Process
from .serializers import ProcessSerializer, HostSerializer
from django.conf import settings
API_KEY = "Hello"

class ProcessDataAPI(APIView):
    def post(self, request):
        key = request.headers.get("API-Key")
        if key is None or key.lower() != API_KEY.lower():
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        hostname = data.get("hostname")
        system_details = data.get("system_details", {})
        processes = data.get("processes", [])

        if not hostname:
            return Response({"error": "Hostname is required"}, status=status.HTTP_400_BAD_REQUEST)

        host, created = Host.objects.get_or_create(hostname=hostname)
        if created or system_details:
            for key, value in system_details.items():
                if hasattr(host, key) and value is not None:
                    setattr(host, key, value)
            host.save()

        for p in processes:
            try:
                Process.objects.update_or_create(
                    host=host,
                    pid=p['pid'],
                    defaults={
                        'name': p['name'],
                        'parent_pid': p.get('parent_pid'),
                        'cpu_percent': float(p.get('cpu_percent', 0)),
                        'memory_percent': float(p.get('memory_percent', 0)),
                        'memory_usage': float(p.get('memory_usage', 0)),
                        'has_children': p.get('has_children', False)
                    }
                )
            except (KeyError, ValueError) as e:
                continue 

        return Response({"status": "success"})

class HostProcessesAPI(APIView):
    def get(self, request, hostname):
        try:
            host = Host.objects.get(hostname=hostname)
        except Host.DoesNotExist:
            return Response({"error": "Host not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HostSerializer(host)
        return Response(serializer.data)

def frontend_view(request):
   
    hosts = Host.objects.all().order_by('-last_seen')

    host_data = []
    for host in hosts:
       
        processes = Process.objects.filter(host=host).values(
            'pid', 'name', 'parent_pid',
            'cpu_percent', 'memory_percent', 'memory_usage', 'has_children'
        )

      
        system_details = {
            "Operating System": host.os,
            "Processor": host.processor,
            "RAM Total": f"{host.ram_total:.2f} GB",
            "RAM Used": f"{host.ram_used:.2f} GB",
            "RAM Available": f"{host.ram_available:.2f} GB",
            "Storage Total": f"{host.storage_total:.2f} GB",
            "Storage Free": f"{host.storage_free:.2f} GB",
        }

        host_data.append({
            "hostname": host.hostname,
            "last_seen": host.last_seen,
            "system_details": system_details,
            "processes": list(processes)
        })

    return render(request, "index.html", {"hosts": host_data})