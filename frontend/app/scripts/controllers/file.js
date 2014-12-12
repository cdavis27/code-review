'use strict';

angular.module('codeReviewApp.controllers')
.controller('FileCtrl', ['$scope', '$routeParams', 'Restangular', '$modal',
function ($scope, $routeParams, Restangular, $modal) {

  	$scope.fileId = $routeParams.fileId;
  	$scope.projectId = $routeParams.projectId;

	$scope.file = undefined;
	$scope.project = undefined;
	$scope.comment = "";

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

	$scope.saveComment = function(_comment) {
		console.log("here");
	}

	// $scope.myComment = {
	// } 

	// Restangular.all('comments').customPOST(myComment).then(function(data) {
	// });

	$scope.editor = undefined;
	
	$scope.codemirrorLoaded = function(_editor) {
		var _doc = _editor.getDoc();

		var unWatch = $scope.$watch('file', function(newVal, oldVal) {
			if (newVal) {
				// Make sure to mark all the lines that have a comment
				for (var i=0; i<$scope.file.comments.length; i++) {
					var comment = $scope.file.comments[i];
					console.log(i, comment);
				}

				unWatch();
			}
		})

		_editor.focus();
		_editor.on("gutterClick", function(cm, n) {
			//get line number
			openCommentModal(n);
			//on save place marker
			var info = cm.lineInfo(n);
			cm.setGutterMarker(n, "comment-gutter", info.gutterMarkers ? null : makeMarker());

			function makeMarker() {
				console.log("here");
				var marker = document.createElement("div");
				marker.style.color = "#6ADBD0";
				marker.innerHTML = "●";
				return marker;
			}
		});
	};

	$scope.editorOptions = {
	  lineWrapping : true,
	  lineNumbers: true,
	  mode: 'javascript',
	  theme: 'monokai',
	  gutters: ["CodeMirror-linenumbers", "comment-gutter"]
	};


	var openCommentModal = function (lineNumber) {
		var modalInstance = $modal.open({
			templateUrl: 'scripts/directives/commentModal/comment-modal.html',
			controller: 'CommentModalCtrl',
			// size: 'lg',
			resolve: {
				lineNumber: function () { return lineNumber; },
				file: function() { return $scope.file; }
			}
		});

		modalInstance.result.then(function (newComment) {
			// here you can do the code to POST to the server
			// using restangular (for a new Comment)
			console.log("Comment Text:", newComment);
			Restangular.all('comments/').customPOST(newComment).then(function(data) {
				console.log("Comment saved", data)
			});
		}, function () {
			// The modal was 'canceled'
		});
	}
  
}])
