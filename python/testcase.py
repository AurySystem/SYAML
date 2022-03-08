import syaml

testcase = """---
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
...
"""
a = syaml.load(testcase)
print(a)
depth = 12
def recurse(dict):
	global depth 
	depth -= 1 #will this be a problem?
	bleh = {}
	if depth == 0:
		return
	dict.update({"keys":recurse(bleh)})
	return dict
#a[0] = recurse(a[0])
b = syaml.dump(2,a)
print(b)
print(syaml.load(b))