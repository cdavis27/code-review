'use strict';

angular.module('codeReviewApp.controllers')
.controller('FileCtrl', ['$scope', '$routeParams', 'Restangular',
function ($scope, $routeParams, Restangular) {

  	$scope.fileId = $routeParams.fileId;
  	$scope.projectId = $routeParams.projectId;

	$scope.file = undefined;
	$scope.project = undefined;

	// Asynchronously get data from the server
	Restangular.one('files', $scope.fileId).get().then(function(data) {
	  $scope.file = data;

	  // You now have the $scope.file.language .. so set the $scope.editorOptions
	  $scope.editorOptions.mode = $scope.file.language.codemirror_mode;
	})

	// Asynchronously get data from the server
	Restangular.one('projects', $scope.projectId).get().then(function(data) {
	  $scope.project = data;
	})

	$scope.editorOptions = {
	  lineWrapping : true,
	  lineNumbers: true,
	  mode: 'javascript',
	  theme: 'monokai'
	};
  
}])
