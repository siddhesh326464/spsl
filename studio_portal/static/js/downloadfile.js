$(document).ready(function(){
    $('.job_files label,#chat_file').on('click',function(e){
        e.preventDefault();
        let url = $(this).attr('data-url');
        $('.page_loader').css('display','flex');
        $.ajax({
            url: url, 
            type: "GET",
            success: function (data, textStatus, xhr){
                $('.page_loader').css('display','none');
                if (data.status == 'error'){
                    alert(data.msg);
                    return false
                }
                url = data['msg']
                window.location.href = url;
                $('.page_loader').css('display','none');
            },
            error:function(textStatus, errorThrown){
                $('.page_loader').css('display','none');
                console.log("Something went wrong",errorThrown)
            }
        })
    })
    
}) 



$(document).ready(function(){
    $('.chat_wrapper .msg_wrapper ul li label[data-chat-url]').on('click',function(){
        // e.preventDefault();
        let url = $(this).attr('data-chat-url');
        $('.page_loader').css('display','flex');
        debugger;
        $.ajax({
            url: url, 
            type: "GET",
            success: function (data, textStatus, xhr){
                $('.page_loader').css('display','none');
                if (data.status == 'error'){
                    alert(data.msg);
                    return false
                }
                url = data['msg']
                window.location.href = url;
                $('.page_loader').css('display','none');
            },
            error:function(textStatus, errorThrown){
                $('.page_loader').css('display','none');
                console.log("Something went wrong",errorThrown)
            }
        })
    })
})