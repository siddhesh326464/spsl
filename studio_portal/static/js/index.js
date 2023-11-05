var tableID;

//serach tag js
const ul = document.querySelector("ul.search_item_chip");
input = document.getElementById("job_search");
var BASE_URL = $('#job_search').attr('data_source');  

let maxTags = 10,
tags = [];
let accessToken = $.cookie('access_token');
let refreshToken = $.cookie('refresh_token');
accessToken = `Bearer ${accessToken}`
const bulkSearchInsertTableData = (data,targetID,targetSpan,count) => {
    var tbody = $(`${targetID} tbody`);
    tbody.empty();
    if (data.length > 0 ){
        $.each(data, function(index, item) {
            var row = $('<tr>');
            row.append($('<td style="width: 11%;">').text(""));
            row.append($(`<td style="width: 5%;"> <a href="/jobdetail/${item.id}/">${item.id}</a></td>`));
            row.append($('<td style="width: 9%;">').text(item.quote_no));
            row.append($('<td style="width: 8%;">').text(item.submitted_date));
            row.append($('<td style="width: 10%;">').text(item.customer_name));
            row.append($('<td style="width: 8%;">').text(item.customer_no));
            row.append($('<td style="width: 9%;">').text(item.proof_request_type));
            row.append($('<td style="width: 9%;">').text(item.logo_name));
            row.append($('<td style="width: 10%;">').text(item.campaign));
            row.append($('<td style="width: 13%;">').text(item.rep_no));
            tbody.append(row);
        });
    }
    else {
        var row = $('<tr>');
        row.append($('<td style="width: 11%;">').text("Job Not found"));
        tbody.append(row);
    }
    $(targetSpan).text(`(${count})`)
    $(`${targetID}`).parent().parent().parent().find('span.t_count').text(`${count}`)

}
const callJobListAPI = (endPoint) => {
    debugger;
    $.ajax({
        "url": endPoint,
        "method": "GET",
        "headers": {
            "Accept": "application/json",
            "Authorization": accessToken
          },
        success: (res) => {
            $('.job_dropdown').fadeOut()
            let statusList = res.response;
            statusName = $('#jobStatus').attr('data-name').split(',')
            let categories = [];
            statusName.map(s => {
                let data = { key: s, targetID: `[data-source='${s}']`,targetSpan:`span[data-id='${s}']`}
                categories.push(data);
            });
            categories.forEach(category => {
                const data = statusList[category.key];
                const count = statusList['total_count'][category.key];
                bulkSearchInsertTableData(data, category.targetID,category.targetSpan,count);
            });
            initiatePagination();
        }
    });
}



function createTag() {
    let endPoint = BASE_URL + '?';
    ul.querySelectorAll("li").forEach(li => li.remove());
    debugger;
    tags.slice().reverse().forEach(tag => {
      endPoint += `${tag.param}=${tag.value}&`;
      let tagName = tag.name === 'all' ? `${tag.value}` : `${tag.name}:${tag.value}`;
      let liTag = `<li class='d-flex align-items-center justify-content-center' data-source='${tagName}'>${tagName} <i class="fa fa-times d-flex align-items-center justify-content-center" onclick="remove(this, '${tag.param}','${tag.value}')"></i></li>`;
      ul.insertAdjacentHTML("afterbegin", liTag);
    });
    callJobListAPI(endPoint);   
  }

// function searchicon() {
//     createTag();
//   }

function remove(element, tagParam,tagValue){
    tags = tags.filter((t) => t.param != tagParam || t.value != tagValue)
    element.parentElement.remove();
    if(tags.length == 0){
        window.location.reload()
    }
    endPoint = BASE_URL + '?'; 
    tags.slice().reverse().forEach(tag =>{
        endPoint += `${tag.param}=${tag.value}&`
    });
    callJobListAPI(endPoint);
}

