angular.module('app').controller('SidebarCtrl', [
          '$scope', 'path', 'userService',
  function($scope, path, userService){
    var user_links;

    var set_default_and_user_links = function() {
      $scope.links = path.links.default.concat( path.links.user );
      user_links = true;
    };

    var set_default_links = function() {
      $scope.links = path.links.default;
      user_links = false;
    };

    userService.observe_login( function() {
      if ( !user_links ) {
        set_default_and_user_links();
      }
    });

    userService.observe_logout( function() {
      if ( user_links ) {
        set_default_links();
      }
    });

    if (userService.is_logged_in()) {
      set_default_and_user_links();
    } else {
      set_default_links();
    }

}]);