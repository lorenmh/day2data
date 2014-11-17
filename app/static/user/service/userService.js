angular.module('user').factory('userService', function() {
  var user = {};
  var observers = [];

  user.id = "default";

  user.observer = function(cb) {
    observers.push(cb);
  };

  var notify = function() {
    angular.forEach(observers, function(cb) {
      cb();
    });
  };

  user.set_user = function(obj) {
    if (obj) {
      user.id = obj.id;
      notify();
    }
  };

  user.init = function(obj) {
    user.set_user(obj);
  };

  return user;
});