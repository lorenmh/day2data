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