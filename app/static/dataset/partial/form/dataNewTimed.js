angular.module('dataset').controller( 'DataNewCtrl', [
          '$scope',
  function($scope) {
    $scope.form_data = {};

    $scope.type = 'value';

    $scope.record_data = function() {
      $scope.$parent.record_data($scope.form_data);
    };


  }
]);