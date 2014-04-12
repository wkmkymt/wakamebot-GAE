var myForm = angular.module("myForm", []);

/* Jinja2 : {{ item }}
 * Angular: [[ item ]] */
myForm.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
});