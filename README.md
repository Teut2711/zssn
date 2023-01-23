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
*GET*  - Perform trading
