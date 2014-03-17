/* =============================================================
 * jquery.daixie.js v0.0.1
 * =============================================================
 * Copyright 2014 Daixie, Inc.
 *
 * All right reserved
 * ============================================================= */

!function($){

    'use strict'; // jshint ;_;

    /* DAIXIE PLUGIN DEFINITION
     * ======================== */

    var ajaxCallbacks = {
        reload: function(){
            window.location.reload(true) 
        }
    }

    function getUserAjaxOptions(options){
        var ajaxOptions = {
            success: function(){}
        }

        if(typeof options == 'function'){
            ajaxOptions.success = options
        }else if(typeof options == 'object'){
            ajaxOptions = options
        }else if(typeof options == 'string'){
            ajaxOptions.success = ajaxCallbacks[options]
        }

        return ajaxOptions
    }
    
    function getAjaxOptions(pluginDefaultOptions, userOptions){
        var ajaxDefaultOptions = {
            dataType: 'json',
            success: function(res){
                $.daixie.toast(res.msg)
            },
            fail: $.daixie.toast
        }

        userOptions = $.extend({}, ajaxDefaultOptions, pluginDefaultOptions, getUserAjaxOptions(userOptions))

        var overrideOptions = {
            success: function(res, textStatus, jqXHR){
                if(res.status == 'ok'){
                    userOptions.success.apply(this, [res])
                }else if(res.status == 'redirect'){
                    userOptions.success.apply(this, [res])
                    window.location = res.url
                }else{
                    userOptions.fail.apply(this, [res.msg])
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                userOptions.fail.apply(this, ['操作失败'])
            },
            statusCode: {
                413: function(){
                    userOptions.fail.apply(this, ['文件过大'])
                }
            }
        }

        return $.extend({}, userOptions, overrideOptions)
    }


    /* DAIXIE STANDALONE PUBLIC APIS
     * ======================== */

    $.daixie = {
        toast: function(msg){
            $('#toasts').daixie('showStatus', msg)
        },

        ajax: function(options){
            var ajaxOptions = getAjaxOptions({}, options)

            $.ajax(ajaxOptions) 
        }
    }

    /* DAIXIE ELEMENT PUBLIC APIS
     * ======================== */
    var methods = {

        showStatus: function(msg, options){
            var $this = $(this)
            var $status = null

            if($this.is('form')){
                if($this.attr('status')){
                    $status = $('#' + $this.attr('status'))
                }else{
                    var $formStatus = $this.find('.form-status')
                    if($formStatus.length){
                        $status = $formStatus
                    }else{
                        var $modalStatus = $this.parents('.modal').find('.modal-status')
                        if($modalStatus.length){
                            $status = $modalStatus
                        }
                    }
                }
            }else{
                $status = $this
            }

            if(!$status) return

            if(!msg){
                $status.html('')
                return
            }

            options = $.extend({}, {
                status: 'important',
                autoHidden: true
            }, options || {})

            $status.html('<span class="label label-'+ options.status +'">'+ msg +'</span>')

            if(options.autoHidden){
                setTimeout(function(){
                    $status.html('')
                }, 3000)
            }
        },

        ajaxLink: function(options){
            options = options || {}
            $(this).on('click', options.delegation, function(e){
                var ajaxOptions = getAjaxOptions({
                    url: $(this).attr('href'),
                    type: 'post',
                    context: this
                }, options)

                $.ajax(ajaxOptions) 

                return false
            }) 
        },

        ajaxForm: function(options){
            options = options || {}
            $(this).on('submit', options.delegation, function(){
                var ajaxOptions = getAjaxOptions({
                    context: this,
                    fail: function(msg){
                        $(this).daixie('showStatus', msg, {status:'important'})
                    },
                    success: function(res){
                        $(this).daixie('showStatus', res.msg, {status:'info'})
                    }
                }, options)

                $(this).ajaxSubmit(ajaxOptions)

                return false
            }) 
        },

        ajaxEle: function(options){
            var $this = $(this)
            options = options || {}

            var ajaxOptions = getAjaxOptions({
                url: $this.attr('data-ajax-url'),
                type: 'get',
                data: $this.data('ajax-data') || {},
                context: this,
                success: function(res){
                    $this.data('ajax-data', res.context)

                    if($this.is('ul')){
                        $this.children('li').remove(':not(.nav-header)')

                        //$this.append(res.html)
                        
                        var $children = $('<div/>').html(res.html).children()
                        $.each($children, function(i, child){
                            $this.append($(child).hide().delay(200*i).fadeIn())
                        })
                    }else{
                        $this.html(res.html)
                    }
                },
                fail: function(msg){
                }
            }, options)

            $.ajax(ajaxOptions) 

            return false
        }
    }
   
    $.fn.daixie = function(method){
        var args = Array.prototype.slice.call(arguments, 1)
        return this.each(function(){
            methods[method].apply(this, args)
        })
    }

    /* DAIXIE DATA-API
     * ================== */

}(jQuery);

!function($){

    'use strict'; // jshint ;_;
    
    //https://gist.github.com/mathiasbynens/326491 
    $.fn.insertAtCaret = function(myValue) {
        return this.each(function() {
                var me = this;
                if (document.selection) { // IE
                        me.focus();
                        sel = document.selection.createRange();
                        sel.text = myValue;
                        me.focus();
                } else if (me.selectionStart || me.selectionStart == '0') { // Real browsers
                        var startPos = me.selectionStart, endPos = me.selectionEnd, scrollTop = me.scrollTop;
                        me.value = me.value.substring(0, startPos) + myValue + me.value.substring(endPos, me.value.length);
                        me.focus();
                        me.selectionStart = startPos + myValue.length;
                        me.selectionEnd = startPos + myValue.length;
                        me.scrollTop = scrollTop;
                } else {
                        me.value += myValue;
                        me.focus();
                }
        });
    };
 
}(jQuery);
