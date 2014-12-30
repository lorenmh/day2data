angular.module('app').factory('model', [
          '$state', '$resource',
  function($state, $resource) {
    /*var blah = function(d) {
      console.log(d);
      return 'a';
    }*/
    var model = {};

    model.User = $resource('/api/u/:u/', { u: "@uid", r: "@rid", s: "@sid" }, {'query': {isArray: false}});

    model.Record = $resource('/api/u/:u/r/:r/', { u: "@uid", r: "@rid" }, {'query': {isArray: true}});

    model.Set = $resource('/api/u/:u/r/:r/s/:s/', { u: "@uid", r: "@rid", s: "@sid" }, {'query': {isArray: false}});

    return model;
}]);