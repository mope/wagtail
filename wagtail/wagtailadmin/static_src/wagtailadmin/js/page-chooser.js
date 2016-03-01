function createPageChooser(id, pageTypes, openAtParentId) {
    var chooserElement = $('#' + id + '-chooser');
    var pageTitle = chooserElement.find('.title');
    var input = $('#' + id);
    var editLink = chooserElement.find('.edit-link');

    $('.action-choose', chooserElement).click(function() {
        var initialUrl = window.chooserUrls.pageChooser;
        if (openAtParentId) {
            initialUrl += openAtParentId + '/';
        }

        ModalWorkflow({
            url: initialUrl,
            urlParams: { page_type: pageTypes.join(',') },
            responses: {
                linkChosen: function(pageData) {
                    input.val(pageData.data.id);
                    openAtParentId = pageData.parentId;
                    pageTitle.text(pageData.title);
                    chooserElement.removeClass('blank');
                    editLink.attr('href', pageData.editUrl);
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        openAtParentId = null;
        chooserElement.addClass('blank');
    });
}
