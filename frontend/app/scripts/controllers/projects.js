'use strict';

angular.module('codeReviewApp.controllers')
.controller('ProjectsCtrl', ['$scope', '$location', 'Restangular',
function ($scope, $location, Restangular) {
      $scope.$root.hideHeader = false;
   	$scope.projects = undefined;

      // Asynchronously get data from the server
      Restangular.all('projects').getList().then(function(data) {
         $scope.projects = data;
      })

   	$scope.goToProject = function (project) {
   		console.log("i'm going to project", project.id)
   		$location.path('/projects/' + project.id);
   	};

      $scope.gotProjectName = function (project) {
         console.log("i'm going to project", project.id)
         $location.path('/projects/' + project.id);
      };
  }]);
