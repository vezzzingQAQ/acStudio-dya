
function getClientHeight(){
    var clientHeight=0;
    if(document.body.clientHeight&&document.documentElement.clientHeight){
        var clientHeight = (document.body.clientHeight<document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
    }
    else{
        var clientHeight = (document.body.clientHeight>document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
    }
    return clientHeight;
}
function scrollAnimate(){
    //blockText
    var animateBlock1=document.querySelectorAll(".content_section .innerContent_div .innerComponent_div .textArea_div");
    for(var i=0;i<animateBlock1.length;i++){
        animateBlock1[i].style.marginTop="200px";
    }
    window.addEventListener("scroll",function(){
        var value=window.scrollY;
        for(var i=0;i<animateBlock1.length;i++){
            if(animateBlock1[i].offsetTop-getClientHeight()-animateBlock1[i].offsetLeft/9<=value){
                animateBlock1[i].style.marginTop="2px";
            }
        }
    })
    //background
    var mainBackground=document.querySelector(".content_section");
    window.addEventListener("scroll",function(){
        var value=window.scrollY;
        var currentValue=value-mainBackground.offsetTop;
        if(currentValue<=255*3){
            mainBackground.style.backgroundColor="rgb("+currentValue/3+","+currentValue/3+","+currentValue/3+")";
        }
    })
}
