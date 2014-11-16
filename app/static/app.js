angular.module('app', ['ui.router']);

var path = {
  root: "/static/",
  join_root: function(sub_path) {
    if (sub_path.charAt(0) === "/") {
      return this.root + sub_path.slice(1);
    } else {
      return this.root + sub_path;
    }
  }
};



angular.module('app').config(function($stateProvider, $urlRouterProvider) {
  $stateProvider.state('root', {
    url: '/',
    templateUrl:  path.join_root('partial/root/root.html')
  });
  $urlRouterProvider.otherwise('/');
});