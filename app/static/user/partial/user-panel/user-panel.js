angular.module('user').controller('UserPanelCtrl', [
          '$scope', 'userService',
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
      console.log(this);
      var user = document.getElementById('username-input');
      var password = document.getElementById('password-input');
      userService.login(user.value, password.value);
    };

    $scope.logout = function() {
      userService.logout();
    };
}]);