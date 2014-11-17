angular.module('user').controller('UserPanelCtrl', [
  '$scope',
  'userService',
  function($scope, userService) {
    $scope.id = userService.id;
    
    var id_cb = function(new_id) {
      $scope.id = new_id;
    };
    userService.observer(id_cb);


}]);