function addTagEnter(e){
    if (e.target.value.trim()){
        $('.job_dropdown').fadeIn();
        $('.search_val').text(e.target.value);
        $('#searchfor').attr('data-source',e.target.value); 
    }
    else{
        $('.job_dropdown').fadeOut()
    }
    if((e.key == "Backspace") && tags.length > 0) {
        let removeTag = tags.pop();
        let tagName = removeTag.name == 'all' ? `${removeTag.value}` : `${removeTag.name}:${removeTag.value}`
        $(`.search_item_chip li[data-source='${tagName}']`).remove();
        if(tags.length == 0){
            window.location.reload()
        }
        endPoint = BASE_URL + '?'; 
        tags.slice().reverse().forEach(tag =>{
            endPoint += `${tag.param}=${tag.value}&`
        });
        callJobListAPI(endPoint);
    }

    if(e.key == "Enter"){
        debugger;
        let tag = e.target.value.replace(/\s+/g, ' ').trim();
        if(tag.length > 0 &&!tags.filter(t => t.value == tag).length){
            tags = tags.filter(t => t.name == 'all');
            tags.map(t => {
                $( `.search_item_chip li[data-source='${t.value}']`).remove();
            })
            tags = tags.filter(t => t.name != 'all');
            if(tags.length < 10){
                data = {
                    name : 'all',
                    value : tag,
                    param : 'all'
                }
                tags.push(data);
                createTag();

                $(".job_dropdown").fadeOut();
            }
        }
        e.target.value = "";
    }
}



input.addEventListener("keyup", addTagEnter);
$('.search_form').on('submit',(e) => {
    e.preventDefault();

})

// ################################
function addTag(e) {
    if (e.target.value.trim()) {
      $('.job_dropdown').fadeIn();
      $('.search_val').text(e.target.value);
      $('#searchfor').attr('data-source', e.target.value);
    } else {
      $('.job_dropdown').fadeOut();
    }
  
    if (e.key === 'Backspace' && tags.length > 0) {
      const removeTag = tags.pop();
      const tagName = removeTag.name === 'all'
        ? removeTag.value
        : `${removeTag.name}:${removeTag.value}`;
      $(`.search_item_chip li[data-source='${tagName}']`).remove();
      if (tags.length === 0) {
        window.location.reload();
      }
      const endPoint = BASE_URL + '?';
      tags.slice().reverse().forEach((tag) => {
        endPoint += `${tag.param}=${tag.value}&`;
      });
      callJobListAPI(endPoint);
    }
  
    const searchIcon = document.getElementById("searchIcons");
    searchIcon.addEventListener('click',function(){
      debugger;
      const tag = e.target.value.replace(/\s+/g, ' ').trim();
      if (tag.length > 0 && !tags.filter((t) => t.value === tag).length) {
        tags = tags.filter((t) => t.name === 'all');
        tags.map((t) => {
          $(`.search_item_chip li[data-source='${t.value}']`).remove();
        });
        tags = tags.filter((t) => t.name !== 'all');
        if (tags.length < 10) {
          const data = {
            name: 'all',
            value: tag,
            param: 'all',
          };
          tags.push(data);
          createTag();
  
          $(".job_dropdown").fadeOut();
        }
      }
      e.target.value = '';
    
    })
  }
  
  input.addEventListener('click', addTag);
  $('.search_form').on('submit', (e) => {
    e.preventDefault();
  });
  
// ##############


$(document).on('click', function (e) {
    if ($(e.target).closest(".job_dropdown").length === 0) {
        $('#job_search').val("")
        $(".job_dropdown").fadeOut();
    }
});

