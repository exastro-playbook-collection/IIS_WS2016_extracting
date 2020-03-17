
import json
import os
import random
import xml.dom.minidom as xmldom
import re
import sys

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/command/3/stdout.txt"

#filename = "D:/SVN/Ansible02/pargen-IIS/roles/stdout.txt"
result = {}
applicationPools_list = []
website_list = []
website_list_result = []


def getTagNodes(elementObj, tagName):
    nodeList = elementObj.getElementsByTagName(tagName)
    return nodeList


def getChildNodes(node):
    nodeList = node.childNodes
    return nodeList


def getNodeLocalName(node):
    return node.localName


def hasChildNodes(node):
    return node.hasChildNodes()

def getPoolNodeAttri(node, nodeMap, nodename):
    nodeArrributes = node.attributes
    i = 0
    if nodeArrributes is not None and nodeArrributes.length != 0:
        while nodeArrributes.length != 0 and i < nodeArrributes.length:
            nodeAttr = nodeArrributes.item(i)
            if nodename is not None:
                attriName = nodename + '.' + nodeAttr.name
            #attriName = getNodeLocalName(node.parentNode) + '.' + getNodeLocalName(node) + '.' + nodeAttr.name
                nodeMap[attriName] = nodeAttr.value
            i = i + 1
        if hasChildNodes(node):
            childNodeList = getChildNodes(node)
            if childNodeList is not None and childNodeList.length > 0:
                for childNode in childNodeList:
                    if getNodeLocalName(childNode) is not None:
                        nodename = nodename + '.' + getNodeLocalName(childNode) + '.'
                        nodeMap = getPoolNodeAttri(childNode, nodeMap, nodename)

    if nodeArrributes is not None and nodeArrributes.length == 0:
        if hasChildNodes(node):
            childNodeList = getChildNodes(node)
            if childNodeList is not None and childNodeList.length > 0:
                for childNode in childNodeList:
                    if getNodeLocalName(childNode) is not None:
                        nodename = nodename + '.' + getNodeLocalName(childNode) + '.'
                        nodeMap = getPoolNodeAttri(childNode, nodeMap, nodename)
    return nodeMap


def getWebsiteNodeAttri(parentNode, index, node, nodeMap):
    nodeName = None
    if parentNode is not None and getNodeLocalName(parentNode) == 'application':
        parentAttributes = parentNode.attributes
        if parentAttributes is not None and parentAttributes.length > 0:
            j = 0
            while j < parentAttributes.length:
                if parentAttributes.item(j).name == 'path':
                    nodeName = parentAttributes.item(j).value.split('/')[1]
                    break
                j = j + 1
    if node is not None and getNodeLocalName(node) == 'application':
        appliAttributes = node.attributes
        if appliAttributes is not None and appliAttributes.length > 0:
            j = 0
            while j < appliAttributes.length:
                if appliAttributes.item(j).name == 'path':
                    nodeName = appliAttributes.item(j).value.split('/')[1]
                    break
                j = j + 1
    nodeArrributes = node.attributes
    if nodeArrributes is not None and nodeArrributes.length != 0:
        i = 0
        while nodeArrributes.length != 0 and i < nodeArrributes.length:
            nodeAttr = nodeArrributes.item(i)
            if nodeName is not None:
                attriName = getNodeLocalName(node.parentNode) + '.' + nodeName + '.' + getNodeLocalName(node) + str(
                    index) + '.' + nodeAttr.name
            else:
                attriName = getNodeLocalName(node.parentNode) + '.' + getNodeLocalName(node) + str(
                    index) + '.' + nodeAttr.name
            nodeMap[attriName] = nodeAttr.value
            i = i + 1
        if hasChildNodes(node):
            childNodeList = getChildNodes(node)
            if childNodeList is not None and childNodeList.length > 0:
                ii = 0
                while ii < len(childNodeList):
                    nodeMap = getWebsiteNodeAttri(node, ii, childNodeList[ii], nodeMap)
                    ii = ii + 1

    if nodeArrributes is not None and nodeArrributes.length == 0:
        if hasChildNodes(node):
            childNodeList = getChildNodes(node)
            if childNodeList is not None and childNodeList.length > 0:
                i = 0
                while i < len(childNodeList):
                    nodeMap = getWebsiteNodeAttri(node, i, childNodeList[i], nodeMap)
                    i = i + 1

    return nodeMap


