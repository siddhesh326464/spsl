
$(document).ready(function(){
    $('#updatebtn,#updatebtn1').unbind('click').on("click",function(e){
        e.preventDefault();
        let errorHtml = `<div class="error_msg text-danger">This field is required</div>`;
        let emailErrorHtml = `<div class="error_msg text-danger">Please enter a valid email address.</div>`;
        let statusErrorHtml = `<div class="error_msg text-danger">Please change status to completed</div>`;
        let isError = false;

        $('.form-control:required').map((idx, elm) => {
            if (!$(elm).val()){
                isError = true;
                $(elm).next().remove();
                $(elm).after(errorHtml);
            }
            else{
                $(elm).next().remove();
            }
        });

        if ($('#id_proof_request_type option:selected').attr('value') == '0'){
            isError = true;
            $('#id_proof_request_type').next().remove();
            $('#id_proof_request_type').after(errorHtml);
        }
        else{
            $('#id_proof_request_type').next().remove();
        }

        // if ($('#id_status option:selected').text() == 'Completed') {
        //     $('.dynamic-form [data-id = completed]').map((idx, elm) => {
        //         if (!$(elm).val() && $(elm).next().children().length == 0) {
        //             isError = true;
        //             $(elm).next().next().remove();
        //             $(elm).next().after(errorHtml);
        //         }
        //     });
        // }
        // else if ($('#id_status option:selected').text() != 'Completed'){
        //     $('.dynamic-form [data-id = completed]').map((idx,elm)=>{
        //         if ($(elm).val()){
        //             isError = true;
        //             $('#id_status').next().remove();
        //             $('#id_status').after(statusErrorHtml);
        //         }
        //     });
        // }
        // else{
        //     $('.dynamic-form [data-id = completed]').next().next().remove();
        //     $('#statusErrorHtml').next().remove();
        // }

        // $('.dynamic-form input[data-id=item_id').map((idx,elm) =>{
        debugger;
        $('#id_job-0-item').map((idx,elm) =>{
            debugger;
            if (!$(elm).val()){
                isError = true;
                $(elm).next().remove();
                $(elm).after(errorHtml)
            }
            else{
                $(elm).next().remove();
                isError=isError
            }
        })

        // $('.dynamic-form input[data-id=submitted').map((idx,elm) =>{
        //     if (!$(elm).val()){
        //         isError = true;
        //         $(elm).next().remove();
        //         $(elm).after(errorHtml)
        //     }
        //     else{
        //         $(elm).next().remove();
        //         isError=isError
        //     }
        // })
        
        // $('.dynamic-form [data-id][submitted]').each((idx, elm) => {
        //     debugger;
        //     const inputElement = $(elm);
        //     const errorElement = inputElement.next().next(); // Assuming error element is two siblings after the input
        //     if (!inputElement.val()) {
        //         isError = true;
        //         errorElement.remove();
        //         inputElement.next().after(errorHtml);
        //     } else {
        //         errorElement.remove();
        //         isError = false; // Assuming you want to set isError to false when there's no error
        //     }
        // });
        if ($('#id_send_art_to_customer').is(':checked')){
            let customerEmail = $('#id_customer_email').val();
            if(customerEmail==""){
                isError = true;
                $('#id_customer_email').next().remove();
                $('#id_customer_email').after(errorHtml);
            }else{
                let newCustomeremail = $('#id_customer_email').val();
                var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i;
                if(!pattern.test(newCustomeremail)){
                    isError=true;
                    $('#id_customer_email').next().remove();
                    $('#id_customer_email').after(emailErrorHtml);
                }else{
                    $('#id_customer_email').next().remove();
                }     
            }
        }

        $('#id_send_art_to_customer').on('change',function(){
            if ($(this).is(':checked')){
                let customerEmail = $('#id_customer_email').val();
                if(customerEmail.trim().length>0){
                    $('#id_customer_email').next().remove();
                }
            }
        });

        if (!isError){
            $('#updatejobform').submit();
        }
        else{
            alert("Please complete the mandatory fields.");
        }
    });



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
        let customerEmail = $('#id_customer_email').val()
        let url = "/sendmailto_customer"
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        let respEmail = $('#id_user_email').val()
        let quote_no = $('#id_quote_no').val();
        let formData = new FormData()
        if (checkbox.is(':checked')){
            if ($('#id_customer_email').val()==""){
                return alert ("please enter customer email")
            }else{
                let newCustomeremail = $('#id_customer_email').val();
                var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i
                if(!pattern.test(newCustomeremail)){
                    return alert("Please enter valid email address")
                }
            }
            formData.append('customer_email',customerEmail)
        }
        formData.append('csrfmiddlewaretoken',csrfToken)
        formData.append('id',job_id)
        formData.append('quote_no',quote_no)
        formData.append('resp_email',respEmail)
        $('.page_loader').css('display','flex');
        debugger;
        $.ajax({
            url:url,
            type:"POST",
            data:formData,
            processData: false,
            contentType: false,
            success: function(data, textStatus, xhr){
                debugger;
                $('.page_loader').css('display','none');
                alert(data['msg'])
            }
            
        })
    
    })
    $('.dynamic-form [data-id = completed]').map((idx,elm) =>{
        console.log($(elm).next().children())
        if ($(elm).next().children().length == 0){
            $('#download_btn').attr('disabled',true)
        }
    })
    $('.dynamic-form [data-id = completed]').map((idx,elm) =>{
        console.log($(elm).next().children())
        if ($(elm).next().children().length == 0){
            $('#customeremailbtn').attr('disabled',true)
        }
    })

    
});
    
    
    
