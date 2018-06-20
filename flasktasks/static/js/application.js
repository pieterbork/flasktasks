function reload_list_container() {
    $.ajax({
        url: "{{ url_for('list_container') }}",
        type: 'GET',
        success: function(result) {
           $('.list_container').replaceWith(result);
        },
    });
}

$(document).on('click', '#delete-list', function(e) {
    $.ajax({
        url: $(this).attr('href'),
        type: 'DELETE',
        success: function(result) {
            $('.list-container').replaceWith(result)
        }
    })
})

$(document).on('click', '#delete-task', function(e) {
    http_delete($(this))
    return false
})

$(document).on('click', '#delete-board', function(e) {
    http_delete($(this))
    return false
})

function http_delete(element) {
    $.ajax({
        url: element.attr('href'),
        type: 'DELETE',
        success: function(result) {
            window.location.href = result;
        }
    });
}

setTimeout(function() {
    $('#flash-message').hide('slide', '1000');
}, 4000); // <-- time in milliseconds
