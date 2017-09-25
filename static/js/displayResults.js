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