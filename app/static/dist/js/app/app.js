angular.module('app', ['ui.router', 'user']);

angular.module('app').constant('path', {
  app_root: "/static/",
  api: "/api/",
  join: function(base_path, sub_path) {
    if (sub_path.charAt(0) === "/") {
      return base_path + sub_path.slice(1);
    } else {
      return base_path + sub_path;
    }
  },
  join_root: function(sub_path) {
    return this.join(this.app_root, sub_path);
  },
  join_api: function(sub_path) {
    return this.join(this.api, sub_path);
  }
});

angular.module('app').config(['$stateProvider', '$urlRouterProvider', 'path',
  function($stateProvider, $urlRouterProvider, path) {
    $stateProvider
      .state('root', {
        resolve: {
          init: function(api) {
            api.get('u/foo/').success(function(d){ console.log(d); });
          }
        },
        url: '',
        templateUrl: path.join_root('partial/root/root.html')
      })
      .state('root.home', {
        url: '/',
        templateUrl: path.join_root('partial/home/home.html')
      })
      .state('root.user-info', {
        url: '/user',
        templateUrl: path.join_root('user/partial/user-info/user-info.html') 
      });
    $urlRouterProvider.otherwise('/');
}]);
angular.module('app').factory('api', ['$http', 'path', function($http, path) {
  var api = {};

  api.get = function(sub_uri) {
    return $http.get(path.join_api(sub_uri));
  };

  return api;
}]);
angular.module('app').controller('RootCtrl', ['$scope', function($scope){
  $scope.world = "World";
}]);
angular.module('app').controller('HomeCtrl', ['$scope', 'api', function($scope, api){
  $scope.world = "World";
  api.get('u/foo/').success(function(d) {
    $scope.world = d;
  });
}]);
angular.module('user', ['ui.router']);

/*angular.module('user').config(function($stateProvider) {
  $stateProvider.state('user-info', {
    url: "/user",
    templateUrl: '/static/user/partial/user-info/user-info.html'
  });
});*/
angular.module('user').controller('UserInfoCtrl', function($scope) {
  $scope.user = "some user info var";
});
angular.module('user').controller('UserPanelCtrl', function($scope) {
  $scope.user = "some user panel var";
});