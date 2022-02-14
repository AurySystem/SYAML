
testyaml = `---
key:
  key: f
  key2: l
  nest:
    inner: g
    nest2:
      nestted: 3
    inner2: s
  outnest: 3
ha: g
je: r
---
key: value
a_list:
  - itema
  - listlist:
    - itemitem
  - itemb
  - key1: bweh
    key2: bweh
    key3: bweh
    key4: bweh
  - innerList:
    - innerItem
    - indict: reh
      rar: dd
      sublist:
        - iteml
        - itemc
        - 
        - itm
        - [44,55,66,"7t","8t","eeee"]
        - ohno
        - "test"
        - "ending": obj
          key: last of inner
    - aa: aaa
  - lastitem
anotherkey: value
...`

function yaml(string) {
    let input = string.split(/\r\n|\n/);
    let out = []; // array of objects
    let object = -1;
    let pobj = -1;
    let line = 0;
    let spSize = -1;
    let indents = 0;
    let listNest = 0;

    out[object] = {};


    let spaceCount = function (lin) {
        let spCnt = 0;
        if (input[lin] == undefined) return -1;
        while (input[lin].charAt(spCnt) === " ") spCnt++;
        return spCnt
    }

    let processLine = function (string) {//top level
        if(string.includes(":")){
            let temp = string.split(/\: |:$/)
            temp = [temp.shift(), temp.join(': ')];
            out[object][processKey(temp[0])] = processIndents(temp[1])
        }
    }

    let processValue = function (string) {//post indent step
        let out = string;
        out = out.replace(/- */, "");
        if(out.startsWith("\"")){
            out = out.substring(out.indexOf("\"")+1, out.lastIndexOf("\""));
        }else if(out.startsWith("[")){
            out = JSON.parse(out.substring(out.indexOf("["), out.lastIndexOf("]")+1))
        }
        return out;
    }

    let processKey = function (string) { //strip quotes
        let out = string;
        console.log(out);
        if(out.startsWith("- ")){
            out = out.substring(2);
        }
        if(out.startsWith("\"")){
            out = out.substring(out.indexOf("\"")+1, out.lastIndexOf("\""));
        }
        return out;
    }

    let processIndents = function (string, prvary) {

        let curline = input[line];
        if (string.replace(" ", "") === "") {
            console.log("aaaa")
            line++
            curline = input[line];
            if (spSize == -1 && curline.charAt(0) === " ") {
                spSize = spaceCount(line);
            }
            let arraycheck = false;
            let arrayI = -1;
            let proc = {};
            let listdrecmented = false;
            //lists and objects here
            let noindent = prvary && input[line].substring(indents * spSize + listNest * 2).startsWith("- ");
            if (!noindent) {
                indents++;
            }
            let curSpaces = spaceCount(line);
            while (curSpaces - (indents * spSize + listNest * 2) == 0) {
                curline = input[line];
                curline = curline.substring(curSpaces);
                if (curline.startsWith("- ")) {
                    if (!arraycheck) {
                        proc = [];
                        arraycheck = true;
                    }
                    listNest++;
                    arrayI++;
                }
                let nextline = input[line + 1];
                let nextSpcs = spaceCount(line + 1);

                console.log(curline, indents, listNest, spaceCount(line), line, nextline, spaceCount(line+1));

                if (nextline.substring(indents * spSize + (listNest - 1) * 2).startsWith("- ") ||
                    (nextSpcs != spaceCount(line) && nextSpcs <= (indents * spSize + (listNest - 1) * 2) && arraycheck)) {
                    listNest--;
                    listdrecmented = true;
                }
                if (!curline.includes(":") && arraycheck) {
                    proc[arrayI] = processValue(curline);
                } else {
                    let temp = curline.split(/\: |:$/)
                    temp = [temp.shift(), temp.join(': ')];
                    if (arraycheck) {
                        if (proc[arrayI] == undefined) proc[arrayI] = {};
                        proc[arrayI][processKey(temp[0])] = processIndents(temp[1], true);
                    } else {
                        proc[processKey(temp[0])] = processIndents(temp[1], false);
                    }
                }
                line++;
                curSpaces = spaceCount(line);
                if(input[line].replace(" ","").startsWith("#")){
                    line++;
                    curSpaces = spaceCount(line);
                }
            }
            line--;
            if (!noindent) {
                if (arraycheck) listNest--;
                indents--;
            } else listNest--;
            return proc;
        }

        console.log(input[line],line)
        return processValue(string);

    }

    while (line < input.length) {
        if (line == 0 || input[line].startsWith("---")) {
            pobj++;
            object = pobj;
            out[object] = {};
            indents = 0;
            listNest = 0;
        } else if (input[line].startsWith("...")) {
            object = -1;
        } else {
            processLine(input[line]);
        }
        line++;
    }

    return out;
}

console.log(JSON.stringify(yaml(testyaml), null, 2));