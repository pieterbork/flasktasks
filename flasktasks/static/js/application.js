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
    console.log(element.attr('href'))
    $.ajax({
        url: element.attr('href'),
        type: 'DELETE',
        success: function(result) {
            window.location.href = result;
        }
    });
}

$('.item-list').sortable({
    group: 'list-group',
    pullPlaceholder: false,
    connectWith: '.item-list',
    stop: function(event, ui) {
        var url_parts = $(ui.item).find('a').attr('href').split("/")
        var task = url_parts[url_parts.length - 1]
        var list_parts = $(ui.item).closest('.list').find('a').attr('href').split("/")
        var list = list_parts[2]
        var url = '/tasks/' + task + '/set_list/' + list + '/order/' + $(ui.item).index()

        $.ajax({
            url: url,
            type: 'GET',
            success: function(result) {
                console.log('yay')
            }
        })
    }
});
