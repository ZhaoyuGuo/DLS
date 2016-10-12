angular.module('layerService', [])
    .service('layerService', ['$rootScope', LayerService]);

function LayerService($rootScope) {
    var self = this;

    const networkLayerEvent = {
        UPDATE: 'layer:update',
        CLEAR: 'layer:clear',
        ADD: 'layer:add',
        REMOVE: 'layer:remove'
    };

    var categories = [];
    var layers = [];

    this.pubLayersUpdateEvent = function() {
        $rootScope.$emit(networkLayerEvent.UPDATE, {});
    };

    this.subLayersUpdateEvent = function(callback) {
        $rootScope.$on(networkLayerEvent.UPDATE, callback);
    };

    this.loadCategoryLayerTree = function () {
        var future = loadCategoriesHttp();
        future.then(function mySucces(response) {
            categories.length = 0;
            response.data.forEach(function (layer) {
                categories.push(layer);
            });
            var future = loadLayersHttp();
            future.then(function mySucces(response) {
                layers.length = 0;
                response.data.forEach(function (layer) {
                    layers.push(layer)
                });
                self.pubLayersUpdateEvent();
            }, function myError(response) {
            });
        }, function myError(response) {
        });
    };

    function loadCategoriesHttp() {
        return $http({
            method: "GET",
            url: "/network/layer/categories"
        })
    }

    function loadLayersHttp() {
        return $http({
            method: "GET",
            url: "/network/layers"
        })
    }

    this.getCategories = function() {
        return categories;
    };

    this.getLayers = function() {
        return layers;
    };

    this.getLayerByType = function(type) {
        for (var i = 0, len = layers.length; i < len; i++) {
            var layer = layers[i];
            if(layer.layerType == type) {
                var copy = copyObject(layer);
                return copy;
            }
        }
    };

    this.setLayers = function(new_layers) {
        layers = new_layers;
    };

    function copyObject(obj) {
        var copy = obj.constructor();
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr))
                if (obj[attr] !== null && typeof obj[attr] === 'object') {
                    copy[attr] = copyObject(obj[attr]);
                } else {
                    copy[attr] = obj[attr];
                }
        }
        return copy;
    }
}