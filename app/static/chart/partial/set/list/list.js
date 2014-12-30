angular.module('chart').controller( 'SetListCtrl', [
          '$scope', 'model',
  function($scope, model) {
    var z = model.Record.get({ u: 'foo', r: 1 });
    $scope.test = z;
    window.a = z;
}]);