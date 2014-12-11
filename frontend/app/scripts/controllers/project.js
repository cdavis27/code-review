'use strict';

angular.module('codeReviewApp.controllers')
.controller('ProjectCtrl', ['$scope', '$routeParams', '$location', 'Restangular',
function ($scope, $routeParams, $location, Restangular) {

	$scope.projectId = $routeParams.projectId;

	$scope.project = undefined;

   // Asynchronously get data from the server
   Restangular.one('projects', $scope.projectId).get().then(function(data) {
      $scope.project = data;
   })

	$scope.goToFile = function (file, projectId) {
		console.log("i'm going to file", file.id);
		console.log("Project", projectId);
		$location.path('/projects/' + projectId + '/file/' + file.id);
	};
}])