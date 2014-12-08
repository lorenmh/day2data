angular.module('chart').controller( 'ChartListCtrl', [
          '$scope', 'dataService',
  function($scope, dataService) {
    var z = dataService.query({ u: 'foo', r: 1, s: 1 });
    $scope.test = z;
    window.a = z;
}]);