// $(document).ready(function(){
//     var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
//     var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//          return new bootstrap.Tooltip(tooltipTriggerEl)
//     });
    
    // create new campaign link name on campaign search dropdown
    $('#id_campaign').select2({
        language:{
         noResults:function(){
              let seachvalue = $('.select2-search__field').val()
              $('#campaign_name').val(seachvalue);
              $('#campaign_add_btn').prop('disabled', false)
              $('#campaign_name').attr('data-id',"");
              return $("<a href='javascript:void(0)' class='text-decoration-none' data-bs-toggle='modal' data-bs-target='#staticBackdrop'>create campaign</a>");
         }
        }
    });
    $('.select2-selection__rendered').on('click',() => {
         $('.select2-search__field').attr('placeholder','search ...');
    });
    // create new campaign end

    // Descard button on page
    $('#discard_btn,#discard_btn1').unbind('click').on('click',function(e){
         e.preventDefault();
         let msg =confirm("The record has been modified, your changes will be discarded. Do you want to proceed?")
         if(msg == true ){
              $('form')[0].reset();
              window.location.replace('/')
         }   
    })
    // Descard button end 

    $('#id_send_art_to_customer').on('change load',function (){
         if($(this).is(":checked")){ 
              $('#customer_email').removeClass('remove_mail');
         } else {
              $('#customer_email').addClass('remove_mail');
         }
    })
    if($('#id_send_art_to_customer').is(":checked")){ 
         $('#customer_email').removeClass('remove_mail');
    } else {
         $('#customer_email').addClass('remove_mail');
    }

    // campaign add and disable logic
    $('#campaign_name').on('input', function() {
         let searchCam = $('.select2-search__field');
         let campaignName = $('.campaign_name').text();
         searchCam.val(searchCam.val() + ' ' + campaignName);
         var inputText = $(this).val().trim();
         inputText.length > 0 ? $('#campaign_add_btn').prop('disabled', false) : $('#campaign_add_btn').prop('disabled', true);
    });

    $('.close_btn').on('click',()=>{
         if ($('#id_campaign option:selected').val() == ""){
              $('#campaign_name').val("");
              $('#campaign_name').val().trim().length > 0 ? $('#campaign_add_btn').prop('disabled', false) : $('#campaign_add_btn').prop('disabled', true);
         }
    })
    // campaign add and disable logic end 

    // create campaign on create button
    $('#id_campaign').on('change keypress',function(){
         $('.campaign_btn').attr('disabled',false);
         let l = $('#id_campaign option:selected')
         let value = l.text()
         let id = l.val()
         if (id !=""){
              $('.campaign_btn').attr('disabled',false);
              // $('.fa-plus').toggleClass('fa-pencil fa-plus')
              $('#campaign_name').val(value)
              $('#campaign_name').attr('data-id',id)
              $('#campaign_add_btn').html('Save')
              $('.campaign_btn').on('click',function(){
                   let changed_value = $('#campaign_name').val()
                   
              })
         }else{
              
              $('.campaign_btn').attr('disabled',true);
              $('#campaign_name').val("")
              $('#campaign_name').attr('data-id',"").append(search_cam)
         }
    });
    
    $('#campaign_add_btn').unbind('click').on('click',function(){
         let campaignName = $('#campaign_name').val();
         let id = $('#campaign_name').attr('data-id') == "" ? "" : $('#campaign_name').attr('data-id');
         let csrfToken = $('input[name=csrfmiddlewaretoken]').val();
         let formData = new FormData()
         formData.append('id',id)
         formData.append('name',campaignName)
         formData.append('csrfmiddlewaretoken',csrfToken);
         let path = window.location.href;
         $('.page_loader').css('display','flex');
         $.ajax({
              url: path, 
              type: "POST",
              data: formData,
              processData: false,
              contentType: false,
              success: function (data, textStatus, xhr) {
                   $('.page_loader').css('display','none');
                   if (data.status === 'error'){
                        alert(data.msg);
                        return false;
                   }
                   $(".close_btn").click();
                   let l = $('#id_campaign option:selected')
                   let value = l.text()
                   let id = l.val()
                   $('.campaign_btn').attr('disabled',false);
                   $('#campaign_name').attr('data-id',data.res.id)
                   $('#campaign_add_btn').html('Save')
                   $('#campaign_add_btn').on('click',function(){
                   })
                   if (id) {
                        $(`#id_campaign option[value="${data.res.id}"]`).remove();
                   }
                    
                   let optionHtml = `<option value="${data.res.id}" data-select2-id="${data.res.id}" selected>${data.res.name}</option>`
                   $('#id_campaign').append(optionHtml).trigger('change.select2');
                   $('#campaign_name').val(data.res.name);
                   $('#campaign_name').attr('data-id', data.res.id);
                   $('#campaign_add_btn').html('Save');
                   $('.campaign_btn').attr('disabled', false);
                   $(".close_btn").click();
                   
              }, 
              error: function (textStatus, errorThrown) {
                   $('.page_loader').css('display','none');
                   console.log(textStatus,errorThrown)
              }
         })
    });
