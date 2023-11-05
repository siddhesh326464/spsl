$(document).ready(function(){
     var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
     var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl)
     });
     
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

     let l = $('#id_campaign option:selected')
     let value = l.text()
     let id = l.val()
     if (id !=""){
          $('.campaign_btn').attr('disabled',false);
          $('#campaign_name').val(value)
          $('#campaign_name').attr('data-id',id)
          $('#campaign_add_btn').html('Save')
          // $('#campaign_add_btn').on('click',function(){
          //      let changed_value = $('#campaign_name').val()
          // })
     }else{

          $('.campaign_btn').attr('disabled',true);
          $('#campaign_name').val("")
          $('#campaign_name').attr('data-id',"")
     }

     //validation of create page
     $('#savebtn,#savebtn1').unbind('click').on("click",function(e){
          e.preventDefault();
          let errorHtml = `<div class="error_msg text-danger">This field is required.</div>`
          let emailErrorHtml = `<div class="error_msg text-danger">Please enter a valid email address.</div>`
          let isError = false;
          $('.form-control:required').map((idx,elm) => {
               if (!$(elm).val()){
                    isError = true;
                    $(elm).next().remove();
                    $(elm).after(errorHtml);
               }
               else{
                    $(elm).next().remove();
                    isError = isError;
               }
          });
          if ($('#id_proof_request_type option:selected').attr('value') == '0'){
               isError = true;
               $('#id_proof_request_type').next().remove();
               $('#id_proof_request_type').after(errorHtml);
          }
          else{
               $('#id_proof_request_type').next().remove();
               isError = isError;
          }
          $('.dynamic-form input[data-id=item_id').map((idx,elm) =>{
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
          $('#id_submitted_files').map((idx,elm)=>{
               if (!$(elm).val()){
                    isError = true;
                    $(elm).next().next().remove();
                    $(elm).next().after(errorHtml)
               }
               else{
                    $(elm).next().next().remove();
                    isError=isError
               }
          });

          if ($('#id_send_art_to_customer').is(':checked')){
               let customerEmail = $('#id_customer_email').val()
               if(customerEmail==""){
                    isError = true;
                    $('#id_customer_email').next().remove()
                    $('#id_customer_email').after(errorHtml)
               }else{
                    let newCustomeremail = $('#id_customer_email').val();
                    var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i
                    if(!pattern.test(newCustomeremail)){
                         isError=true
                         $('#id_customer_email').next().remove()
                         $('#id_customer_email').after(emailErrorHtml)
                    }else{
                         $('#id_customer_email').next().remove()
                         isError=isError
                    }     
               }
          }
          $('#id_send_art_to_customer').on('change',function(){
               if ($(this).is(':checked')){
                    let customerEmail = $('#id_customer_email').val()
                    if(customerEmail.trim().length>0){
                         $('#id_customer_email').next().remove()
                         isError=isError
                    }
               }
          });
          if (isError) {
               alert("Please complete the mandatory fields.");
           }
           else {
               $('#createjobform').submit();
           }
     });

     
});
// const removeFile = (e) => {
//      let fileName = $(e).attr('data-source');
//      let parentId = $(e).attr('data-id')
//      let fileList = $(`#${parentId}`)[0]
//      let fileArray = Array.from(fileList.files);
//      let finalList = fileArray.filter(f => f.name != fileName);
//      let newFileList = new DataTransfer();
//      finalList.map(f=>newFileList.items.add(f))
//      fileList.files = newFileList.files

//      $(e).parent().closest('div').remove();
//      submitted_file[$(e).attr('data-id')] = submitted_file[$(e).attr('data-id')].filter(f=>f.name!=$(e).attr('data-source'));
// }

// const setItemFile = (file_type,key,value) => {
//      let serializedFiles = value.map(function(file) {
//           return {
//           name: file.name,
//           type: file.type,
//           size: file.size,
//           lastModified: file.lastModified
//           };
// });

// let files = getFileList('submitted_file',key)
// var filesJson = undefined;
// if (!files){
//      let fileDict = {};
//      fileDict[key] = serializedFiles;
//      filesJson = JSON.stringify(fileDict);
// }
// else {
//      files[key] = serializedFiles;
//      filesJson = JSON.stringify(files);
// }
// localStorage.setItem(file_type,filesJson)
// }

// const getFileList = (file_type,key) => {
//      var filesJson = localStorage.getItem(file_type);
//      if (filesJson) {
//           var serializedFiles = JSON.parse(filesJson);
//           return serializedFiles
//      }
//      return false
// }

// const convertObjToFileList = (files) => {
//      var fileList = new DataTransfer();
//      files.forEach(function(file) {
//           var newFile = new File([], file.name, { type: file.type, lastModified: file.lastModified });
//           fileList.items.add(newFile);
//      });
//      return fileList
// }
// let submitted_file = {}
// const handleFileOnChange = (e) => {
//      $(e).next().empty()
//      let Files = Array.from(e.files);
//      let fileName = submitted_file[e.id] != undefined ? submitted_file[e.id].map(f=>f.name) : []
//      submitted_file[e.id] = submitted_file[e.id] != undefined ? [... new Set(submitted_file[e.id].concat(Files.filter(f=> !fileName.includes(f.name))))] : Files;
//      let newFileList = new DataTransfer();
//      submitted_file[e.id].map(f=>newFileList.items.add(f))
//      e.files = newFileList.files
//      $.each(submitted_file[e.id],(id,elm) => {
//                let alertBox = `<div class="alert alert-secondary alert-dismissible fade show py-1 px-2 mb-1" role="alert">
//                                    <p class='mb-0 alert-file-name'>${elm.name}</p>
//                          <span class="alert-close-btn" onclick = "removeFile(this)" data-source='${elm.name}' data-id="${e.id}"><i class="fa fa-times text-danger"></i></span>
//                          </div>`
//                $(e).next().append(alertBox)
//      })
// };

  
