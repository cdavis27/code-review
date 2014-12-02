'use strict';

angular.module('codeReviewApp.controllers')
.controller('ProjectCtrl', ['$scope', '$routeParams', '$location',
function ($scope, $routeParams, $location) {

	$scope.projectId = $routeParams.projectId;

	$scope.files = [
   		{
   			id: 1,
   			title: 'File 1',
   			file: 'test.txt'
   		},
   		{
   			id: 2,
   			title: 'file 2',
   			file: 'test2.txt'
   		},
   		{
   			id: 3,
   			title: 'file 3',
   			file: 'test3.txt'
   		}
   	];

   	$scope.goToFile = function (file, projectId) {
   		console.log("i'm going to file", file.id);
   		console.log("Project", projectId);
   		$location.path('/projects/' + projectId + '/file/' + file.id);
   	};
}])