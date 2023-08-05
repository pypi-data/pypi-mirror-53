"use strict";

app.directive('pagination', function () {
    return {
        templateUrl: 'static/elements/pagination.html',
        controller: 'PaginationController'
    }
});

app.directive('menu', function () {
    return {
        templateUrl: 'static/elements/menu.html',
        controller: 'MenuController'
    }
});

app.directive('monitorlevel', function () {
    return {
        templateUrl: 'static/elements/monitorLevel.html',
        controller: 'MonitorLevelController',
        scope: {
            name: '=',
            value: '='
        }
    }
});

app.directive('endpointdetails', function () {
    return {
        templateUrl: 'static/elements/endpointDetails.html',
        controller: 'EndpointController',
        scope: {
            name: '=',
            value: '='
        }
    }
});