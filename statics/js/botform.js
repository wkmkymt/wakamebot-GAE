/* ============
 *  Initialize
 * ============ */
$(document).ready(function() {
  /* Initialization of the form */
  $("#addType").show();
  $("#removeType").hide();

  /* Add the event when radio button is checked */
  $("input:radio").bind("change", changeAction);
  $("input:checkbox").bind("change", checkCheckBox);
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


  /* Check checkboxes' number when botForm is removeType */
  if($("input:radio:checked").val() == "/remove")
    checkCheckBox();
};


/* ================
 *  Check CheckBox
 * ================ */
var checkCheckBox = function() {
  /* Disable remove button if checkbox isn't checked */
  $("input:submit[name='removeBtn']").attr("disabled", !isChecked());
};


/* ======================
 *  Is CheckBox Checked?
 * ====================== */
var isChecked = function() {
  /* Get checkboxes */
  var checked = $("input:checkbox:checked");

  if(checked.size())
    return true;
  else
    return false;
};