'use strict';

/**
 * @ngdoc function
 * @name codeReviewApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the codeReviewApp
 */
angular.module('codeReviewApp.controllers')
.controller('ProjectsCtrl', ['$scope', '$location',
function ($scope, $location) {
	
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
  }]);
