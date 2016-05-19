var projects = angular.module('projects',[]);

projects.config(function($interpolateProvider) {
	
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

projects.config(function($httpProvider) {

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});



projects.controller('ListCtrl', function($scope, $http) {
	

	$scope.toggleEdit = [];
	$scope.editItem = function(itemIndex) {
		$scope.toggleEdit[itemIndex] = true;
	};


    $scope.loadItems = function() {
        
        $http({
	        method : "GET",
	        url : "/projectlist/"
    	}).then(function(response) {
        	$scope.items = response.data;
    	});
    };

    $scope.loadItems();
    $scope.currentItem = {};

    $scope.saveItem = function() {
    	$http({
          method  : 'POST',
          url     : '/projectlist/',
          data    : $scope.currentItem,
          headers : {'Content-Type': 'application/json'} 
         }).success(function() {
            
				$scope.loadItems();
				$scope.currentItem = {};
          });

     };

 	$scope.updateItem = function(item) {
    	$http({
          method  : 'PUT',
          url     : '/projectlist/'+item.id,
          data    : item,
          headers : {'Content-Type': 'application/json'} 
         }).success(function(data) {
            
				$scope.loadItems();
				$scope.currentItem = {};
          });
 	};


    $scope.delItem = function(item) {
    	$http.delete('/projectlist/'+item.id).then(function(response){
            $scope.loadItems();
        });
    };


    
});

projects.controller('ImagesCtrl', function($scope, $http, $location) { 

	$scope.imagesUser = $location.absUrl().split('/')[3]; // getting the username from the url for the REST API filter

	$scope.loadImages = function() {
        
        $http({
	        method : "GET",
	        url : "/imagelist/"+$scope.imagesUser,
    	}).then(function(response) {
        	$scope.images = response.data;
    	});
    };

    $scope.loadImages();


    $scope.saveImage = function(image) {
    	var fd = new FormData(imageform);
    	var xhr = new XMLHttpRequest;
    	$scope.barPercent = 0;

    	// var blob = new Blob([image.compressed.dataURL], {type: 'image/jpeg'});
    	// var file = new File([blob], 'image.jpg');


var dataURL = image.compressed.dataURL;

function dataURItoBlob(dataURI) {
    var binary = atob(dataURI.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}

var blob = dataURItoBlob(dataURL);
var myimage = new File([blob], 'image.jpg');



    	fd.append('image', myimage);

    	xhr.upload.onprogress = function(e) {

            $scope.$apply(function() {
              
                if (e.lengthComputable) {
                    $scope.barPercent = Math.round(e.loaded / e.total * 100);
                };
            });
        };

        xhr.upload.onload = function(e) {

            $scope.$apply(function() { 
            	$scope.loadImages();
            	// $scope.barPercenst = 0;

            });
        };

   		xhr.open('POST', '/imagelist/');
        xhr.send(fd);

     };

});

projects.controller('ReviewsCtrl', function($scope, $http, $location) {
	
	$scope.reviewee = $location.absUrl().split('/')[3];

	$scope.toggleEdit = [];
	$scope.editItem = function(itemIndex) {
		$scope.toggleEdit[itemIndex] = true;
	};

	$scope.loadReviews = function() {
        
        $http({
	        method : "GET",
	        url : "/reviewlist/"+$scope.reviewee,
    	}).then(function(response) {
        	$scope.reviews = response.data;
    	});
    };

    $scope.loadReviews();
    // $scope.currentReview = {};

    $scope.saveReview = function() {
    	// $scope.currentReview.reviewed = $scope.reviewee;
    	// $scope.currentReview.append("reviewed", $scope.reviewee);

    	$http({
          method  : 'POST',
          url     : '/reviewlist/',
          data    : $scope.currentReview,
          headers : {'Content-Type': 'application/json'} 
         }).success(function() {

				$scope.loadReviews();
				$scope.currentReview.rating =null;
				$scope.currentReview.review_text =null;
          });
    

     };


     $scope.updateReview = function(review) {
     	
     	$http({
          method  : 'PUT',
          url     : '/reviewlist/'+review.id,
          data    : review,
          headers : {'Content-Type': 'application/json'} 
         }).success(function(data) {            
				$scope.loadReviews();
          });
     };

     $scope.deleteReview = function(review) {
    	$http.delete('/reviewlist/'+review.id).then(function(response){
            $scope.loadReviews();
        });
    };


     $scope.rateFunction = function( rating ) { 
     	$scope.currentReview.rating = rating;
     };
     $scope.updateFunction = function(rating, review){
     	review.rating = rating;
     };
});



projects.controller('BidsCtrl', function($scope, $http, $location) {
	
	$scope.project_id = $location.absUrl().split('/')[3];

	$scope.toggleEdit = [];
	$scope.editItem = function(itemIndex) {
		$scope.toggleEdit[itemIndex] = true;
	};

	$scope.loadBids = function() {
        
        $http({
	        method : "GET",
	        url : "/bidlist/"+$scope.project_id,
    	}).then(function(response) {
        	$scope.bids = response.data;
    	});
    };

    $scope.loadBids();

    $scope.saveBid = function() {

    	console.log($scope.currentBid);
    	$http({
          method  : 'POST',
          url     : '/bidlist/',
          data    : $scope.currentBid,
          headers : {'Content-Type': 'application/json'} 
         }).success(function() {

				$scope.currentBid.amount=null;
				$scope.currentBid.descrip=null;
				$scope.loadBids();				
          });
     };


	$scope.updateBid = function(bid) {
		$http({
		  method  : 'PUT',
		  url     : '/biddetail/'+bid.id,
		  data    : bid,
		  headers : {'Content-Type': 'application/json'} 
	 	}).success(function(data) {            
			$scope.loadBids();
	  	});
	};

	$scope.deleteBid = function(bid) {
		$http.delete('/biddetail/'+bid.id).then(function(response){
		    $scope.loadBids();
		});
	};


});

 // --------------------------------------------  directives -----------------------------------------------------


projects.directive('starRating', function() {
return {
restrict : 'A',
template : '<ul class="rating">'
   + ' <li ng-repeat="star in stars" ng-class="star" ng-click="toggle($index)">'
   + '  <i class="fa fa-star"></i>'
   + ' </li>'
   + '</ul>',
    
scope : {
	clickable : '@',
	ratingValue : '=',
	max : '=',
	onRatingSelected : '&'
},
    
link : function(scope, elem, attrs) {
 var updateStars = function() {
  scope.stars = [];
  for ( var i = 0; i < scope.max; i++) {
   scope.stars.push({
    filled : i < scope.ratingValue
   });
  }
 };
 
 scope.toggle = function(index) {
 	if(scope.clickable=='true') {
	  scope.ratingValue = index + 1;
	  scope.onRatingSelected({rating : index + 1});
	}
 };
 
 scope.$watch('ratingValue',
  function(oldVal, newVal) {
   if (newVal) {
    updateStars();
   }
  }
 );
}
};
}
);

'use strict';
/*******************************
 adapted off of weeroom/angularjs-imageupload-directive and JIC from github
 https://github.com/weroom/angularjs-imageupload-directive/blob/master/public/javascripts/imageupload.js
 https://github.com/brunobar79/J-I-C
 *********************************/

projects.directive('image', ['$q',
	function($q) {


		var URL = window.URL || window.webkitURL;

		var getResizeArea = function() {
			var resizeAreaId = 'fileupload-resize-area';

			var resizeArea = document.getElementById(resizeAreaId);

			if (!resizeArea) {
				resizeArea = document.createElement('canvas');
				resizeArea.id = resizeAreaId;
				resizeArea.style.visibility = 'hidden';
				document.body.appendChild(resizeArea);
			}

			return resizeArea;
		};

		/**
		 * Receives an Image Object (can be JPG OR PNG) and returns a new Image Object compressed
		 * @param {Image} sourceImgObj The source Image Object
		 * @param {Integer} quality The output quality of Image Object
		 * @return {Image} result_image_obj The compressed Image Object
		 */

		var jicCompress = function(sourceImgObj, options) {
			var outputFormat = options.resizeType;
			var quality = options.resizeQuality * 100 || 70;
			var mimeType = 'image/jpeg';
			if (outputFormat !== undefined && outputFormat === 'png') {
				mimeType = 'image/png';
			}


			var maxHeight = options.resizeMaxHeight || 300;
			var maxWidth = options.resizeMaxWidth || 250;

			var height = sourceImgObj.height;
			var width = sourceImgObj.width;

			// calculate the width and height, constraining the proportions
			if (width > height) {
				if (width > maxWidth) {
					height = Math.round(height *= maxWidth / width);
					width = maxWidth;
				}
			}
			else {
				if (height > maxHeight) {
					width = Math.round(width *= maxHeight / height);
					height = maxHeight;
				}
			}

			var cvs = document.createElement('canvas');
			cvs.width = width; //sourceImgObj.naturalWidth;
			cvs.height = height; //sourceImgObj.naturalHeight;
			var ctx = cvs.getContext('2d').drawImage(sourceImgObj, 0, 0, width, height);
			var newImageData = cvs.toDataURL(mimeType, quality / 100);
			var resultImageObj = new Image();
			resultImageObj.src = newImageData;
			return resultImageObj.src;

		};

		var resizeImage = function(origImage, options) {
			var maxHeight = options.resizeMaxHeight || 300;
			var maxWidth = options.resizeMaxWidth || 250;
			var quality = options.resizeQuality || 0.7;
			var type = options.resizeType || 'image/jpg';

			var canvas = getResizeArea();

			var height = origImage.height;
			var width = origImage.width;

			// calculate the width and height, constraining the proportions
			if (width > height) {
				if (width > maxWidth) {
					height = Math.round(height *= maxWidth / width);
					width = maxWidth;
				}
			}
			else {
				if (height > maxHeight) {
					width = Math.round(width *= maxHeight / height);
					height = maxHeight;
				}
			}

			canvas.width = width;
			canvas.height = height;

			//draw image on canvas
			var ctx = canvas.getContext('2d');
			ctx.drawImage(origImage, 0, 0, width, height);

			// get the data from canvas as 70% jpg (or specified type).
			return canvas.toDataURL(type, quality);
		};

		var createImage = function(url, callback) {
			var image = new Image();
			image.onload = function() {
				callback(image);
			};
			image.src = url;
		};

		var fileToDataURL = function(file) {
			var deferred = $q.defer();
			var reader = new FileReader();
			reader.onload = function(e) {
				deferred.resolve(e.target.result);
			};
			reader.readAsDataURL(file);
			return deferred.promise;
		};


		return {
			restrict: 'A',
			scope: {
				image: '=',
				resizeMaxHeight: '@?',
				resizeMaxWidth: '@?',
				resizeQuality: '@?',
				resizeType: '@?'
			},
			link: function postLink(scope, element, attrs) {

				var doResizing = function(imageResult, callback) {
					createImage(imageResult.url, function(image) {
						//var dataURL = resizeImage(image, scope);
						var dataURLcompressed = jicCompress(image, scope);
						// imageResult.resized = {
						// 	dataURL: dataURL,
						// 	type: dataURL.match(/:(.+\/.+);/)[1]
						// };
						imageResult.compressed = {
							dataURL: dataURLcompressed,
							type: dataURLcompressed.match(/:(.+\/.+);/)[1]
						};
						callback(imageResult);
					});
				};

				var applyScope = function(imageResult) {
					scope.$apply(function() {
						console.log(imageResult);
						if (attrs.multiple) {
							scope.image.push(imageResult);
						}
						else {
							scope.image = imageResult;
						}
					});
				};


				element.bind('change', function(evt) {
					//when multiple always return an array of images
					if (attrs.multiple)
						{scope.image = [];}

					var files = evt.target.files;
					for (var i = 0; i < files.length; i++) {
						//create a result object for each file in files
						var imageResult = {
							file: files[i],
							url: URL.createObjectURL(files[i])
						};

						fileToDataURL(files[i]).then(function(dataURL) {
							console.log(dataURL)
							imageResult.dataURL = dataURL;
						});

						if (scope.resizeMaxHeight || scope.resizeMaxWidth) { //resize image
							doResizing(imageResult, function(imageResult) {
								applyScope(imageResult);
							});
						}
						else { //no resizing
							applyScope(imageResult);
						}
					}
				});
			}
		};
	}
]);
