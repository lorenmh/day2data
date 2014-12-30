angular.module('user').controller('FormUserNewCtrl', [
          '$scope', 'api', 'path', 'userService',
  function($scope, api, path, userService) {
    $scope.logged_in = userService.is_logged_in();
    
    $scope.form_errors = null;
    
    $scope.show_form = false;

    $scope.form_data = {};

    var set_errors_from_obj = function(obj) {
      var errors, keys, i;
      errors = [];
      keys = Object.keys(obj);
      for (i = 0; i < keys.length; i++) {
        errors.push( obj[keys[i]] );
      }
      $scope.form_errors = errors;
    };

    $scope.submit = function() {
      api.post( path.api.route.user(), $scope.form_data )
        .success(function(res) {
          userService.init(res.message);
        })
        .error(function(res) {
          set_errors_from_obj(res.message);
        });
    };

    userService.observe_logged_in(function(logged_in) {
      $scope.logged_in = logged_in;
    });

    $scope.toggle_form = function() {
      $scope.show_form = !$scope.show_form;
      $scope.form_errors = null;
      $scope.form_data = {};
    };

}]);