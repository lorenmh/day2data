angular.module('user').controller('FormUserNewCtrl', [
          '$scope', 'api', 'userService',
  function($scope, api, userService) {
    $scope.logged_in = userService.is_logged_in();
    $scope.login_errors = userService.login_errors;
    $scope.show_form = false;

    $scope.submit = function() {

    };

    userService.observe_logged_in(function(logged_in) {
      $scope.logged_in = logged_in;
    });

    $scope.toggle_form_user_new = function() {
      $scope.show_form = !$scope.show_form;
    };

}]);