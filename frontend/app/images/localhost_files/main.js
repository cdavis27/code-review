'use strict';

angular.module('codeReviewApp.controllers')
  .controller('MainCtrl', function ($scope) {
  	$scope.$root.hideHeader = true;
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
