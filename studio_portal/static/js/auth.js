// window.addEventListener('beforeunload', () => {
//     $('.page_loader').css('display','flex');
// });

// window.addEventListener('load', ()=>{
//     $('.page_loader').css('display','none');
// });
window.addEventListener('beforeunload', () => {
    $('.page_loader').css('display', 'flex');
  });
  
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      $('.page_loader').css('display', 'none');
    }
  });
// $(document).ready(function(){
//     let accessToken = $.cookie('access_token');
//     let refreshToken = $.cookie('refresh_token');
//     accessToken = `Bearer ${accessToken}`
//     $("#logout").click(function(e) {
//         e.preventDefault();
//         let logoutEndpoint = $(e.target).attr('data-source');
//         let action = confirm('Are you sure you want to logout.')
//         debugger;
//         if (action) {
//             $.ajax({
//                 "url": logoutEndpoint,
//                 "method": "POST",
//                 "headers": {
//                     "Accept": "application/json",
//                     "Authorization": accessToken
//                 },
//                 data: {
//                     'refresh': refreshToken
//                 },
//                 success: function(response) {
//                     debugger;
//                     $.removeCookie('access_token',{ path: '/' })
//                     $.removeCookie('refresh_token',{ path: '/' })
//                     window.location.replace('/auth/login/')
//                 },
//                 error: function(error) {
//                     console.error(error);
//                 }
//             });
//         }
//     });
// });



$(document).ready(function() {
    let accessToken = $.cookie('access_token');
    let refreshToken = $.cookie('refresh_token');
    accessToken = `Bearer ${accessToken}`
    let csrftoken = $.cookie('csrftoken'); // Retrieve the CSRF token from the cookie
    $("#logout").click(function(e) {
        e.preventDefault();
        let logoutEndpoint = $(e.target).attr('data-source');
        let action = confirm('Are you sure you want to logout.');
        if (action) {
        $('.page_loader').css('display','flex');
            $.ajax({
                "url": logoutEndpoint,
                "method": "POST",
                "headers": {
                    "Accept": "application/json",
                    "Authorization": accessToken,
                    "X-CSRFToken": csrftoken // Include the CSRF token in the headers
                },
                data: {
                    'refresh': refreshToken
                },
                success: function(response) {
                    $('.page_loader').css('display','none');
                    $.removeCookie('access_token', { path: '/' })
                    $.removeCookie('refresh_token', { path: '/' })
                    window.location.replace('/auth/login/')
                },
                error: function(error) {
                    console.error(error);
                }
            });
        }
    });
});
