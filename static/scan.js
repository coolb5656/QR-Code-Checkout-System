$(document).ready(function(){
    var items = [];

    $("#scan").on("click", function (){
        $("#code").focus();
        $('#code').val('');
    });

    $("#code").change(function addItem() {
        $.getJSON($SCRIPT_ROOT + '/scan', {
            code: $('input[name="code"]').val(),
          }, function(data) {
            if(data.itemStatus && !(items.includes(data.item_id))){
              items.push(data.item_id)
              $("#items").append(data.result+"<br>");
              $('#ids').val(items);
            }
            else {
              alert("Item is already checked out or not existent!")
              
            }
          });
          return false;
    })

    $('form input').keydown(function (e) {
      if (e.keyCode == 13) {
          e.preventDefault();
          $("#code").blur()
          $("#code").focus();
          $('#code').val(''); 
          return false;
      }
  });
})
