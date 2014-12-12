'use strict';

angular.module('codeReviewApp.directives')
.controller('CommentModalCtrl', ['$scope', '$modalInstance', 'lineNumber', 'file', 
function($scope, $modalInstance, lineNumber, file) {
	$scope.file = file;

	$scope.newComment = {
		commentor: 1,
		file: file.id,
		line_number: lineNumber,
		text: '',
		date_created: null
	};
	
	$scope.saveComment = function(newComment) {
		// make sure to update newComment.date_created

		$modalInstance.close(newComment);
	}

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	}
}])