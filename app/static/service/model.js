angular.module('app').factory('model', [
          '$state', '$resource',
  function($state, $resource) {
    /*var blah = function(d) {
      console.log(d);
      return 'a';
    }*/
    var model = {};

    model.User = $resource('/api/u/:u/', { u: "@uid", r: "@rid", s: "@sid" }, {'query': {isArray: false}});

    model.Dataset = $resource('/api/s/:dataset_id', { dataset_id: "@dataset_id" });

    return model;
}]);