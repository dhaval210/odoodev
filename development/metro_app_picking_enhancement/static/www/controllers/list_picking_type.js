/* global angular */

angular.module('mobile_app_picking').controller(
  'ListPickingTypeCtrl', [
    '$scope', '$rootScope', '$state', 'PickingTypeModel', '$translate', 'tools',
    function ($scope, $rootScope, $state, PickingTypeModel, $translate, tools) {
      $scope.data = {
        'pickingTypes': [],
        'filter': null,
      };

      $scope.$on(
        '$stateChangeSuccess',
        function (event, toState, toParams, fromState, fromParams) {
          if ($state.current.name === 'list_picking_type') {
            // Show loader
            $rootScope.$broadcast('handleBroadcastSpinner', true);

            tools.focus();
            $scope.data.filter = null;
            PickingTypeModel.get_list().then(function (pickingTypes) {
              $scope.data.pickingTypes = pickingTypes;
              // Hide loader
              $rootScope.$broadcast('handleBroadcastSpinner', false);
              // Skip this screen if there is only one picking type
              if ($scope.data.pickingTypes.length === 1) {
                $state.go(
                  'list_picking',
                  {picking_type_id: $scope.data.pickingTypes[0].id});
              }
            }).catch(function (r) {
              $scope.data.errorMessage = r["fullTrace"]["data"]["message"];
              // console.log(r);
              tools.display_loading_end();
              // Hide loader
              $rootScope.$broadcast('handleBroadcastSpinner', false);
            });
          }
        });
    }]);
