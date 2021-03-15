$("form[name=signup").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
      url: "/signup",
      method: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        if ("error" in resp){
          $error.text(resp.error).removeClass("error--hidden");
        }else{
          window.location.href = "/concert/list";
        }
      }
    });
  
    e.preventDefault();
  });

  $("form[name=login_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
      url: "/login",
      method: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        if ("error" in resp){
          $error.text(resp.error).removeClass("error--hidden");
        }else{
          window.location.href = "/concert/list";
        }
      }
    });
  
    e.preventDefault();
  });

  $(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 1500);
  });

  $('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
    })

  // $(document).ready( function () {
  //   $('#concertList').dataTable();
  // });

  $(document).ready(function() {
    var table = $('#concertList').DataTable();
 
    $('#concertList tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );
 
    $('#selectedconcert').click( function () {
      var data = [];
      for(var i=0 ;i < table.rows('.selected').data().length;i++){
        data.push(table.rows('.selected').data()[i][0])
      }
      $.ajax({
        url: "/concert/closeorder",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function () {
          location.href = '/';
        }
      })
    } );
} );

  $(document).ready(function() {
    var table = $('#userList').DataTable();

    $('#userList tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

    $('#countuser').click( function () {
        var data = [];
        for(var i=0 ;i < table.rows('.selected').data().length;i++){
          data.push(table.rows('.selected').data()[i][0])
        }
        $.ajax({
          url: "/permission",
          method: "POST",
          contentType: "application/json",
          data: JSON.stringify(data),
          dataType: "json",
          success: function () {
            location.href = '/permission';
          }
        })
    } );
  } );

  $(document).ready(function() {
    var table = $('#waitedList').DataTable();

    $('#waitedList tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

    $('#selectpurchase').click( function () {
        console.log( table.rows('.selected').data()[0]);
    } );
  } );

  $(document).ready(function() {
    var table = $('#purchasedList').DataTable();

    $('#purchasedList tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

    $('#selectpurchased').click( function () {
        console.log( table.rows('.selected').data()[0]);
    } );
  } );


$('#paymentModal, #purchasedModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('payment') // Extract info from data-* attributes
  var username = button.data('username')
  var transid = button.data('transid')

  var modal = $(this)
  modal.find('#status').text('Payment of ' + username)
  modal.find('#paymentImage').attr("src", recipient);
  modal.find('#confirmPayment').attr('value', transid)
})


$('#confirmPayment').click(function(){
  var pathname = window.location.pathname;
  var formData = {
    'transid': $(this).attr('value')
  };
  console.log(formData);
  $.ajax({
        type: 'POST',
        url: pathname+'/payment',
        contentType: "application/json",
        data: JSON.stringify(formData),
        dataType: 'json',
        success: function () {
          location.href = pathname;
        }
    })
  });