$('.list-group-item').on('click',(e) => {
    col_name = $(e.target).attr('data-source');
    param_name = $(e.target).attr('data-param');
    col_name = col_name == undefined ? 'all' : col_name;
    param_name = param_name == undefined ? 'all' : param_name;
    let searchText = $('.search_item_chip input').val();
    if (col_name == 'all'){
        // debugger;
        removeTags = tags;
        removeTags.map(t => {
            $( `.search_item_chip li[data-source='${t.value}']`).remove();
        });
        tags = [];
    }
    else{
        // debugger;
        removeTags = tags.filter(t => t.name == 'all' || t.name == col_name);
        removeTags.map(t => {
            // debugger;
            let tagName = t.name == 'all' ? `${t.value}` : `${t.name}:${t.value}`
            $( `.search_item_chip li[data-source='${tagName}']`).remove();
        });
        tags = tags.filter(t => t.name != 'all' && t.name != col_name);
    }
    if (!tags.filter(t => t.value == searchText && t.name == col_name).length){
        data = {
            name : col_name,
            value : searchText,
            param : param_name
        }
        tags.push(data);
        createTag();
    }
});
// $(document).ready(function(){
    let jobStatus = $('#jobStatus');    
    const pagination = (startLimitID,endLimitID,totalCountCls,pageNumberID,prevBtnID,nextBtnID,jobStatusUrl) => {
        let startLimit = $(`${startLimitID}`);
        let endLimit = $(`${endLimitID}`);
        let totalCount = $(`${totalCountCls}`);
        let pageNumber = $(`${pageNumberID}`);
        let prevBtn = $(`${prevBtnID}`);
        let nextBtn = $(`${nextBtnID}`);
        let jobStatusEndPoint = $(`${jobStatusUrl}`).attr('href');
        let totalCountValue = parseInt(totalCount.text());
        let pageLimit = totalCountValue < 10 ? totalCountValue : 10;
        var currentPage = 1;
        // debugger;
        let maxPage = totalCountValue <= 10 ?  1 : Math.ceil(totalCountValue/pageLimit);
        pageNumber.text(currentPage);
        startLimit.text(currentPage - 1);
        endLimit.text(currentPage * pageLimit);
        if (maxPage <=1){
            nextBtn.attr('disabled',true);
            prevBtn.attr('disabled',true)
        }

        let accessToken = $.cookie('access_token');
        accessToken = `Bearer ${accessToken}`
        
        prevBtn.unbind('click').on('click',() => {
            currentPage -= 1
            currentPage == 1 ? startLimit.text(0) : startLimit.text(parseInt(startLimit.text() - pageLimit))
            endLimit.text(currentPage * pageLimit);
            currentPage < maxPage ? nextBtn.attr('disabled',false) : nextBtn.attr('disabled',true)
            currentPage == 1 ? prevBtn.attr('disabled',true) : prevBtn.attr('disabled',false)
            pageNumber.text(currentPage);
            let endpointUrl = jobStatusEndPoint + `?page=${currentPage}&limit=${pageLimit}`;
            tags.slice().reverse().forEach(tag =>{
                endpointUrl += `&${tag.param}=${tag.value}`
            });
            let targetTableId = prevBtn.attr('data-table');
            tableID = targetTableId;
            MakeGetCall(endpointUrl,accessToken,nextBtn);
        });
    
        nextBtn.unbind('click').on('click',() => {
            // debugger;
            currentPage += 1
            startLimit.text(parseInt(endLimit.text()) + 1);
            let endLimitCount = currentPage == maxPage ? totalCountValue : currentPage * pageLimit
            endLimit.text(endLimitCount);
            currentPage > 1 ? prevBtn.attr('disabled',false) : prevBtn.attr('disabled',true)
            currentPage == maxPage ? nextBtn.attr('disabled',true) : nextBtn.attr('disabled',false)
            pageNumber.text(currentPage);
            let endpointUrl = jobStatusEndPoint + `?page=${currentPage}&limit=${pageLimit}`;
            tags.slice().reverse().forEach(tag =>{
                endpointUrl += `&${tag.param}=${tag.value}`
            });
            let targetTableId = nextBtn.attr('data-table');
            tableID = targetTableId;
            MakeGetCall(endpointUrl,accessToken,nextBtn);
        });
    }
    const initiatePagination = () => {
        let jobStatusList = jobStatus.attr('data');
        jobStatusList = jobStatusList.split(',');
        jobStatusList.map((value,index) => {
            let start_limit = `#start_limit_${index + 1}`
            let end_limit = `#end_limit_${index + 1}`
            let total_count = `.total_count_${index + 1}`
            let prev = `#prev_${index + 1}`
            let next = `#next_${index + 1}`
            let pagenumber = `#pagenumber_${index + 1}`
            let jobstatusurl = `.api-url_${index + 1}`
            pagination(start_limit,end_limit,total_count,pagenumber,prev,next,jobstatusurl);
        });
    }
    initiatePagination();

    const bulkInsertTableData = (data,targetID) => {
        var tbody = $(`#${targetID} tbody`);
        tbody.empty();
        if (data.length > 0 ){
            $.each(data, function(index, item) {
                var row = $('<tr>');
                row.append($('<td style="width: 11%;">').text(""));
                row.append($(`<td style="width: 5%;"> <a href="/jobdetail/${item.id}/">${item.id}</a></td>`));
                row.append($('<td style="width: 9%;">').text(item.quote_no));
                row.append($('<td style="width: 8%;">').text(item.submitted_date));
                row.append($('<td style="width: 10%;">').text(item.customer_name));
                row.append($('<td style="width: 8%;">').text(item.customer_no));
                row.append($('<td style="width: 9%;">').text(item.proof_request_type));
                row.append($('<td style="width: 9%;">').text(item.logo_name));
                row.append($('<td style="width: 10%;">').text(item.campaign));
                row.append($('<td style="width: 13%;">').text(item.rep_no));
                tbody.append(row);
            });
        }
        else {
            var row = $('<tr>');
            row.append($('<td style="width: 11%;">').text("Job Not found"));
            tbody.append(row);
        }
    }
    const MakeGetCall = (url,token,nextBtn) => {
        $.ajax({
            "url": url,
            "method": "GET",
            "headers": {
                "Accept": "application/json",
                "Authorization": token
              },
            success: function (data, status, xhr) {
                bulkInsertTableData(data.response,tableID);
                tableID = undefined;
            },
            error: function(jqXHR, textStatus, errorThrown){
                // debugger;
                console.log(errorThrown)
            }
          });
    }


