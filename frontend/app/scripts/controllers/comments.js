'use strict';

angular.module('codeReviewApp.controllers')
.controller('CommentsCtrl', ['$scope', '$routeParams', 'Restangular',
function ($scope, $routeParams, Restangular) {

   $scope.projectId = $routeParams.projectId;

   $scope.project = undefined;

   // Asynchronously get data from the server
   Restangular.one('projects', $scope.projectId).get().then(function(data) {
      $scope.project = data;
   })

   

}]);