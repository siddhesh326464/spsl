const ul = document.querySelector("ul.search_item_chip"),
input = document.querySelector("input");
var BASE_URL = $('#job_search').attr('data_source');
let maxTags = 10,
tags = [];
const bulkInsertTableData = (data,targetID,targetSpan,count) => {
    var tbody = $(`${targetID} tbody`);
    tbody.empty();
    if (data.length > 0 ){
        $.each(data, function(index, item) {
            var row = $('<tr>');
            row.append($('<td style="width: 11%;">').text(""));
            row.append($('<td style="width: 5%;">').text(item.id));
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
    $.ajax({
        url: endPoint,
        type: "GET",
        dataType: "json",
        success: (res) => {
            let statusList = res.response;
            statusName = $('#jobStatus').attr('data-name').split(',')
            let categories = [];
            statusName.map(s => {
                let data = { key: s, targetID: `[data-source='${s}']`,targetSpan:`span[data-id='${s}']`}
                categories.push(data);
            })
            categories.forEach(category => {
                const data = statusList[category.key];
                const count = statusList['total_count'][category.key];
                bulkInsertTableData(data, category.targetID,category.targetSpan,count);
                // initiatePagination();
            });
        }
    });
}

function createTag(){
    endPoint = BASE_URL + '?';
    ul.querySelectorAll("li").forEach(li => li.remove());
    tags.slice().reverse().forEach(tag =>{
        endPoint += `${tag.param}=${tag.value}&`
        let tagName = tag.name == 'all' ? `${tag.value}` : `${tag.name}:${tag.value}`
        let liTag = `<li class='d-flex align-items-center justify-content-center' data-source='${tagName}'>${tagName} <i class="fa fa-times d-flex align-items-center justify-content-center" onclick="remove(this, '${tag.param}','${tag.value}')"></i></li>`;
        ul.insertAdjacentHTML("afterbegin", liTag);
    });
    callJobListAPI(endPoint);
    
}
function remove(element, tagParam,tagValue){
    tags = tags.filter((t) => t.param != tagParam || t.value != tagValue)
    element.parentElement.remove();
    endPoint = BASE_URL + '?'; 
    tags.slice().reverse().forEach(tag =>{
        endPoint += `${tag.param}=${tag.value}&`
    });
    callJobListAPI(endPoint);
}

function addTag(e){
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
        endPoint = BASE_URL + '?'; 
        tags.slice().reverse().forEach(tag =>{
            endPoint += `${tag.param}=${tag.value}&`
        });
        callJobListAPI(endPoint);
    }
  
    if(e.key == "Enter"){
        // if (tags.length==4){
        //     alert("You can search only 4 columns at a time");
        //     return false
        // }
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

input.addEventListener("keyup", addTag);
$('.search_form').on('submit',(e) => {
    e.preventDefault();
})

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