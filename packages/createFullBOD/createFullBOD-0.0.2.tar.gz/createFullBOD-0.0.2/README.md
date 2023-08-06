# Create Full BOD Wrapper for Scripting

This Python package contains some functions to create a BOD wrapper after converting JSON data to XML

you can find the code to this file

```
createFullBOD.py
```

### def createRoot(root):
the root parameter should be verb+noun like SyncItemMaster.
It creates the root of the BOD

createRoot('Syncemployee')
```
<Syncemployee xmlns="http://schema.infor.com/InforOAGIS/2">
</Syncemployee>
```

### def createApplArea(lid,compId):
It creates the ApplicationArea structure proving the LogicalID and ComponentID

createApplArea('lid://infor.ln','erp')
```
    <ApplicationArea>
        <Sender>
        <LogicalID>lid://infor.ln</LogicalID>
        <ComponentID>erp</ComponentID>
        <ConfirmationCode>OnError</ConfirmationCode>
        </Sender>
        <CreationDateTime>2019-10-09T12:02:44:270Z</CreationDateTime>
        <BODID>b3c8437e-ea8c-11e9-aad9-ca7d09e7940e</BODID>
    </ApplicationArea>
```

### def createDataArea():
it creates just the DataArea tag

```
    <DataArea></DataArea>
```

### def createVerb(verb,aev,locv,aexv):
it creates the Verb structure of the BOD providing the VERB = [Sync|Process|Acknowldge|....] plus the AccountingEntity, Location and Action = [Add|Change|Replace]

createVerb('Sync','AE','000','Add')
```
    <Sync>
      <AccountingEntityID>AE</AccountingEntityID>
      <LocationID>000</LocationID>
      <ActionCriteria>
        <ActionExpression actionCode="Add" />
      </ActionCriteria>
    </Sync>
```

### def renameTag(xml, oldtag,newtag):
Giving an XML, it replaces the oldtag within the XML with the newtag

renameTag(XML,'element','employee')

From here:
```
  <element>
    <empnum>1001</empnum>
    <fullname>John Doe                                </fullname>
    <dateofhire>2009-08-28</dateofhire>
  </element>
```
To here:
```
  <employee>
    <empnum>1001</empnum>
    <fullname>John Doe                                </fullname>
    <dateofhire>2009-08-28</dateofhire>
  </employee>
```

### def createFullBOD(verb,noun,lid,erp,ae,loc,action,body):

- verb = Sync
- noun = employee
- lid  = lid://infor.ln.1
- erp = erp
- ae = AE
- loc = 000
- action = Add
- body = see below

the body parameter should be the JSON data converted in XML
if we consider as JSON this array

```
[
	{
		"empnum": 1001,
		"fullname": "John Doe                                ",
		"dateofhire": "2009-08-28"
	},
	{
		"empnum": 1002,
		"fullname": "Jane Doe                                ",
		"dateofhire": "2009-08-28"
	},
	{
		"empnum": 1003,
		"fullname": "Tim Bone                                ",
		"dateofhire": "2014-01-01"
	}
]
```

the converted XML will be like this

```
<root>
  <element>
    <empnum>1001</empnum>
    <fullname>John Doe                                </fullname>
    <dateofhire>2009-08-28</dateofhire>
  </element>
  <element>
    <empnum>1002</empnum>
    <fullname>Jane Doe                                </fullname>
    <dateofhire>2009-08-28</dateofhire>
  </element>
  <element>
    <empnum>1003</empnum>
    <fullname>Tim Bone                                </fullname>
    <dateofhire>2014-01-01</dateofhire>
  </element>
</root>
```

if the JSON data has the format as above after the convert, you can invoke the function

createFullBOD('Sync','employee','lid://infor.ln.1','erp','AE','000','Add', body)

the result will be

```
<Syncemployee 
  xmlns="http://schema.infor.com/InforOAGIS/2">
  <ApplicationArea>
    <Sender>
      <LogicalID>lid://infor.ln.1</LogicalID>
      <ComponentID>erp</ComponentID>
      <ConfirmationCode>OnError</ConfirmationCode>
    </Sender>
    <CreationDateTime>2019-10-09T12:28:50:088Z</CreationDateTime>
    <BODID>5902f98a-ea90-11e9-bfec-427e59ba50c3</BODID>
  </ApplicationArea>
  <DataArea>
    <Sync>
      <AccountingEntityID>AE</AccountingEntityID>
      <LocationID>000</LocationID>
      <ActionCriteria>
        <ActionExpression actionCode="Add" />
      </ActionCriteria>
    </Sync>
    <employee>
      <empnum>1001</empnum>
      <fullname>John Doe                                </fullname>
      <dateofhire>2009-08-28</dateofhire>
    </employee>
    <employee>
      <empnum>1002</empnum>
      <fullname>Jane Doe                                </fullname>
      <dateofhire>2009-08-28</dateofhire>
    </employee>
    <employee>
      <empnum>1003</empnum>
      <fullname>Tim Bone                                </fullname>
      <dateofhire>2014-01-01</dateofhire>
    </employee>
  </DataArea>
</Syncemployee>
```

Contact: <giampaolo.spagoni@infor.com>
