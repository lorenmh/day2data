angular.module('app').factory('api', [
          '$http', 'path', 
  function($http, path) {
    var api = {};

    api.get = function(uri) {
      return $http.get(path.join_api(uri));
    };

    api.post = function(uri, data) {
      return $http.post(path.join_api(uri), JSON.stringify(data));
    };

    api.init = function() {
      return api.get(path.uri.init);
    };

    api.logout = function() {
      return api.get(path.uri.logout);
    };

    api.login = function(id, password) {
      return api.post(path.uri.login, {id: id, password: password});
    };

    return api;
}]);