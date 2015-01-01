angular.module('dataset').controller( 'DatasetListCtrl', [
          '$scope', 'model',
  function($scope, model) {
    $scope.datasets = model.Dataset.query();
}]);