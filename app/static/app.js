angular.module('app', ['ui.router', 'user', 'chart']);

angular.module('app').constant('path', 
(function() {
  var path = {
    root: "/static/",
    api: {
      root: "/api/",
      sub: {
        init:   "init",
        login:  "login",
        logout: "logout",
        user: "u",
        record: "r",
        set: "s",
        data: "d"
      },
      uri: {
        user: function(id) {
          return path.api.sub.user + '/' + (id !== undefined ? id + '/' : '');
        },
        record: function(id) {
          return path.api.sub.record + '/' + (id !== undefined ? id + '/' : '');
        },
        set: function(id) {
          return path.api.sub.set + '/' + (id !== undefined ? id + '/' : '');
        },
        data: function(id) {
          return path.api.sub.data + '/' + (id !== undefined ? id + '/' : '');
        },
      },
      route: {
        init:   function() { return path.api.join_root(path.api.sub.init); },
        login:  function() { return path.api.join_root(path.api.sub.login); },
        logout: function() { return path.api.join_root(path.api.sub.logout); },
        user: function(id) { return path.api.join_root(path.api.uri.user(id)); }
      },
      build: function(args) {
        var sub_paths = [];
        if (args.user !== undefined) {
          sub_paths.push(path.api.uri.user(args.user));
          if (args.record !== undefined) {
            sub_paths.push(path.api.uri.record(args.record));
            if (args.set !== undefined) {
              sub_paths.push(path.api.uri.set(args.set));
              if (args.data !== undefined) {
                sub_paths.push(path.api.uri.data(args.data));
              }
            }
          }
        }
        return path.api.join_paths_root(sub_paths);
      },
      join_root: function(sub_path) {
        return path.join(path.api.root, sub_path);
      },
      join_paths_root: function(sub_paths) {
        return path.api.join_root(sub_paths.join(''));
      }
    },
    uri: {
      home:   "/"
    },
    login_redirect:  "root.dash",
    logout_redirect: "root.home",
    links: {
      default: [
        //{ name: "Home",         route: "root.home" }
      ],
      user: [
        { name: "Dashboard",    route: "root.dash" },
        { name: "Data",      route: "root.set" },
        { name: "Records",   route: "root.record" },
        { name: "Settings",     route: "root.settings" }
      ]
    },
    join: function(base_path, sub_path) {
      if (sub_path.charAt(0) === "/") {
        if (sub_path.charAt(sub_path.length - 1) === "/") {
          return base_path + sub_path.slice(1);
        } else {
          return base_path + sub_path.slice(1) + "/";
        }
      } else {
        if (sub_path.charAt(sub_path.length - 1) === "/") {
          return base_path + sub_path;
        } else {
          return base_path + sub_path + "/";
        }
      }
    },
    join_root: function(sub_path) {
      return path.join(path.root, sub_path);
    }
  };
  window.test = path;
  return path;
}()));

angular.module('app').config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

// angular ui routing via stateProvider
// the root state is a parent route such that all routes can be children of it
// data will hold additional info about that state
// data.auth will hold authorization required to view certain paths
angular.module('app').config(
  ['$stateProvider', '$urlRouterProvider', '$locationProvider', 'path',
  function($stateProvider, $urlRouterProvider, $locationProvider, path) {
    
    $locationProvider.html5Mode(true);

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
        templateUrl: path.join_root('partial/dash/dash.html'),
        data: { auth: 'User' }
      })
      .state('root.settings', {
        url: '/settings',
        templateUrl: path.join_root('user/partial/settings/settings.html'),
        data: { auth: 'User' }
      })
      .state('root.set', {
        url: '/sets',
        templateUrl: path.join_root('chart/partial/set/list/list.html'),
        data: { auth: 'User' }
      })
      .state('root.record', {
        url: '/records',
        templateUrl: path.join_root('chart/partial/record/list/list.html'),
        data: { auth: 'User' }
      });
    $urlRouterProvider.otherwise('/');
}]);

// check authorization states and redirect if authorizations not met
angular.module('app').run(
  ['$rootScope', '$state', 'userService', 
  function($rootScope, $state, userService){
    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
      if ( toState.data.auth === 'User' && !userService.is_logged_in() ) {
        event.preventDefault();
        $state.go('root.home');
      }
    });
}]);