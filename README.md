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
