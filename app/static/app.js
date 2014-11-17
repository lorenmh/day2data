angular.module('app', ['ui.router', 'user']);

angular.module('app').constant('path', {
  app_root: "/static/",
  api: "/api/",
  uri: {
    init: "init"
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
  },
  init: function() {
    return this.join(this.api, this.uri.init);
  }
});

angular.module('app').config(['$stateProvider', '$urlRouterProvider', 'path',
  function($stateProvider, $urlRouterProvider, path) {
    $stateProvider
      .state('root', {
        resolve: {
          init: function(api) {
            api.init().success(function(d){ console.log("intialize"); console.log(d); });
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