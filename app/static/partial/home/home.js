angular.module('app').controller('HomeCtrl', [
          '$scope', 'api',
  function($scope, api){
    $scope.world = "World";
    api.get('u/foo/').success(function(d) {
      $scope.world = d;
    });
}]);