// });
// campaign call api
     // add btn
//      $('#campaign_name').on('input', function() {
//         var inputText = $(this).val().trim();
//         inputText.length > 0 ? $('#campaign_add_btn').prop('disabled', false) : $('#campaign_add_btn').prop('disabled', true);
//    });
//    $('.close_btn').on('click',()=>{
//         if ($('#id_campaign option:selected').val() == ""){
//              $('#campaign_name').val("");
//              $('#campaign_name').val().trim().length > 0 ? $('#campaign_add_btn').prop('disabled', false) : $('#campaign_add_btn').prop('disabled', true);
//         }
//    })
//    $('#id_campaign').on('change',function(){
//         console.log("in")
//         let l = $('#id_campaign option:selected')
//         let value = l.text()
//         let id = l.val()
//         if (id !=""){
//              $('.fa-plus').toggleClass('fa-pencil fa-plus')
//              $('#campaign_name').val(value)
//              $('#campaign_name').attr('data-id',id)
//              $('#campaign_add_btn').html('Save')
//              $('#campaign_add_btn').on('click',function(){
//                   let changed_value = $('#campaign_name').val()
//                   console.log(changed_value)
//              })
//         }else{
//              $('.fa-pencil').toggleClass('fa-plus fa-pencil')
//              $('#campaign_name').val("")
//              $('#campaign_name').attr('data-id',"")
//         }
//    });
//    $('#campaign_add_btn').unbind('click').on('click',function(){
//         let campaignName = $('#campaign_name').val();
//         let id = $('#campaign_name').attr('data-id') == "" ? "" : $('#campaign_name').attr('data-id');
//         let csrfToken = $('input[name=csrfmiddlewaretoken]').val();
//         let formData = new FormData()
//         formData.append('id',id)
//         formData.append('name',campaignName)
//         formData.append('csrfmiddlewaretoken',csrfToken);
//         let path = window.location.href;
//         $('.page_loader').css('display','flex');
//         debugger;
//         $.ajax({
//              url: path, 
//              type: "POST",
//              data: formData,
//              processData: false,
//              contentType: false,
//              success: function (data, textStatus, xhr) {
//                   debugger;
//                   $('.page_loader').css('display','none');
//                   // let name = data.response['name']
//                   if (data.status === 'error'){
//                        alert(data.msg);
//                        return false;
//                   }
//                   $(".close_btn").click();
//                   let optionHtml = `<option value="${data.res.id}" data-select2-id="${data.res.id}" selected>${data.res.name}</option>`
//                   $('#id_campaign').append(optionHtml);
//              },
//              error: function (textStatus, errorThrown) {
//                   $('.page_loader').css('display','none');
//                   console.log(textStatus,errorThrown)
//              }
//         })
//    });
// // campaign end