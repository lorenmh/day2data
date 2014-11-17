angular.module('user').factory('userService', ['api',
  function(api) {
    var user = {};
    var observers = [];

    user.login_errors = null;
    user.id = null;

    user.observer = function(cb) {
      observers.push(cb);
    };

    var notify = function() {
      angular.forEach(observers, function(cb) {
        cb();
      });
    };

    var set_id = function(id) {
      user.id = id;
      notify();
    };

    var set_login_errors = function(e) {
      user.login_errors = e;
      notify();
    };

    user.logout = function() {
      api.logout();
      set_id(null);
    };

    user.login = function(id, password) {
      api.login(id, password)
        .success(function(d) {
          user.init(d);
        })
        .error(function(d) {
          set_login_errors(d.errors);
        });
    };

    user.init = function(obj) {
      if (obj) {
        set_id(obj.user.id);
      }
    };

    return user;
}]);