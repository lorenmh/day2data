App to store personal data, so a user can keep track of their progress over time.  Will be displayed using some form of data library (d3?)

Notes:  
Make sure to call create() instead of save() for first save of a Model.
create() creates a unique resource id (res_id) which should only be done once.
this res_id is going to be used so that resource ids will be relative.  
For example:  
  /user/jimbob/valueset/1/1 would correspond to the first data point in the first valueset for user jimbob.  
  /user/ricky/valueset/1/1 would correspond to the first data point in the first valueset for user ricky.  

the Alternative would be to not use these relative resource ids, which would look more like this:  
  /user/jimbob/valueset/42/14252  
    or  
  /user/ricky/valueset/49/14976  

This way we know we are dealing with jimbob's or ricky's resources and not using some global id

#Update 10/30
##Record
So a record will now hold value sets.  This way we can have a single record which tracks different sets.  For example, I might have a 'Losing Weight' record.  Inside this record I might have different data sets, like one tracking my current weight, another tracking my jogging times, jogging distances, etc.

#Info about the schemas used
##Data
Corresponds to a 'data point'.  
Comprises: ValueData, CountData, TimedData  
*Note about TimedData* TimedData holds two 'TimePoints'.  This is so that each TimedData can hold a start and a stop time (ie, a jog time has a start point and an end point)
##Sets
Corresponds to a 'set of data points'  
Comprises: ValueSet, CountSet, TimedSet  
##Records
Corresponds to a 'record of data sets'.  This is really so that people can track multiple sets within one 'space' (ie, record).  They can then view or share these records.  Permissions will be tied to the record, depending on how the user sets it up.  
Comprises: Record  

#Update 10/31
##Timelines
###Release 1
Will have all basic functionality; User can create and view data sets and records.  Will be able to add text, etc.
###Release 2
User will be able to make each record private / public, (private default)
###ChoiceSet
Add a ChoiceSet with ChoiceData and a Choice table (with res\_ids), where only one of a certain set of choices can be selected.  Ex: 'Green', 'Yellow', 'Red'.  A person could record which color of stoplight they encounter while driving (stupid example, but it gets the point across).  This would allow data to be displayed in pie charts.

#update 11/23
move partials over to directives:  
*login form
*user status
*menu
*navbar  

  start thinking of how to put together a d3 / chart directive
