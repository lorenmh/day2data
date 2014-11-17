angular.module('app').factory('api', ['$http', 'path', function($http, path) {
  var api = {};

  api.get = function(sub_uri) {
    return $http.get(path.join_api(sub_uri));
  };

  return api;
}]);