angular.module('app', ['ui.router', 'user', 'chart']);

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
    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
      if ( toState.data.auth === 'User' && !userService.is_logged_in() ) {
        event.preventDefault();
        $state.go('root.home');
      }
    });
}]);