import urllib.request
from os import getcwd
import os

#基础规则库-Clash
DirectClash = ["https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/China.yaml"]
ProxyClash = ["https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/StreamingMedia/Streaming.yaml",
               "https://raw.githubusercontent.com/DivineEngine/Profiles/master/Clash/RuleSet/Global.yaml"]
#自添加规则库-Clash [Direct,Proxy]
AddSetClash = ["https://raw.githubusercontent.com/729376442/Rule-Set/main/ClashRules/DirectList.yaml",
               "https://raw.githubusercontent.com/729376442/Rule-Set/main/ClashRules/ProxyList.yaml"]


#基础规则库-Quantumult
DirectQuantumult = ["https://raw.githubusercontent.com/DivineEngine/Profiles/master/Quantumult/Filter/China.list"]
ProxyQuantumult = ["https://raw.githubusercontent.com/DivineEngine/Profiles/master/Quantumult/Filter/StreamingMedia/Streaming.list",
                    "https://raw.githubusercontent.com/DivineEngine/Profiles/master/Quantumult/Filter/Global.list"]
#自添加规则库-Quantumult [Direct,Proxy]
AddSetQuantumult = ["https://raw.githubusercontent.com/729376442/Rule-Set/main/Quantumult/DirectList.list",
                    "https://raw.githubusercontent.com/729376442/Rule-Set/main/Quantumult/ProxyList.list"]

#基础规则库-Surge
DirectSurge = ["https://raw.githubusercontent.com/DivineEngine/Profiles/master/Surge/Ruleset/China.list"]
ProxySurge = ["https://raw.githubusercontent.com/DivineEngine/Profiles/master/Surge/Ruleset/StreamingMedia/Streaming.list",
               "https://raw.githubusercontent.com/DivineEngine/Profiles/master/Surge/Ruleset/Global.list"]
#自添加规则库-Surge [Direct,Proxy]
AddSetSurge = ["https://raw.githubusercontent.com/729376442/Rule-Set/main/SurgeRules/DirectList.list",
               "https://raw.githubusercontent.com/729376442/Rule-Set/main/SurgeRules/ProxyList.list"]


#去除自添加的冲突规则
ShowSelfConflictRules = 1
#去除与基础规则冲突的自添加规则
ShowBaseConflictRules = 0
#去除重复的自添加规则
ShowSelfDupliacteRules = 1
#去除与基础规则重复的自添加规则
ShowBaseDupliacteRules = 1

Clash = 0
Quantumult = 0
Surge = 1



