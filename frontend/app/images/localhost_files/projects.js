'use strict';

angular.module('codeReviewApp.controllers')
.controller('ProjectsCtrl', ['$scope', '$location',
function ($scope, $location) {
      $scope.$root.hideHeader = false;
	
   	$scope.projects = [
   		{
   			id: 1,
   			title: 'My Project'
   		},
   		{
   			id: 2,
   			title: 'Candice'
   		}
   	];

   	$scope.goToProject = function (project) {
   		console.log("i'm going to project", project.id)
   		$location.path('/projects/' + project.id);
   	};

      $scope.gotProjectName = function (project) {
         console.log("i'm going to project", project.id)
         $location.path('/projects/' + project.id);
      };
  }]);
