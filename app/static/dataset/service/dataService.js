angular.module('dataset').factory('dataService', [
          '$state', '$resource',
  function($state, $resource) {
    /*var blah = function(d) {
      console.log(d);
      return 'a';
    }*/
    var Record = $resource('/api/u/:u/r/:r/', { u: "@uid", r: "@rid" }, {'query': {isArray: false}});
    return Record;
}]);