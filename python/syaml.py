import re
import json


def load(string):
    yaml = re.split('\r\n|\n', string)
    out = []  # list of dicts
    doc = -1
    pobj = -1
    line = 0
    spSize = -1
    indents = 0
    listNest = 0

    def spaceCount(lin):
        spCnt = 0
        if (lin >= len(yaml)):
            return -1
        while (yaml[lin][spCnt] == " "): 
            spCnt += 1
        return spCnt

    def processLine(string):  # top level
        if( string.find(":") != -1 ):
            temp = re.split(': |:$', string)
            temp = [temp.pop(0), ": ".join(temp)]
            out[doc].update({processKey(temp[0]): processIndents(temp[1],False)})

    def processValue(string):  # post indent step
        out = string
        out = re.sub('- *', "", out)
        if(out.startswith("\"")):
            out = out[out.find("\"")+1: out.rfind("\"")]
        elif(out.startswith("[")):
            out = json.loads(out[out.find("["): out.rfind("]")+1])
        elif(out.startswith("{")):
            out = json.loads(out[out.find("{"): out.rfind("}")+1])
        elif(out.find(" # ") != -1):
            out = out[:out.find(" # ")]  # todo flow and numbers
        return out


    def processKey(string) : #strip quotes
        out = string
        if(out.startswith("- ")):
            out = out[2:]        
        if(out.startswith("\"")):
            out = out[int(out.find("\"")+1): int(out.rfind("\""))]
        
        return out
    

    def processIndents (string, prvary) :
        nonlocal line
        nonlocal spSize
        nonlocal indents
        nonlocal listNest
        curline = yaml[line]
        if (string.replace(" ", "") == "") :
            line += 1
            curline = yaml[line]
            if (spSize == -1 and curline.startswith(" ")) :
                spSize = spaceCount(line)
            arraycheck = False
            arrayI = -1
            proc = {}
            listdrecmented = False
            noindent = prvary and yaml[line][(indents * spSize + listNest * 2):].startswith("- ")
            if (not noindent):
                indents += 1
            curSpaces = spaceCount(line)
            
            while curSpaces - (indents * spSize + listNest * 2) == 0:
                curline = yaml[line]
                curline = curline[curSpaces:]
                if (curline.startswith("- ")):
                    if (not arraycheck):
                        proc = []
                        arraycheck = True
                    listNest += 1
                    arrayI += 1
                
                nextline = yaml[line + 1] if line + 1 < len(yaml) else ""
                nextSpcs = spaceCount(line + 1)

                if (nextline[(indents * spSize + (listNest - 1) * 2):].startswith("- ") or (nextSpcs != spaceCount(line) and (nextSpcs <= (indents * spSize + (listNest - 1) * 2)) and arraycheck)):
                    listNest -= 1
                    listdrecmented = True
                
                if (curline.find(":") == -1 and arraycheck):
                    proc.insert(arrayI, processValue(curline))
                else :
                    temp = re.split(': |:$', curline)
                    temp = [temp.pop(0), ': '.join(temp)]
                    if (arraycheck):
                        if (arrayI >= len(proc)):
                            proc.insert(arrayI, {})
                        proc[arrayI].update({processKey(temp[0]): processIndents(temp[1], True)})
                    else :
                        proc.update({processKey(temp[0]): processIndents(temp[1], False)})
                    
                line += 1
                curSpaces = spaceCount(line)
                if(yaml[line].replace(" ","").startswith("#")):
                    line += 1
                    curSpaces = spaceCount(line)
                
            line -= 1
            if (not noindent):
                if (arraycheck):
                    listNest -= 1
                indents -= 1
            else: 
                listNest -= 1
            return proc
        return processValue(string)

    

    while (line < len(yaml)) :
        if (line == 0 or yaml[line].startswith("---")) :
            pobj += 1
            doc = pobj
            out.insert(doc,{})
            indents = 0
            listNest = 0
        elif (yaml[line].startswith("...")) :
            doc = -1
        else :
            if doc != -1:
                processLine(yaml[line])
        line += 1
    return out

def dump(spacesize, dicts):
    out = ""
    line = 0
    indents = 0
    listNest = 0
    
    def unRoll(value, listabove = False, firstdictIndent = False):
        out = ""
        nonlocal spacesize
        nonlocal line
        nonlocal indents
        nonlocal listNest
        
        if isinstance(value, list):
            if listabove:
                out += json.dumps(value) + "\n" #todo replace with flow controler
            else:
                if not firstdictIndent:
                    indents += 1
                indstr = " " * (spacesize * indents + 2 * listNest)
                out += "\n"
                for entry in value:
                    out += indstr + "- "
                    out += unRoll(entry, True)
                if not firstdictIndent:
                    indents -= 1
        elif isinstance(value, dict):
            if listabove:
                listNest += 1
            else:
                out += "\n"
                indents += 1
            first = True
            indstr = " " * (spacesize * indents + 2 * listNest)
            for key, entry in value.items():
                out += ("" if (first and listabove) else indstr) + key +": "
                out += unRoll(entry, False, listabove and first)
                first = False
            if listabove:
                listNest -= 1
            else:
                indents -= 1
        elif isinstance(value, str):
            if re.search('{|}|[|]|#',value) != None:
                out += "\"" + value + "\"\n" # todo auto add quotes?
            else:
                out += value + "\n" # todo auto add quotes?
        else:
            out += str(value) + "\n"
        
        return out
    
    for doc in dicts:
        out += "---\n"
        for key, entry in doc.items():
            out += key +": "
            out += unRoll(entry)
    
    return out


def dumps(spacesize, *dicts):
    dump(spacesize, dicts)
