$(document).ready(function() {
	$(".btn-primary").click(function(){
        var elements = $(this).parent().parent().next();
        while(elements.attr('class') === 'name'){
        trigger(elements);
        elements = elements.next();
        }
    });

    // switch the status of display
    function trigger(element) {
        if (element.css('display') !== 'none') {
          element.hide();
        } else {
          element.show();
        }
    }

    $("#submit").click(function(){
    	var interest = getInnerHTML("interest");
    	var zip_code = getInnerHTML("zip_code");
    	var user = getInnerHTML("user");
        var ointerest = getInnerHTML("ointerest");
        var ozip_code = getInnerHTML("ozip_code");
        var friend = getInnerHTML("friend");
        window.location.href = "http://0.0.0.0:8111/" + "?interest="+interest+"&zip_code="+zip_code+"&user="+user+"&ointerest="+ointerest+"&ozip_code="+ozip_code+"&friend="+friend;
    });
    $("#submit2").click(function(){
    	var interest = getInnerHTML("interest");
    	var zip_code = getInnerHTML("zip_code");
    	var user = getInnerHTML("user");
        var ointerest = getInnerHTML("ointerest");
        var ozip_code = getInnerHTML("ozip_code");
        var friend = getInnerHTML("friend");
        window.location.href = "http://0.0.0.0:8111/" + "?interest="+interest+"&zip_code="+zip_code+"&user="+user+"&ointerest="+ointerest+"&ozip_code="+ozip_code+"&friend="+friend;
    });
    $("#submit3").click(function(){
    	var interest = getInnerHTML("interest");
    	var zip_code = getInnerHTML("zip_code");
    	var user = getInnerHTML("user");
        var ointerest = getInnerHTML("ointerest");
        var ozip_code = getInnerHTML("ozip_code");
        var friend = getInnerHTML("friend");
        window.location.href = "http://0.0.0.0:8111/" + "?interest="+interest+"&zip_code="+zip_code+"&user="+user+"&ointerest="+ointerest+"&ozip_code="+ozip_code+"&friend="+friend;
    });

});

function getInnerHTML(input){
	var value = document.getElementById(input);
	return value[value.selectedIndex].innerHTML;
}