# main process
if os.path.isfile(filename):
    doc = xmldom.parse(filename)
    applicationHost = getTagNodes(doc, "system.applicationHost")
    if applicationHost is not None and applicationHost.length > 0:
        # get applicationPools
        applicationPools = getTagNodes(applicationHost[0], "applicationPools")
        if applicationPools is not None and applicationPools.length > 0:
            pool_nodeList = getTagNodes(applicationPools[0], "add")
            if pool_nodeList is not None and pool_nodeList.length > 0:
                for pool in pool_nodeList:
                    poolMap = {}
                    poolMap = getPoolNodeAttri(pool, poolMap, 'add')
                    applicationPools_list.append(poolMap)
            pool_nodeList = getTagNodes(applicationPools[0], "applicationPoolDefaults")
            if pool_nodeList is not None and pool_nodeList.length > 0:
                for pool in pool_nodeList:
                    poolMap = {}
                    poolMap = getPoolNodeAttri(pool, poolMap, 'applicationPoolDefaults')
                    applicationPools_list.append(poolMap)
       # print 'applicationPools_list is:', applicationPools_list

        # get sites
        sites = getTagNodes(applicationHost[0], "sites")
        if sites is not None and sites.length > 0:
            site_nodeList = getTagNodes(sites[0], "site")
            if site_nodeList is not None and site_nodeList.length > 0:
                for site in site_nodeList:
                    siteMap = {}
                    siteMap = getWebsiteNodeAttri(None, 0, site, siteMap)
                    website_list.append(siteMap)
            site_nodeList = getTagNodes(sites[0], "siteDefaults")
            if site_nodeList is not None and site_nodeList.length > 0:
                for site in site_nodeList:
                    siteMap = {}
                    siteMap = getWebsiteNodeAttri(None, 0, site, siteMap)
                    website_list.append(siteMap)
            site_nodeList = getTagNodes(sites[0], "applicationDefaults")
            if site_nodeList is not None and site_nodeList.length > 0:
                for site in site_nodeList:
                    siteMap = {}
                    siteMap = getWebsiteNodeAttri(None, 0, site, siteMap)
                    website_list.append(siteMap)
            site_nodeList = getTagNodes(sites[0], "virtualDirectoryDefaults")
            if site_nodeList is not None and site_nodeList.length > 0:
                for site in site_nodeList:
                    siteMap = {}
                    siteMap = getWebsiteNodeAttri(None, 0, site, siteMap)
                    website_list.append(siteMap)
#print('website_list is:', website_list)

