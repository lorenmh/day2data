angular.module('app', ['ui.router', 'user']);

angular.module('app').constant('path', {
  app_root: "/static/",
  api:      "/api/",
  uri: {
    home:   "/",
    init:   "init",
    login:  "login",
    logout: "logout"
  },
  login_redirect:  "root.dash",
  logout_redirect: "root.home",
  links: {
    default: [
      { name: "Home",         route: "root.home" }
    ],
    user: [
      { name: "Dashboard",    route: "root.dash" },
      { name: "My Charts",    route: "root.chart" },
      { name: "My Records",   route: "root.record" },
      { name: "Settings",     route: "root.settings" }
    ]
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

// angular ui routing via stateProvider
// the root state is a parent route such that all routes can be children of it
// data will hold additional info about that state
// data.auth will hold authorization required to view certain paths
angular.module('app').config(['$stateProvider', '$urlRouterProvider', 'path',
  function($stateProvider, $urlRouterProvider, path) {
    $stateProvider
      .state('root', {
        resolve: {
          init: function(api, userService) {
            api.init().success(function(res) {
              if (res) {
                userService.init(res);
              }
            });
          }
        },
        url: '',
        templateUrl: path.join_root('partial/root/root.html'),
        data: {}
      })
      .state('root.home', {
        url: '/',
        templateUrl: path.join_root('partial/home/home.html'),
        data: {}
      })
      .state('root.dash', {
        url: '/dashboard',
        templateUrl: path.join_root('partial/home/home.html'),
        data: { auth: 'User' }
      })
      .state('root.settings', {
        url: '/settings',
        templateUrl: path.join_root('user/partial/settings/settings.html'),
        data: { auth: 'User' }
      })
      .state('root.chart', {
        url: '/charts',
        templateUrl: path.join_root('partial/home/home.html'),
        data: { auth: 'User' }
      })
      .state('root.record', {
        url: '/records',
        templateUrl: path.join_root('partial/home/home.html'),
        data: { auth: 'User' }
      });
    $urlRouterProvider.otherwise('/');
}]);

// check authorization states and redirect if authorizations not met
angular.module('app').run(['$rootScope', '$state', 'userService', 
  function($rootScope, $state, userService){
    console.log('c');
    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
      if ( toState.data.auth === 'User' && !userService.is_logged_in() ) {
        event.preventDefault();
        $state.go('root.home');
      }
    });
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
angular.module('user').controller('SettingsCtrl', function($scope) {
  $scope.user = "some user info var";
});
angular.module('user').controller('UserPanelCtrl', [
  '$scope',
  'userService',
  function($scope, userService) {
    $scope.id = userService.id;
    $scope.login_errors = userService.login_errors;
    $scope.login_form = false;

    userService.observe_error(function() {
      $scope.login_errors = userService.login_errors;
    });

    userService.observe_login(function() {
      $scope.id = userService.id;
      $scope.login_form = false;
    });

    $scope.toggle_login_form = function() {
      $scope.login_form = !$scope.login_form;
    };

    $scope.submit = function() {
      var user = document.getElementById('username-input');
      var password = document.getElementById('password-input');
      userService.login(user.value, password.value);
    };

    $scope.logout = function() {
      userService.logout();
    };
}]);
angular.module('app').controller('SidebarCtrl', ['$scope', 'path', 'userService', function($scope, path, userService){
  var user_links;

  var set_default_and_user_links = function() {
    $scope.links = path.links.default.concat( path.links.user );
    user_links = true;
  };

  var set_default_links = function() {
    $scope.links = path.links.default;
    user_links = false;
  };

  userService.observe_login( function() {
    if ( !user_links ) {
      set_default_and_user_links();
    }
  });

  userService.observe_logout( function() {
    if ( user_links ) {
      set_default_links();
    }
  });

  if (userService.is_logged_in()) {
    set_default_and_user_links();
  } else {
    set_default_links();
  }

}]);
angular.module('user').factory('userService', ['$state', 'path', 'api',
  function($state, path, api) {
    var user = {};
    var logged_in = false;
    var login_observers = [];
    var logout_observers = [];
    var error_observers = [];

    user.login_errors = null;
    user.id = null;

    user.observe_error = function(cb) {
      error_observers.push(cb);
    };

    user.observe_login = function(cb) {
      login_observers.push(cb);
    };

    user.observe_logout = function(cb) {
      logout_observers.push(cb);
    };

    var notify_login = function() {
      angular.forEach(login_observers, function(cb) {
        cb();
      });
    };

    var notify_logout = function() {
      angular.forEach(logout_observers, function(cb) {
        cb();
      });
    };

    var notify_error = function() {
      angular.forEach(error_observers, function(cb) {
        cb();
      });
    };

    var set_id = function(id) {
      user.id = id;
      logged_in = true;
      notify_login();
    };

    var set_login_errors = function(d) {
      user.login_errors = d.error;
      notify_error();
    };

    user.logout = function() {
      api.logout()
        .success(function() {
          set_id(null);
          logged_in = false;
          notify_logout();
          $state.go(path.logout_redirect);
        });
    };

    user.login = function(id, password) {
      api.login(id, password)
        .success(function(d) {
          user.init(d);
          $state.go(path.login_redirect);
        })
        .error(function(d) {
          set_login_errors(d);
        });
    };

    user.init = function(obj) {
      if (obj) {
        set_id(obj.user.id);
      }
    };

    user.is_logged_in = function() {
      return logged_in;
    };

    return user;
}]);