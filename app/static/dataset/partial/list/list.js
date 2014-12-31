angular.module('dataset').controller( 'SetListCtrl', [
          '$scope', 'model',
  function($scope, model) {
    var z = model.Record.get({ u: 'foo' });
    $scope.test = z;
    window.a = z;
}]);