angular.module('dataset').controller( 'DatasetListCtrl', [
          '$scope', 'model',
  function($scope, model) {
    $scope.datasets = model.Dataset.query();

    $scope.dataset_new = function(form_data, cb) {
      var new_dataset, v;

      form_data = { title: 'foo bizzar', data_type: 2 };

      new_dataset = new model.Dataset();

      for (v in form_data) {
        if (form_data.hasOwnProperty(v)) {
          new_dataset[v] = form_data[v];
        }
      }

      new_dataset.$save()
        .then( function(d) {
            console.log(d);
            console.log('handle success');
            $scope.datasets.push( d.message );
          })
        .catch( function(d) {
            console.log('handle error');
            console.log(d);
          })
      ;

    };

}]);