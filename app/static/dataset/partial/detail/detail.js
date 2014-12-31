angular.module('dataset').controller( 'DatasetDetailCtrl', [
          '$scope', '$stateParams',
  function($scope, $stateParams) {
    alert('here');
    $scope.test = $stateParams.dataset_id;
}]);