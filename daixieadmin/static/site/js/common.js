jQuery(document).ready(function($) {
    $('.datepicker').datetimepicker({
        autoclose: true,
        todayHighlight: 1,
        format:'yyyy-mm-dd',
        startDate:new Date(),
        daysOfWeekDisabled:[1],
        minView:2
    });
});

/*
 * order/create.html
 */
var create_order = (function(window, $){

    function getSelect2($select, formatResult, formatSelection) {
        var type = $select.attr('user_type');
        var options = {
            allowClear: true,
            initSelection: function(element, callback) {
                if(!element.val()) return;
                $.ajax({
                    url: element.attr('data-ajax-url'),
                    data: {email: element.val(), type: type},
                    success: function(ret) {
                        if(!ret.items) return;
                        callback(ret.items[0]);
                    }
                });
            },
            query: function(query) {
                var term = $.trim(query.term).toLowerCase();
                var page = query.page;

                if(term === query.element.data('select2-last-term')
                    && page === query.element.data('select2-last-page')) {
                    query.callback(query.element.data('select2-last-results'));
                    return;
                }

                query.element.data('select2-last-term', term);
                query.element.data('select2-last-page', page);

                $.ajax({
                    url: query.element.attr('data-ajax-url'),
                    data: {query: term, page: page, type: type},
                    success: function(ret) {
                        var data = {
                            results: ret.items,
                            more: page < ret.pages
                        }
                        query.callback(data);
                        query.element.data('select2-last-results', data);
                    }
                });
            },
            escapeMarkup: function(markup) {
                return markup;
            }
        }

        if(formatResult) {
            options.formatResult = formatResult;
        }

        if(formatSelection) {
            options.formatSelection = formatSelection;
        }

        $select.select2(options);
    }
    
    function _run(){

        getSelect2($('input.select[name=user_email]'));
        getSelect2($('input.select[name=cs_email]'));
        getSelect2($('input.select[name=solver_email]'));

    } /* end run*/

    return {
        run:_run
    }
})(window, jQuery);