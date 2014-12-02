'use strict';
angular.module('codeReviewApp.controllers', []);

/**
 * @ngdoc overview
 * @name codeReviewApp
 * @description
 * # codeReviewApp
 *
 * Main module of the application.
 */
angular
  .module('codeReviewApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.codemirror',
    'codeReviewApp.controllers'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/projects', {
        templateUrl: 'views/projects.html',
        controller: 'ProjectsCtrl'
      })
      .when('/projects/:projectId', {
        templateUrl: 'views/project.html',
        controller: 'ProjectCtrl'
      })
      .when('/reviews', {
        templateUrl: 'views/reviews.html',
        controller: 'ReviewsCtrl'
      })
      .when('/activity', {
        templateUrl: 'views/activity.html',
        controller: 'ActivityCtrl'
      })
      .when('/projects/:projectId/file/:fileId', {
        templateUrl: 'views/file.html',
        controller: 'FileCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });

