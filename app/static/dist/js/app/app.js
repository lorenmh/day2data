angular.module('app', ['ui.router', 'user']);

angular.module('app').constant('path', {
  app_root: "/static/",
  api:      "/api/",
  uri: {
    init:   "init",
    login:  "login",
    logout: "logout"
  },
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
          init: function(api, userService) {
            api.init().success(function(res){
              if (res) {
                userService.init(res);
              }
            });
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
angular.module('user').controller('UserPanelCtrl', [
  '$scope',
  'userService',
  function($scope, userService) {
    $scope.id = userService.id;
    $scope.login_errors = userService.login_errors;
    
    var user_cb = function() {
      $scope.id = userService.id;
      $scope.login_errors = userService.login_errors;
    };
    userService.observer(user_cb);

    $scope.show_login = function() {
      userService.login('foo', 'pswd');
    };

    $scope.logout = function() {
      userService.logout();
    };
}]);
angular.module('user').factory('userService', ['api',
  function(api) {
    var user = {};
    var observers = [];

    user.login_errors = null;
    user.id = null;

    user.observer = function(cb) {
      observers.push(cb);
    };

    var notify = function() {
      angular.forEach(observers, function(cb) {
        cb();
      });
    };

    var set_id = function(id) {
      user.id = id;
      notify();
    };

    var set_login_errors = function(e) {
      user.login_errors = e;
      notify();
    };

    user.logout = function() {
      api.logout();
      set_id(null);
    };

    user.login = function(id, password) {
      api.login(id, password)
        .success(function(d) {
          user.init(d);
        })
        .error(function(d) {
          set_login_errors(d.errors);
        });
    };

    user.init = function(obj) {
      if (obj) {
        set_id(obj.user.id);
      }
    };

    return user;
}]);