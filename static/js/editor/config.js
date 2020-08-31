KindEditor.ready(function(K) {
    window.editor = K.create('#id_content',{
        // set width and height
        width:'800px',
        height:'200px',
        uploadJson : '/admin/upload/kindeditor',
    });
});
