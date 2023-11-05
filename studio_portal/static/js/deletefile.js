$(document).ready(function(){
    $('#deletefilebtn').on('click',function(){
        let res = confirm("Are you sure you want to delete this file ")
        if(res==true){
            let url = $('.job_files label').attr('data-url')
        } 

    })

})


