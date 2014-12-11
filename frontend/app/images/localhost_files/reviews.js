'use strict';

/**
 * @ngdoc function
 * @name codeReviewApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the codeReviewApp
 */
angular.module('codeReviewApp.controllers')
  .controller('ReviewsCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });