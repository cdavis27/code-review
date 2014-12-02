'use strict';

/**
 * @ngdoc function
 * @name codeReviewApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the codeReviewApp
 */
angular.module('codeReviewApp.controllers')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
