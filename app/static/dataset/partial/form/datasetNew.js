angular.module('dataset').controller( 'DatasetNewCtrl', [
          '$scope',
  function($scope) {
    $scope.form_data = {};

    $scope.dataset_new = function() {
      $scope.$parent.dataset_new($scope.form_data);
    };
  }
]);