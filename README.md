# zssn<br>
NonaLifestyle Assessment 

Link to the API:<br>
http://teut.pythonanywhere.com/



# Endpoints<br>
#### 1)  http://teut.pythonanywhere.com/survivors <br>
Methods :<br>
*GET*  - Get all survivors

#### 2)  http://teut.pythonanywhere.com/survivors/<survivor_id>
Methods :   
*GET*  - Get a survivor by id<br>
*POST* - Create new survivor<br>
*PUT*  - Update details of survivor<br>

*POST/PUT* body example:<br>
```json
{
  "name": "Kevin Dickerson",
  "age": 14,
  "gender": "M",
  "lat": -50.677346,
  "lon": -169.916907,
  "contamination": 3
}
```



#### 3)  http://teut.pythonanywhere.com/survivors/<survivor_id>/increase-contamination
Methods : <br>
*GET*  - Update survivor contamination reporting

#### 4)  http://teut.pythonanywhere.com/reports
Methods : <br>
*GET*  - Get report with the following data:<br>
a) Percentage of infected survivors.<br>
b) Percentage of non-infected survivors.<br>
c) Average amount of each kind of resource by survivor (e.g. 5 waters per survivor)<br>
d) Points lost because of infected survivors.<br>

#### 5)  http://teut.pythonanywhere.com/trades/<survivor_id>/
Methods : <br>
*GET*  - Get inventory of survivor by id

#### 6)  http://teut.pythonanywhere.com/trades
Methods : <br>
*POST*  - Perform trading


*POST/PUT* body format and example:<br>

###### Format:
```
{
  <survivor1_id>: {
    <resource_name> : <quantity>, 
    ...
  },
  <survivor2_id>: {
    <resource_name> : <quantity>, 
    ...
  },
  
}
```

###### Example:
```json
{
  "61c1d406-7a3d-4a2e-9573-064de5fd8c48": {
    "Water" : 2,
    "Ammunition" : 3
  },
  "9ae5a5d7-32c5-4ea1-a10e-14d3e0c08951": {
    "Water" : 2,
    "Medication" : 3
  },
  
}
```
