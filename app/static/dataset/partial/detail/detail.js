angular.module('dataset').controller( 'DatasetDetailCtrl', [
          '$scope', '$stateParams', 'model', 'd3',
  function($scope, $stateParams, model, d3) {
    
    $scope.dataset = model.Dataset.get({ dataset_id: $stateParams.dataset_id });

    console.log($scope.dataset);

    window.d3 = d3;

    $scope.dataset.$promise.then(function(dataset) {
      var svg = d3.select("svg.ds-view");

      var width = + svg.attr('width'),
          height = + svg.attr('height');

      var x = d3.time.scale().range([ 0, width ]);
      var y = d3.scale.linear().range([ height, 0 ]);

      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");

      var line = d3.svg.line()
          .x(function(d) { return x(d.time); })
          .y(function(d) { return y(d.id); });

      var parse_timestamp = function(d) {
        return new Date(d);
      };

      var data = dataset.dataset.data;

      data.forEach(function(d) {
        d.timestamp = parse_timestamp(d.time);
      });

      x.domain(d3.extent(data, function(d) { return d.time; }));
      y.domain(d3.extent(data, function(d) { return d.id; }));

      svg.append("g")
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + height + ')')
          .call(xAxis);

      svg.append("g")
          .attr('class', 'y axis')
          .call(yAxis)
        .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '.71em')
          .style('text-anchor', 'end')
          .text('Number');

      svg.append('path')
        .datum(data)
        .attr('class', 'line')
        .attr('d', line);
    });
}]);