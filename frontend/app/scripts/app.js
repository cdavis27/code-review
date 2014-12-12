'use strict';
angular.module('codeReviewApp.controllers', []);
angular.module('codeReviewApp.directives', []);

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
    'ngUpload',
    'ui.bootstrap',
    'restangular',
    'codeReviewApp.controllers',
    'codeReviewApp.directives'
  ])
  .config(function ($routeProvider, RestangularProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
       .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl'
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
      .when('/projects/:projectId/comments', {
        templateUrl: 'views/comments.html',
        controller: 'CommentsCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });

      RestangularProvider.setBaseUrl('http://localhost:8001/v1/');
  });