# get all website information:application, virtual, binding
defaultPool_name = None
if len(website_list) > 0:
    for website_info in website_list:
        websiteMap = {}
        parameter_map = {}
        applicationId_list = []
        bindingId_list = []
        dict_keys = website_info.keys()
        # get application and binging for each website,  and virtual for application
        # 1. Get the ID that distinguishes each application, virtual, binding
        for key in dict_keys:
            key_match = re.match('sites.site\d*.name', key)
            if key_match is not None:
                key = key_match.group().strip()
                websiteMap['VAR_WEBSITE_NAME'] = website_info.get(key)
            key_match = re.match('site.(.*)\d*.application\d*.path', key)
            if key_match is not None:
                applicationId_list.append(key_match.group(1).strip())
            key_match = re.match('bindings.binding(\d*).protocol', key)
            if key_match is not None:
                bindingId_list.append(key_match.group(1).strip())
        # 2. Use id to assign application to the corresponding website group.
        # Use id to assign virtual to the corresponding application group.

        for key in dict_keys:
            isParam = False
            key_match = re.match('sites.site' + '\d*..*', key)
            if key_match is not None:
                isParam = True
                continue
            key_match = re.match('bindings.binding' + '\d*..*', key)
            if key_match is not None:
                isParam = True
                continue
            key_match = re.match('sites.virtualDirectoryDefaults' + '\d*..*', key)
            if key_match is not None:
                isParam = True
                continue
            key_match = re.match('sites.applicationDefaults' + '\d*..*', key)
            if key_match is not None:
                isParam = True
                continue
            for applicationId in applicationId_list:
                key_match = re.match('site.' + applicationId + '\d*.application\d*..*', key)
                if key_match is not None:
                    isParam = True
                    break
                key_match = re.match('application.' + applicationId + '\d*.virtualDirectory(\d*)..*', key)
                if key_match is not None:
                    isParam = True
                    break
            if isParam == False:
                parameter_map[key] = website_info.get(key)
        websiteMap['parameters'] = parameter_map
        siteApplication_list = []
        for applicationId in applicationId_list:
            applicationMap = {}
            applicationVirtual_list = []
            virtualDirId_list = []
            for key in dict_keys:
                key_match = re.match('site.' + applicationId + '\d*.application\d*.applicationPool', key)
                if key_match is not None:
                    applicationMap['applicationPool'] = website_info.get(key)
                    continue
                key_match = re.match('site.' + applicationId + '\d*.application\d*.path', key)
                if key_match is not None:
                    applicationMap['applicationPath'] = website_info.get(key)
                    continue
                key_match = re.match('application.' + applicationId + '\d*.virtualDirectory(\d*).physicalPath', key)
                if key_match is not None:
                    virtualDirId_list.append(key_match.group(1).strip())
                    continue
            applicationMap['applicationName'] = applicationId
            for virtualDirId in virtualDirId_list:
                applicationVirtualMap = {}
                for key in dict_keys:
                    key_match = re.match(
                        'application.' + applicationId + '\d*.virtualDirectory' + virtualDirId + '.path', key)
                    if key_match is not None:
                        applicationVirtualMap['path'] = website_info.get(key)
                    key_match = re.match(
                        'application.' + applicationId + '\d*.virtualDirectory' + virtualDirId + '.physicalPath',
                        key)
                    if key_match is not None:
                        applicationVirtualMap['physicalPath'] = website_info.get(key)
                if len(applicationVirtualMap) > 0:
                    applicationVirtual_list.append(applicationVirtualMap)
            if len(applicationVirtual_list) > 0:
                applicationMap['vituralDirList'] = applicationVirtual_list
            if len(applicationMap) > 0:
                siteApplication_list.append(applicationMap)
        websiteMap['application'] = siteApplication_list

        # 3. Use id to assign binding to the corresponding website group.
        siteBinding_list = []
        for bindId in bindingId_list:
            bindingMap = {}
            for key in dict_keys:
                key_match = re.match('bindings.binding' + bindId + '.protocol', key)
                if key_match is not None:
                    bindingMap['protocol'] = website_info.get(key)
                key_match = re.match('bindings.binding' + bindId + '.bindingInformation', key)
                if key_match is not None:
                    bindingMap['bindingInformation'] = website_info.get(key)
                key_match = re.match('bindings.binding' + bindId + '.sslFlags', key)
                if key_match is not None:
                    bindingMap['sslFlags'] = website_info.get(key)
            if len(bindingMap) > 0:
                siteBinding_list.append(bindingMap)
        if len(siteBinding_list) > 0:
            websiteMap['binding'] = siteBinding_list
        website_list_result.append(websiteMap)
        for key in dict_keys:
            defaultPool_match = re.match('sites\d*.applicationDefaults\d*.applicationPool', key)
            if defaultPool_match is not None:
                defaultPool_name = website_info.get(key)
                break
    website_list_result.append(websiteMap)
# print('website_list_result is:',website_list_result)

# Finalize the parameters in applicationPools_list_tmp to VAR_WEBAPPPOOL_NAME and VAR_WEBAPPPOOL_ATTRI
# get all applicationPools information
applicationPools_list_tmp = []
defaultPoolMap = {}
if len(applicationPools_list) > 0:
    for applicationPool in applicationPools_list:
        webapppool_map = {}
        pool_keys = applicationPool.keys()
        for pool_key in pool_keys:
            attri_match = re.match('add..*(recycling.*)', pool_key)
            if attri_match is not None:
                attriName = attri_match.group(1).strip().replace('..', '.')
                if (re.match('.*(processModel).*', attriName) is None) and (re.match('.*(failure).*', attriName) is None) and (re.match('.*(cpu).*', attriName) is None):
                    webapppool_map[attriName] = applicationPool.get(pool_key)
                    continue
            secondAttri_match = re.match('add..*(failure.*)', pool_key)
            if secondAttri_match is not None:
                attriName = secondAttri_match.group(1).strip().replace('..', '.')
                if (re.match('.*(processModel).*', attriName) is None) and (re.match('.*(recycling).*', attriName) is None) and (re.match('.*(cpu).*', attriName) is None):
                    webapppool_map[attriName] = applicationPool.get(pool_key)
                    continue
            threeAttri_match = re.match('add..*(cpu.*)', pool_key)
            if threeAttri_match is not None:
                attriName = threeAttri_match.group(1).strip().replace('..', '.')
                if (re.match('.*(processModel).*', attriName) is None) and (re.match('.*(recycling).*', attriName) is None) and (re.match('.*(failure).*', attriName) is None):
                    webapppool_map[attriName] = applicationPool.get(pool_key)
                    continue
            threeAttri_match = re.match('add..*(processModel.*)', pool_key)
            if threeAttri_match is not None:
                attriName = threeAttri_match.group(1).strip().replace('..', '.')
                if (re.match('.*(cpu).*', attriName) is None) and (re.match('.*(recycling).*', attriName) is None) and (re.match('.*(failure).*', attriName) is None):
                    webapppool_map[attriName] = applicationPool.get(pool_key)
                    continue
            Attri_match = re.match('add.(.*)', pool_key)
            if Attri_match is not None:
                attriName = Attri_match.group(1).strip().replace('..', '.')
                webapppool_map[attriName] = applicationPool.get(pool_key)
                continue
            poolDefault_match = re.match('applicationPoolDefaults.(.*)', pool_key)
            if poolDefault_match is not None:
                attriName = poolDefault_match.group(1).strip().replace('..', '.')
                defaultPoolMap[attriName] = applicationPool.get(pool_key)
                if defaultPool_name is not None:
                    defaultPoolMap['name'] = defaultPool_name
                continue

            '''
            poolDefault_match = re.match('applicationPools.applicationPoolDefaults.(.*)', pool_key)
            if poolDefault_match is not None:
                defaultPoolMap[poolDefault_match.group(1).strip()] = applicationPool.get(pool_key)
                continue
            if re.match('applicationPool(.*)', pool_key) is not None:
                continue
            threeAttri_match = re.match('^(.*)', pool_key)
            if threeAttri_match is not None:
                webapppool_map[threeAttri_match.group(1).strip()] = applicationPool.get(pool_key)
'''
        if len(webapppool_map) > 0:
            applicationPools_list_tmp.append(webapppool_map)
#print 'applicationPools_list_tmp is:', applicationPools_list_tmp

for poolmap in applicationPools_list_tmp:
    if 'name' in poolmap and poolmap['name'] == defaultPoolMap['name']:
        keys = poolmap.keys()
        if keys is not None and len(keys) > 0:
            for key in keys:
                defaultPoolMap[key] = poolmap.get(key)
        applicationPools_list_tmp.remove(poolmap)
        applicationPools_list_tmp.append(defaultPoolMap)
        break
# 'applicationPools_list_tmp is:', applicationPools_list_tmp
pools_list = []

for pool in applicationPools_list_tmp:
    pool_map = {}
    poolAttri_map = {}
    keys = pool.keys()
    for key in keys:
        if 'name' == key:
            pool_map['VAR_WEBAPPPOOL_NAME'] = pool.get(key)
        else:
            poolAttri_map[key] = pool.get(key)
    if len(poolAttri_map) > 0:
        pool_map['VAR_WEBAPPPOOL_ATTRI'] = poolAttri_map
    if len(pool_map) > 0:
        pools_list.append(pool_map)
# ('website_list_result is:', website_list_result)
# Finalize the parameters in website_list_result to VAR_WEBSITE_NAME and VAR_WEBBINDING_INFO and VAR_WEBAPP_INFO and VAR_VIRTUALDIR_INFO
websiteInfo_list = []
for website in website_list_result:
    websiteMap = {}
    websiteInfo = {}
    keys = website.keys()
    for key in keys:
        if 'VAR_WEBSITE_NAME' == key:
            websiteMap['VAR_WEBSITE_NAME'] = website.get(key)
        if 'binding' == key:
            bindingList = []
            bindings = website.get(key)
            for binding in bindings:
                bindingMap = {}
                if 'sslFlags' in binding:
                    bindingMap['sslFlags'] = int(binding.get('sslFlags'))
                if binding.get('protocol') == 'http' or binding.get('protocol') == 'https':
                    bindinginforList = binding.get('bindingInformation').split(':')
                    if len(bindinginforList) == 2:
                        if bindinginforList[0] != '*':
                            bindingMap['ip'] = bindinginforList[0]
                        bindingMap['port'] = bindinginforList[1]
                    if len(bindinginforList) == 3:
                        if bindinginforList[0] != '*':
                            bindingMap['ip'] = bindinginforList[0]
                        bindingMap['port'] = bindinginforList[1]
                        if bindinginforList[2] != '':
                            bindingMap['host_header'] = bindinginforList[2]
                    bindingMap['protocol'] = binding.get('protocol')
                else:
                    bindingMap['protocol'] = binding.get('protocol')
                    bindingMap['host_header'] = binding.get('bindingInformation')
                    bindingMap['protocol'] = binding.get('protocol')
                if len(bindingMap) > 0:
                    bindingList.append(bindingMap)
            if len(bindingList) > 0:
                websiteMap['VAR_WEBBINDING_INFO'] = bindingList
        if 'application' == key:
            applicationList = website.get(key)
            application_list = []
            websitePhysicalPath = False
            virtual_list = []
            for application in applicationList:
                applicationName = ''
                applicationMap = {}
                if '/' != application.get('applicationPath'):
                    applicationName = application.get('applicationPath').split('/')[1]
                    applicationMap['name'] = applicationName
                    if 'applicationPool' in application and application.get('applicationPool') is not None:
                        applicationMap['poolname'] = application.get('applicationPool')
                if '/' == application.get('applicationPath'):
                    websiteMap['poolname'] = application.get('applicationPool')
                    websitePhysicalPath = True
                virtualList = application.get('vituralDirList')
                for virtual in virtualList:
                    virtualMap = {}
                    if '/' == virtual.get('path'):
                        if websitePhysicalPath == False:
                            applicationMap['physical_path'] = virtual.get('physicalPath')
                        if websitePhysicalPath == True:
                            websiteInfo['physical_path'] = virtual.get('physicalPath')
                            websitePhysicalPath = False
                    elif '/' != virtual.get('path'):
                        virtualMap['name'] = virtual.get('path').split('/')[1]
                        virtualMap['physical_path'] = virtual.get('physicalPath')
                        if applicationName != '':
                            virtualMap['application'] = applicationName
                    if len(virtualMap) > 0:
                        virtual_list.append(virtualMap)
                if len(applicationMap) > 0:
                    application_list.append(applicationMap)
            if len(virtual_list) > 0:
                websiteMap['VAR_VIRTUALDIR_INFO'] = virtual_list
                # print ("virtual_list is:", websiteMap['VAR_VIRTUALDIR_INFO'])
            if len(application_list) > 0:
                websiteMap['VAR_WEBAPP_INFO'] = application_list
        if 'parameters' == key:
            parameterStr = None
            paramMap = website.get(key)
            parametersList_tmp = []
            paramKeys = list(paramMap.keys())
            if len(paramKeys) > 0:
                i = 0
                while i < len(paramKeys):
                    paramName_list = paramKeys[i].split('.', 2)
                    if paramName_list is not None and len(paramName_list) == 3:
                        paramName = re.sub('\d', '', paramName_list[1].strip()) + '.' + paramName_list[2].strip()
                        parameterStr = '"' + paramName + '":"' + paramMap.get(paramKeys[i]) + '"'
                        parametersList_tmp.append(parameterStr)
                    i = i + 1
                parameterStr = '|'.join(parametersList_tmp)
            if parameterStr is not None:
                websiteInfo['parameters'] = parameterStr
            websiteMap['VAR_WEBSITE_INFO'] = websiteInfo
    if len(websiteMap) > 0:
        websiteInfo_list.append(websiteMap)
