$(document).ready(function(){
    var items = [];

    $("#scan").on("click", function (){
        $("#code").focus();
        $('#code').val('');
    });

    $("#code").change(function addItem() {
        $.getJSON($SCRIPT_ROOT + '/scan', {
            code: $('#code').val(),
            action: 0

          }, function(data) {
            if(data.itemStatus && !(items.includes(data.item_id))){
              items.push(data.item_id)
              $("#items").append(data.result+"<br>");
              $('#ids').val(items);
            }
            else {
              alert("Item is not checked out or not existent!")
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
