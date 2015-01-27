angular.module('app').directive('ioTextInput', function() {
  return {
    restrict: 'E',
    scope: {
      inputValue: '=ngModel'
    },
    replace: true,
    template: 
      '<div class="io-input-wrap">' +
        '<label class="io-input-label">' +
          '<span class="io-input-label-text">{{ label }}:' +
            '<span class="{{ requiredClass() }}">{{ requiredText() }}</span>' +
          '</span>' +
          '<input class="io-input" type="text" ng-model="inputValue" placeholder="{{ placeholder }}"/>' +
        '</label>' +
      '</div>',
    link: function(scope, el, attr) {
      scope.label = attr.label;
      scope.placeholder = attr.placeholder || '';
      scope.required = attr.required !== undefined;

      scope.requiredClass = function requiredClass() {
        return "io-input-" + (scope.required ? 'required' : 'optional')
      };

      scope.requiredText = function requiredText() {
        return (scope.required ? '*' : '(optional)');
      }
    }
  };
});