$("#delete-task").click(function() {
    http_delete($(this));
    return false;
});

$("#delete-board").click(function() {
    http_delete($(this));
    return false;
});

$('.item-list').sortable({
    group: 'list-group',
    pullPlaceholder: false,
    connectWith: '.item-list'
});

$(document).bind("sortstop", function(event) {
    console.log("SORT STOPPED!", event)
})

$(document).on('click', '.up', function(e) {
    var list = $(this).closest('.list')
    var task = $(this).closest('.list-group-item').attr('href')
    var url = task + "/set_order/up"
    $.ajax({
        url: url,
        type: 'GET',
        success: function(result) {
            $(list).replaceWith(result)
        }
    })
    return false
});

$(document).on('click', '.down', function(e) {
    var list = $(this).closest('.list')
    var task = $(this).closest('.list-group-item').attr('href')
    var url = task + "/set_order/down"
    $.ajax({
        url: url,
        type: 'GET',
        success: function(result) {
            $(list).replaceWith(result)
        }
    })
    return false
});

$(document).on('click', '.next', function(e) {
    var board = $(this).closest('.board')
    var task = $(this).closest('.list-group-item').attr('href')
    var url = task + "/set_list/next"
    $.ajax({
        url: url,
        type: 'GET',
        success: function(result) {
            $('.list-container').replaceWith(result)
        }
    })
    return false
});

$(document).on('click', '.prev', function(e) {
    var board = $(this).closest('.board')
    var task = $(this).closest('.list-group-item').attr('href')
    var url = task + "/set_list/prev"
    $.ajax({
        url: url,
        type: 'GET',
        success: function(result) {
            $('.list-container').replaceWith(result)
        }
    })
    return false
});



function http_delete(element) {
    $.ajax({
        url: element.attr('href'),
        type: 'DELETE',
        success: function(result) {
            window.location.href = result;
        }
    });
}
