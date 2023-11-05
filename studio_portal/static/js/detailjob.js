$(document).ready(function(){
    var checkbox = $('#id_send_art_to_customer');
    var button = $('#customeremailbtn');
    if (checkbox.is(':checked')) {
        button.html('Submit proof to customer')
    } else {
        button.html('Submit proof to Rep');
    }
    checkbox.on('change click', function() {
        if (checkbox.is(':checked')) {
            button.html('Submit proof to customer');
            
        } else {
            button.html('Submit proof to Rep');
        }
    });
    $('#customeremailbtn').on('click',function(e){
        e.preventDefault();
        let customerEmail = $('#id_email_customer').val();
        let url = "/sendmailto_customer"
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        let respEmail = $('#id_user_email').val()
        let quote_no = $('#quote_no').val()
        let formData = new FormData()
        formData.append('customer_email',customerEmail)
        formData.append('csrfmiddlewaretoken',csrfToken)
        formData.append('id',job_id)
        formData.append('resp_email',respEmail)
        formData.append('quote_no',quote_no)
        $('.page_loader').css('display','flex');
        $.ajax({
            url:url,
            type:"POST",
            data:formData,
            processData: false,
            contentType: false,
            success: function(data, textStatus, xhr){
                $('.page_loader').css('display','none');
                alert("Proof has been sent successfully.")
                console.log(data)
            }
            
        })
    })
    $('#compfiles').map((idx,elm) =>{
        console.log($(elm).next())
    })
    $('.th[val="Completed Files"], td:nth-child(9)').each(function() {
        var text = $(this).text().trim();
        var button = $(this).next().find('#customeremailbtn');
        
        if (text === '') {
            button.hide().prop('disabled', true);
        } else {
            button.show().prop('disabled', false);
        }
    });
    
    
    
});







// code for status row highlight

  let status = "{{jobdetail.status.status_value}}";

  $('.breadcrumbs_item').each(function() {
    var spanText = $(this).find('span').text();

    if (spanText === status) {
      $(this).addClass('highlight');
      $(this).find('.arrow').addClass('highlight-arrow');
    }
  });
