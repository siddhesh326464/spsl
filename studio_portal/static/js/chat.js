$(document).ready(function(){
    $('#id_msg').on('keyup',function(){
        let msgValue = $(this).val().trim();
        let isDisabled = msgValue.length == 0 ? true : false;
        $('#send,#attachment').attr('disabled',isDisabled);
        isDisabled ? $('#attach').addClass('disabled_attachement') : $('#attach').removeClass('disabled_attachement')
    })
    let path=window.location.href
    let accessToken = $.cookie('access_token');
    let csrfToken = $('#chat_form input[name=csrfmiddlewaretoken]').val();
    $('#send').on('click',function(e){
        e.preventDefault()
        let formData = new FormData();
        let msg = $('#id_msg').val();
        let attachement = $('#attachment')[0].files[0];
        formData.append('attachment',attachement);
        formData.append('details',msg);
        formData.append('csrfmiddlewaretoken',csrfToken);
        $('.page_loader').css('display','flex');
        $.ajax({
            url: path, 
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data, textStatus, xhr) {
                $('.page_loader').css('display','none');
                let msg = data.response['details'];
                let attachement = data.response['attachment'];
                let filename = data.response['filename'];
                let user_id = data.response['user_id'];
                let log_datetime = data.response['log_datetime'];
                // let htmlAttachment = attachement ? `<li><a href="${attachement}">${filename}</a></li>` : ""
                let htmlAttachment = attachement ? `<li><label for=""  data-url="/downloadfile/${data.response.attachment.file_type}/${data.response.id}" id='chat_file' >${filename}</label></li>` : ""
                let msgContent = `<div class="msg_wrapper my-2">
                                    <div class="sender_header">Note by <span class='sender_name'>${user_id}</span> - ${log_datetime}</div>
                                    <ul class="msg no-bullets">
                                    <li>${msg}</li>
                                    ${htmlAttachment}
                                    </ul>
                                </div>`
                $(".chat_wrapper").prepend(msgContent);
                $('#id_msg').val("");
                $('#attachment').val("");
                $('#file_name').text("")
                let msgValue = $("#id_msg").val().trim();
                let isDisabled = msgValue.length == 0 ? true : false;
                $('#send,#attachment').attr('disabled',isDisabled);
                isDisabled ? $('#attach').addClass('disabled_attachement') : $('#attach').removeClass('disabled_attachement')
            },   
            error: function (textStatus, errorThrown) {
                $('.page_loader').css('display','none');
                $('#id_msg').val("");
                let msgValue = $("#id_msg").val().trim();
                let isDisabled = msgValue.length == 0 ? true : false;
                $('#send,#attachment').attr('disabled',isDisabled);
                isDisabled ? $('#attach').addClass('disabled_attachement') : $('#attach').removeClass('disabled_attachement')
                console.log("error while sending message",errorThrown);  
            }    
        });
    })
    $('#attachment').on('change',function(){
        let file=$(this)[0].files[0]
        if(file){
            $('#file_name').text(file.name) 
        }   
    })
});

