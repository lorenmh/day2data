angular.module('chart').controller( 'RecordListCtrl', [
          '$scope', 'model',
  function($scope, model) {
    var z = model.Record.query({ u: 'foo' });
    $scope.test = z;
    window.a = z;
}]);