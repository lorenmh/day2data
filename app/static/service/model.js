angular.module('app').factory('model', [
          '$state', '$resource',
  function($state, $resource, $api) {
    /*var blah = function(d) {
      console.log(d);
      return 'a';
    }*/
    var model = {};

    model.User = $resource('/api/u/:u/', { u: "@uid", r: "@rid", s: "@sid" }, {'query': {isArray: false}});

    model.Dataset = $resource('/api/s/:dataset_id', { dataset_id: "@dataset_id" });

    model.Data = $resource (
      '/api/s/:dataset_id/d/:data_id',
      { 
        dataset_id: "@dataset_id",
        data_id: "@data_id" 
      }
    );

    return model;
}]);