#print 'websiteInfo_list is:', websiteInfo_list
#print 'pools_list is:', pools_list
result_list = []
website_pool_list = []
for pool in pools_list:
    result_map = {}
    #print "pool['VAR_WEBAPPPOOL_NAME'] is:", pool['VAR_WEBAPPPOOL_NAME']
    for website in websiteInfo_list:
        if 'VAR_WEBAPPPOOL_NAME' in pool and 'poolname' in website:
            #print 'poolname is:', website['poolname']
            if pool['VAR_WEBAPPPOOL_NAME'] == website['poolname']:
                #pools_list.remove(pool)
                website_pool_list.append(pool)
                result_map['VAR_IIS_OS_Version'] = 'Windows Server 2016'
                result_map['VAR_WEBAPPPOOL_NAME'] = pool['VAR_WEBAPPPOOL_NAME']
                if 'VAR_WEBAPPPOOL_ATTRI' in pool:
                    result_map['VAR_WEBAPPPOOL_ATTRI'] = pool['VAR_WEBAPPPOOL_ATTRI']
                result_map['VAR_WEBSITE_NAME'] = website['VAR_WEBSITE_NAME']
                if 'VAR_WEBSITE_INFO' in website:
                    result_map['VAR_WEBSITE_INFO'] = website['VAR_WEBSITE_INFO']
                if 'VAR_WEBBINDING_INFO' in website:
                    result_map['VAR_WEBBINDING_INFO'] = website['VAR_WEBBINDING_INFO']
                if 'VAR_WEBAPP_INFO' in website:
                    result_map['VAR_WEBAPP_INFO'] = website['VAR_WEBAPP_INFO']
                if 'VAR_VIRTUALDIR_INFO' in website:
                    result_map['VAR_VIRTUALDIR_INFO'] = website['VAR_VIRTUALDIR_INFO']
            if website['poolname'] is None and pool['VAR_WEBAPPPOOL_NAME'] == defaultPool_name:
                #print 'defaultPool_name is:', defaultPool_name
                pools_list.remove(pool)
                result_map['VAR_IIS_OS_Version'] = 'Windows Server 2016'
                result_map['VAR_WEBAPPPOOL_NAME'] = defaultPool_name
                if pool['VAR_WEBAPPPOOL_NAME'] == defaultPool_name and 'VAR_WEBAPPPOOL_ATTRI' in pool:
                    result_map['VAR_WEBAPPPOOL_ATTRI'] = pool['VAR_WEBAPPPOOL_ATTRI']
                result_map['VAR_WEBSITE_NAME'] = website['VAR_WEBSITE_NAME']
                if 'VAR_WEBSITE_INFO' in website:
                    result_map['VAR_WEBSITE_INFO'] = website['VAR_WEBSITE_INFO']
                if 'VAR_WEBBINDING_INFO' in website:
                    result_map['VAR_WEBBINDING_INFO'] = website['VAR_WEBBINDING_INFO']
                if 'VAR_WEBAPP_INFO' in website:
                    result_map['VAR_WEBAPP_INFO'] = website['VAR_WEBAPP_INFO']
                if 'VAR_VIRTUALDIR_INFO' in website:
                    result_map['VAR_VIRTUALDIR_INFO'] = website['VAR_VIRTUALDIR_INFO']
    # print('result_map is:', result_map)
    if len(result_map) > 0:
        result_list.append(result_map)
#print 'pools_list is:', pools_list
#print 'website_pool_list is:', website_pool_list
singPoolList = []
for pool in pools_list:
    isSingle = True
    for website_pool in website_pool_list:
        if 'VAR_WEBAPPPOOL_NAME' in website_pool and 'VAR_WEBAPPPOOL_NAME' in pool:
            if website_pool['VAR_WEBAPPPOOL_NAME'] == pool['VAR_WEBAPPPOOL_NAME']:
                isSingle = False
                break
    if isSingle == True:
        singPoolList.append(pool)
#print 'singPoolList is:', singPoolList
for pool in singPoolList:
    result_map = {}
    if 'VAR_WEBAPPPOOL_NAME' in pool:
        result_map['VAR_IIS_OS_Version'] = 'Windows Server 2016'
        result_map['VAR_WEBAPPPOOL_NAME'] = pool['VAR_WEBAPPPOOL_NAME']
        if 'VAR_WEBAPPPOOL_ATTRI' in pool:
            result_map['VAR_WEBAPPPOOL_ATTRI'] = pool['VAR_WEBAPPPOOL_ATTRI']
        if len(result_map) > 0:
            result_list.append(result_map)
#result['websitelist'] = result_list
#print('result list is:', result_list)

result_count = {}
result_count['count'] = len(result_list)
print(json.dumps(result_count))


