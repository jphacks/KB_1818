var container = document.getElementById('canvas-container');
var canvas = document.getElementById('picture');
var ctx = canvas.getContext('2d');
var isInit = false;
var img = new Image();
img.src = "C:/Users/ttpea/Documents/KB_1818/image.png";

//描画
var render = function(){
    var scale = 0;
    if(isInit){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }else{
        isInit = true;
    }
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight; 
    scale = canvas.width / img.width;
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
    ctx.drawImage(img, 0, 0);
}
//メイン
var main = function(){
    img.addEventListener('load', render, false);
    window.addEventListener('resize', render, false);
}
//メイン実行
main();