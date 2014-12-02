'use strict';

angular.module('codeReviewApp.controllers')
.controller('FileCtrl', ['$scope', '$routeParams',
function ($scope, $routeParams) {

  $scope.id = $routeParams.fileId;
  
  $scope.editorOptions = {
      lineWrapping : true,
      lineNumbers: true,
      mode: 'javascript',
      theme: 'monokai'
  };
  
}])
