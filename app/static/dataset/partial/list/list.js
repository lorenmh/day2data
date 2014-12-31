angular.module('dataset').controller( 'DatasetListCtrl', [
          '$scope', 'model',
  function($scope, model) {
    var z = model.Dataset.query();
    $scope.test = z;
    window.a = z;
}]);