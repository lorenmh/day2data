angular.module('app').controller('HomeCtrl', [
          '$scope', 'api', 'path',
  function($scope, api, path){
    $scope.test = "World";
    api.get(path.api.build({ user: 'foo', record: 1, set: 1})).success(function(d) {
      console.log(d);
      $scope.test = d;
    });
}]);