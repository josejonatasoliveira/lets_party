angular.module("myApp", ['ngSanitize'])
  .controller("indexCtrl", function($scope) {
    $scope.events = "init";
    $.ajax({
      url: 'event_carousel', 
      success: function(data) {
        $scope.$apply(function() {
          $scope.events = data.results;
        });
      }
    })
    
  });