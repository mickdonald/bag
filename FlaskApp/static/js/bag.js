window.onload = function(){
    dom = {};
    els = [
        "remaining",
        "warning",
        "guess",
        "result",
        "usertext"
    ]
    for(var i = 0; i<els.length; i++){
        dom[els[i]] = $("#" + els[i]);
    }
    dom.usertext.keydown(typing);
    dom.usertext.click(typing);
    dom.guess.click(getGuess);
    dom.guess.mouseenter(checkLength);
    dom.guess.mouseleave(hideCheckLength);
    typing();
}

function typing(){
    var sofar = dom.usertext.val().length;
    var remaining = constant.maxlen - sofar;
    dom.usertext.val(dom.usertext.val().substring(0, constant.maxlen));
    dom.remaining.html(remaining);
}

function getGuess(){
    fetch();
    if(data.usertext.length <= constant.maxlen){
        var method;
        if(data.usertext.length <= constant.GETmax){
            method = $.get;
        }
        else{
            method = $.post;
        }
        method("/getguess", {usertext: data.usertext})
            .done(function(result){
                console.log(result);
                data.guesstext = result.guess;
                update();
            });
    }
}

function fetch(){
    data.usertext = dom.usertext.val();
}

function checkLength(){
    var len = dom.usertext.val().length;
    if(len < constant.minlen){
        dom.warning.html("a longer comment is recommended");
    }
}

function hideCheckLength(){
    dom.warning.html("&nbsp;");
}



function update(){
    var result;
    if(data.guesstext.length){
        result = "r/" + data.guesstext;
    }
    else{
        result = "no idea... try a longer/less generic input";
    }
    dom.result.fadeToggle(200, function(){dom.result.html(result);});;
    dom.result.fadeToggle(200);
}
        

var constant = {
    GETmax: 1000,
    maxlen: 4000,
    minlen: 50
};

var data = {
    usertext: "",
    guesstext: "the guess"
};

var dom;
