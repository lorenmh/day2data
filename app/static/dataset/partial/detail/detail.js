angular.module('dataset').controller( 'DatasetDetailCtrl', [
          '$scope', '$stateParams', 'model', 'd3',
  function($scope, $stateParams, model, d3) {
    
    var dataset_id = $stateParams.dataset_id;

    $scope.dataset = model.Dataset.get({ dataset_id: dataset_id });

    console.log(model);

    $scope.record_data = function(form_data, cb) {
      var new_data, v;

      new_data = new model.Data({ dataset_id: dataset_id });

      form_data = { value: Math.random() * 20 }

      for (v in form_data) {
        if (form_data.hasOwnProperty(v)) {
          new_data[v] = form_data[v];
        }
      }

      new_data.$save()
          .then( function(d) {
            console.log('handle success');
            $scope.dataset.data.push( d );
          })
          .catch( function(d) {
            console.log('handle error');
            console.log(d);
          })
      ;

    };

    $scope.dataset.$promise.then(function(dataset) {
      var svg, width, height, x, y, xAxis, yAxis, line, parse_timestamp, data;
      svg = d3.select("svg.ds-view");

      width = + svg.attr('width');
      height = + svg.attr('height');

      if (dataset.data_type === 'count') {
        x = d3.time.scale().range([ 0, width ]);
        y = d3.scale.linear().range([ height, 0 ]);

        xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        line = d3.svg.line()
            .x(function(d) { return x(d.time); })
            .y(function(d) { return y(d.id); });

        parse_timestamp = function(d) {
          return new Date(d);
        };

        data = dataset.data;

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
        } else if (dataset.data_type === 'value') {
          x = d3.time.scale().range([ 0, width ]);
          y = d3.scale.linear().range([ height, 0 ]);

          xAxis = d3.svg.axis()
              .scale(x)
              .orient("bottom");

          yAxis = d3.svg.axis()
              .scale(y)
              .orient("left");

          line = d3.svg.line()
              .x(function(d) { return x(d.time); })
              .y(function(d) { return y(d.value); });

          parse_timestamp = function(d) {
            return new Date(d);
          };

          data = dataset.data;

          data.forEach(function(d) {
            d.timestamp = parse_timestamp(d.time);
          });

          x.domain(d3.extent(data, function(d) { return d.time; }));
          y.domain(d3.extent(data, function(d) { return d.value; }));

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
        }

    });
  }
]);