def quchong(type):
    directory = getcwd()
    savepath = ""
    DirectList = []
    ProxyList = []
    AddSet = []
    filetype = ""
    if type == 'C' and DirectClash != [] and ProxyClash != [] and AddSetClash != []:
        savepath = directory + '\\Rules\\Clash'
        DirectList = DirectClash
        ProxyList = ProxyClash
        AddSet = AddSetClash
        filetype = ".yaml"
        print("Analyzing Clash Rules...")
    elif type == 'Q' and DirectQuantumult != [] and ProxyQuantumult != [] and AddSetQuantumult != []:
        savepath = directory + '\\Rules\\Quantumult'
        DirectList = DirectQuantumult
        ProxyList = ProxyQuantumult
        AddSet = AddSetQuantumult
        filetype = ".list"
        print("Analyzing Quantumult Rules...")
    elif type == 'S' and DirectSurge != [] and ProxySurge != [] and AddSetSurge != []:
        savepath = directory + '\\Rules\\Surge'
        DirectList = DirectSurge
        ProxyList = ProxySurge
        AddSet = AddSetSurge
        filetype = ".list"
        print("Analyzing Surge Rules...")
    else:
        print("Wrong parameters.")
        return
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    DirectRevision = open(savepath+"\\DirectList" + filetype, 'w')
    DirectDropped = open(savepath + "\\DirectDropped" + filetype, 'w')
    ProxyRevision = open(savepath + "\\ProxyList" + filetype, 'w')
    ProxyDropped = open(savepath + "\\ProxyDropped" + filetype, 'w')

    DirectRules = []
    ProxyRules = []

    for url in DirectList:
        tempstr = ""
        conn = urllib.request.urlopen(url)
        for html in conn.read().decode('utf-8'):
            tempstr += html
        DirectRules += tempstr.split('\n')

    for url in ProxyList:
        tempstr = ""
        conn = urllib.request.urlopen(url)
        for html in conn.read().decode('utf-8'):
            tempstr += html
        ProxyRules += tempstr.split('\n')

    if type == 'Q':
        for i in range(len(DirectRules)):
            if '#' not in DirectRules[i] and DirectRules[i].count(',') == 2:
                DirectRules[i] = DirectRules[i][0:DirectRules[i].rfind(',')]
        for i in range(len(ProxyRules)):
            if '#' not in ProxyRules[i] and ProxyRules[i].count(',') == 2:
                ProxyRules[i] = ProxyRules[i][0:ProxyRules[i].rfind(',')]

    AddDirectRules = []
    AddProxyRules = []

    tempstr = ""
    conn1 = urllib.request.urlopen(AddSet[0])
    for html in conn1.read().decode('utf-8'):
        tempstr += html
    tempDirect = tempstr.split('\n')
    tempstr = ""
    conn2 = urllib.request.urlopen(AddSet[1])
    for html in conn2.read().decode('utf-8'):
        tempstr += html
    tempProxy = tempstr.split('\n')
    conn1.close()
    conn2.close()

    DConflict = []
    DDupliacte = []
    DDirect = []
    DProxy = []
    DWarning = []
    DOut = [DWarning, DConflict, DDupliacte, DDirect, DProxy]
    for line in tempDirect:
        Quanline = line
        if type == 'Q' and line.count(',') == 2 and '#' not in line:
            line = line[0:line.rfind(',')]
        if "payload:" in line or '#' in line:
            DirectRevision.write(Quanline + "\n")
        else:
            count = 0
            templine = "===== " + Quanline
            if line in AddProxyRules and ShowSelfConflictRules:
                count += 1
                templine = "Self-Conflict " + templine
            if line in AddDirectRules and ShowSelfDupliacteRules:
                count += 1
                templine = "Self-Dupliacte " + templine
            if line in DirectRules and ShowBaseDupliacteRules:
                count += 1
                templine = "Base-Dupliacte " + templine
            if line in ProxyRules and ShowBaseConflictRules:
                count += 1
                templine = "Base-Conflict " + templine

            if count == 0:
                AddDirectRules.append(line)
                DirectRevision.write(Quanline + "\n")
            elif count == 1:
                if line in AddProxyRules and ShowSelfConflictRules:
                    DConflict.append(("##### Count = " + str(count) + " " + templine + "\n"))
                if line in AddDirectRules and ShowSelfDupliacteRules:
                    DDupliacte.append(("##### Count = " + str(count) + " " + templine + "\n"))
                if line in DirectRules and ShowBaseDupliacteRules:
                    DDirect.append(("##### Count = " + str(count) + " " + templine + "\n"))
                if line in ProxyRules and ShowBaseConflictRules:
                    DProxy.append(("##### Count = " + str(count) + " " + templine + "\n"))
            else:
                DWarning.append(("##### Count = " + str(count) + " " + templine + "\n"))
            #DirectRe.write(line + "\n")
    for sum in DOut:
        for record in sum:
            DirectDropped.write(record)

    PConflict = []
    PDupliacte = []
    PDirect = []
    PProxy = []
    PWarning = []
    POut = [PWarning, PConflict, PDupliacte, PDirect, PProxy]
    for line in tempProxy:
        Quanline = line
        if type == 'Q' and line.count(',') == 2 and '#' not in line:
            line = line[0:line.rfind(',')]
        if "payload:" in line or '#' in line:
            ProxyRevision.write(line + "\n")
        else:
            count = 0
            templine = "===== " + Quanline
            if line in AddDirectRules and ShowSelfConflictRules:
                count += 1
                templine = "Self-Conflict " + templine
            if line in AddProxyRules and ShowSelfDupliacteRules:
                count += 1
                templine = "Self-Dupliacte " + templine
            if line in DirectRules and ShowBaseConflictRules:
                count += 1
                templine = "Base-Conflict " + templine
            if line in ProxyRules and ShowBaseDupliacteRules:
                count += 1
                templine = "Base-Dupliacte " + templine
            if count == 0:
                AddProxyRules.append(line)
                ProxyRevision.write(Quanline + "\n")
            elif count == 1:
                if line in AddDirectRules and ShowSelfConflictRules:
                    PConflict.append(("##### Count = " + str(count) + " " + templine + "\n"))
                if line in AddProxyRules and ShowSelfDupliacteRules:
                    PDupliacte.append(("##### Count = " + str(count) + " " + templine + "\n"))
                if line in DirectRules and ShowBaseConflictRules:
                    PDirect.append(("##### Count = " + str(count) + " " + templine + "\n"))
                if line in ProxyRules and ShowBaseDupliacteRules:
                    PProxy.append(("##### Count = " + str(count) + " " + templine + "\n"))
            else:
                PWarning.append(("##### Count = " + str(count) + " " + templine + "\n"))
            #ProxyRe.write(line + "\n")
    for sum in POut:
        for record in sum:
            ProxyDropped.write(record)
    print("Done.")


if Clash:
    quchong('C')
if Quantumult:
    quchong('Q')
if Surge:
    quchong('S')