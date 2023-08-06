layui.use('upload', function () {
    var $ = layui.jquery
        , upload = layui.upload;

    //拖拽上传
    upload.render({
        elem: '#upload_docx'
        , url: '/autopost/convert_docx/'
        , accept: 'file'
        , exts: 'docx|doc' //只允许上传docx
        , done: function (res) {
            if (res.code == 200) {
                // let content = $('div[data-field-id="id_content"]').find('.simditor-body');
                // content.html(res.data);
                editorList['id_content'].setValue(res.data);
            }
        }
    });

});

