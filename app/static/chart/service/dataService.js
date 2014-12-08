angular.module('chart').factory('dataService', [
          '$state', '$resource',
  function($state, $resource) {
    /*var blah = function(d) {
      console.log(d);
      return 'a';
    }*/
    var Set = $resource('/api/u/:u/r/:r/s/:s/', { u: "@uid", r: "@rid", s: "@sid" }, {'query': {isArray: false}});
    return Set;
}]);