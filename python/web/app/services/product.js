app.service('ProductService', ['$http', function($http) {
    return {
        getAll: function(successCallback, errorCallback) {
            var type = location.hash.split('=')[1];
            $http.get('/api/product/category/' + type).then(successCallback, errorCallback);
        },
        add: function(product, successCallback, errorCallback) {
            $http({
                method: 'POST',
                url: '/api/product/',
                headers: {
                    'Content-Type': undefined
                },
                data: product,
                transformRequest: function (data, headersGetter) {
                    var formData = new FormData();
                    angular.forEach(data, function (value, key) {
                        formData.append(key, value);
                    });

                    var headers = headersGetter();
                    delete headers['Content-Type'];

                    return formData;
                }
            })
            .success(successCallback)
            .error(errorCallback);
        }
    };
}]);