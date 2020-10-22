var redisApp = angular.module('redis', ['ui.bootstrap']);

/**
 * Constructor
 */
function RedisController() {}

redisApp.controller('RedisCtrl', function ($scope, $http, $location) {
        $scope.controller = new RedisController();
        $scope.controller.scope_ = $scope;
        $scope.controller.location_ = $location;
        $scope.controller.http_ = $http;

    $scope.onRedis = function() {
	value = $scope.msg;
	$http.get("/message/set/" + value)
            .success(angular.bind(this, function(data) {
		console.log(data);
		$scope.messages = data;
		$scope.msg = "";
            }));
    };

    $scope.onErase = function() {
	$http.get("/message/erase")
            .success(angular.bind(this, function(data) {
		$scope.messages = data;
		$scope.msg = "";
            }));
    };

    $scope.controller.http_.get("/message/all")
        .success(function(data) {
            $scope.messages = data;
        });
});
