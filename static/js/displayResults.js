$(document).ready(function () {
    $('.reason').hide();
    $('.score').hide();
});
function hideClass(button, className) {
    $('.'+className).toggle();
    console.log(button.html());
    if(button.html() == "Show Scores"){
        button.html("Hide Scores");
    }else{
        button.html("Show Scores");
    }
}
function readFile(Filename) {
    $.get(Filename, function (data) {
        var win = window.open();
        console.log(win);
        win.document.open();
        str =
        '<head>'+
        '<meta charset="UTF-8">'+
        '<title>Opened File!</title>'+
        '<script src="../static/js/jquery-3.2.1.min.js"></script>'+
        '<link rel="stylesheet" href="../static/css/openFile.css">'+
        '</head>'+
        '<body>';
        win.document.write(str);
        lines = data.split("\n");
        for(i = 0; i < lines.length; i++){
            win.document.write("<p>"+lines[i]+"</p>")
        }
        win.document.close();
    })
}