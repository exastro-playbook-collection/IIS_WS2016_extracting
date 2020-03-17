import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/command/0/stdout.txt"

result = {}
featureList = ['Web-Server','Web-WebServer','Web-Security','Web-Filtering','Web-Cert-Auth','Web-IP-Security','Web-Url-Auth','Web-Windows-Auth','Web-Basic-Auth','Web-CertProvider''Web-Client-Auth','Web-Digest-Auth','Web-Common-Http','Web-Http-Errors','Web-Static-Content','Web-Default-Doc','Web-Dir-Browsing','Web-Http-Redirect','Web-DAV-Publishing','Web-Performance','Web-Stat-Compression','Web-Dyn-Compression','Web-Health','Web-Http-Logging','Web-ODBC-Logging','Web-Http-Tracing','Web-Request-Monitor','Web-Log-Libraries','Web-Custom-Logging','Web-App-Dev','Web-Net-Ext','Web-Net-Ext45','Web-ASP','Web-Asp-Net','Web-Asp-Net45','Web-CGI','Web-ISAPI-Ext','Web-ISAPI-Filter','Web-WebSockets','Web-Includes','Web-AppInit','Web-Ftp-Server','Web-Ftp-Service','Web-Ftp-Ext','Web-Mgmt-Tools','Web-Mgmt-Console','Web-Mgmt-Compat','Web-Metabase','Web-WMI','Web-Lgcy-Mgmt-Console','Web-Lgcy-Scripting','Web-Scripting-Tools','Web-Mgmt-Service','NET-Framework-Features','NET-Framework-Core','NET-HTTP-Activation','NET-Non-HTTP-Activ','NET-Framework-45-Features','NET-Framework-45-Core','NET-Framework-45-ASPNET','NET-WCF-Services45','NET-WCF-HTTP-Activation45','NET-WCF-TCP-PortSharing45','NET-WCF-TCP-Activation45','NET-WCF-Pipe-Activation45','NET-WCF-MSMQ-Activation45']
featureList_tmp = []
if os.path.isfile(filename):
    fo = open(filename)
    readlines = fo.readlines()
    for strLine in readlines:
        for feature in featureList:
            featureName = feature + '\s*Installed'
            str_match = re.match(featureName, strLine)
            if str_match is not None:
                featureList_tmp.append(feature)
                break
    fo.close()
    if len(featureList_tmp) > 0:
        featureName = ','.join(featureList_tmp)
        result['VAR_IIS_FEATURE_NAME'] = featureName
print(json.dumps(result))


