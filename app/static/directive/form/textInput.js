angular.module('app').directive('ioTextInput', function() {
  return {
    restrict: 'E',
    scope: {
      ioValue: '=',
      ioError: '='
    },
    replace: true,
    template: 
      '<div class="io-input-container io-text">' +
        '<label class="io-input-label">' +
          '<span class="io-input-label-text">{{ label }}:' +
            '<span ng-if="required" class="io-input-required">*</span>' +
          '</span>' +
          '<div class="io-input-wrap">' +
            '<span ng-if="ioError" class="io-error-text">{{ ioError }}</span>' +
            '<input class="io-input"  type="text" ng-model="ioValue" ng-change="validate()" placeholder="{{ placeholder }}" />' +
          '</div>' +
        '</label>' +
      '</div>',
    link: function(scope, el, attr) {
      scope.label = attr.label;
      scope.placeholder = attr.placeholder || '';
      scope.required = attr.required !== undefined;

      scope.validate = function() {

      }
    }
  };
});

angular.module('app').directive('ioIntegerInput', function() {
  return {
    restrict: 'E',
    scope: {
      ioValue: '=',
      ioError: '='
    },
    replace: true,
    template: 
      '<div class="io-input-container io-integer">' +
        '<label class="io-input-label">' +
          '<span class="io-input-label-text">{{ label }}:' +
            '<span ng-if="required" class="io-input-required">*</span>' +
          '</span>' +
          '<div class="io-input-wrap">' +
            '<span ng-if="ioError" class="io-error-text">{{ ioError }}</span>' +
            '<input class="io-input"  type="text" ng-model="ioValue" ng-change="validate()" placeholder="{{ placeholder }}" />' +
          '</div>' +
        '</label>' +
      '</div>',
    link: function(scope, el, attr) {
      scope.label = attr.label;
      scope.placeholder = attr.placeholder || '';
      scope.required = attr.required !== undefined;

      scope.validate = function() {
        if (isNaN( +scope.ioValue )) {
          scope.ioError = 'Please enter number value.'
        } else if ( (+scope.ioValue) % 1 !== 0) {
          scope.ioError = 'Please enter a number without decimals'
        } else {
          scope.ioError = null;
        }
      }
    }
  };
});

angular.module('app').directive('ioNumberInput', function() {
  return {
    restrict: 'E',
    scope: {
      ioValue: '=',
      ioError: '='
    },
    replace: true,
    template: 
      '<div class="io-input-container io-number">' +
        '<label class="io-input-label">' +
          '<span class="io-input-label-text">{{ label }}:' +
            '<span ng-if="required" class="io-input-required">*</span>' +
          '</span>' +
          '<div class="io-input-wrap">' +
            '<span ng-if="ioError" class="io-error-text">{{ ioError }}</span>' +
            '<input class="io-input" type="text" ng-model="ioValue" ng-change="validate()" placeholder="{{ placeholder }}" />' +
          '</div>' +
        '</label>' +
      '</div>',
    link: function(scope, el, attr) {
      scope.label = attr.label;
      scope.placeholder = attr.placeholder || '';
      scope.required = attr.required !== undefined;

      scope.validate = function() {
        if (isNaN( +scope.ioValue )) {
          scope.ioError = 'Please enter number value.'
        } else {
          scope.ioError = null;
        }
      }
    }
  };
});