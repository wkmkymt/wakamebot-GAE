/* ========
 *  Config
 * ======== */
var myForm = angular.module("myForm", []);

/* Jinja2 : {{ item }}
 * Angular: [[ item ]] */
myForm.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
});


/* ============
 *  Initialize
 * ============ */
$(document).ready(function() {
  /* Initialization of the form */
  $("#addType").show();
  $("#removeType").hide();

  /* Add the event when radio button is checked */
  $("input:radio").bind("change", changeAction);
});


/* ===============
 *  Change Action
 * =============== */
var changeAction = function() {
  /* Change of elements to display */
  $("#addType").toggle();
  $("#removeType").toggle();

  /* Change of form's action */
  $("form[name='botForm']").attr("action", $("input:radio:checked").val());
};