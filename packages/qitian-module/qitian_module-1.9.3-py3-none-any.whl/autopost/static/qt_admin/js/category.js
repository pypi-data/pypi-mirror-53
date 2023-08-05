(function ($) {
    $(function () {
        if ($('#id_parent').length > 0) {
            var opt_dom = $('#id_parent');
        } else if ($('#id_category').length > 0) {
            var opt_dom = $('#id_category');
        }
        $('#id_site').change(function () {
            let site_id = $(this).val();
            $.get('/autopost/category_tree/' + site_id, function (data) {
                render_category(data, opt_dom);
            });
        });
        $.get('/autopost/category_tree/' + $('#id_site').val(), function (data) {
            render_category(data, opt_dom);
        });
    });


    /**
     * 渲染分类下拉
     * @param data
     */
    function render_category(data, opt_dom) {
        let select_id = opt_dom.val();
        opt_dom.empty();
        let category_tree = data['tree'];
        opt_dom.append('<option value>-----</option>');
        $.each(category_tree, function (index, item) {
            $.each(item, function (i, node) {
                let ckd_str = '';
                if(select_id==node.id){
                    ckd_str = 'selected';
                }
                let opt = $('<option value="' + node.id + '" '+ckd_str+'>' + node.name + '</option>');
                opt_dom.append(opt);
            })
        });
    }
})(django.jQuery);
