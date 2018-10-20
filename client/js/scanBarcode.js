var takePicture = document.querySelector("#Take-Picture"),
showPicture = document.createElement("img");
Result = document.querySelector("#textbit");
var canvas =document.getElementById("picture");
var ctx = canvas.getContext("2d");
JOB.Init();
JOB.SetImageCallback(function(result) {
    if(result.length > 0){
        var tempArray = [];
        for(var i = 0; i < result.length; i++) {
            tempArray.push(result[i].Format+" : "+result[i].Value);
        }
        Result.innerHTML=tempArray.join("<br />");
    }else{
        if(result.length === 0) {
            Result.innerHTML="Decoding failed.";
        }
    }
    copyVideo();
});
JOB.PostOrientation = true;
JOB.OrientationCallback = function(result) {
    canvas.width = result.width;
    canvas.height = result.height;
    var data = ctx.getImageData(0,0,canvas.width,canvas.height);
    for(var i = 0; i < data.data.length; i++) {
        data.data[i] = result.data[i];
    }
    ctx.putImageData(data,0,0);
};
JOB.SwitchLocalizationFeedback(true);
JOB.SetLocalizationCallback(function(result) {
    ctx.beginPath();
    ctx.lineWIdth = "2";
    ctx.strokeStyle="red";
    for(var i = 0; i < result.length; i++) {
        ctx.rect(result[i].x,result[i].y,result[i].width,result[i].height); 
    }
    ctx.stroke();
});
if(takePicture && showPicture) {
    takePicture.onchange = function (event) {
        alert('aaa');
        var files = event.target.files;
        if (files && files.length > 0) {
            file = files[0];
            try {
                var URL = window.URL || window.webkitURL;
                showPicture.onload = function(event) {
                    Result.innerHTML="";
                    JOB.DecodeImage(showPicture);
                    URL.revokeObjectURL(showPicture.src);
                };
                showPicture.src = URL.createObjectURL(file);
            }
            catch (e) {
                try {
                    var fileReader = new FileReader();
                    fileReader.onload = function (event) {
                        showPicture.onload = function(event) {
                            Result.innerHTML="";
                            JOB.DecodeImage(showPicture);
                        };
                        showPicture.src = event.target.result;
                    };
                    fileReader.readAsDataURL(file);
                }
                catch (e) {
                    Result.innerHTML = "Neither createObjectURL or FileReader are supported";
                }
            }
        }
    };
}
var video = document.getElementById('video');
    var constraints = {
        audio: false,
        video: {
            // スマホのバックカメラを使用
            facingMode: 'environment'
        }
    };
    //  カメラの映像を取得
    navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
            video.srcObject = stream;
            setTimeout(copyVideo,1000);
        })
        .catch((err) => {
            window.alert(err.name + ': ' + err.message);
        });

function copyVideo(){
    var canvas = document.getElementById('canvas');
    //canvasの描画モードを2sに
    var ctx = canvas.getContext('2d');
    var img = document.getElementById('img2');

    //videoの縦幅横幅を取得
    var w = 400;//video.offsetWidth;
    var h = 225;//video.offsetHeight;

    //同じサイズをcanvasに指定
    canvas.setAttribute("width", w);
    canvas.setAttribute("height", h);

    //canvasにコピー
    ctx.drawImage(video, 0, 0, w, h);
    //imgにpng形式で書き出し
    img.src = canvas.toDataURL('image/png');

    // var canvas2 =document.getElementById("picture");
    // var ctx2 = canvas2.getContext("2d");
    // ctx2.drawImage(video, 0, 0, w, h);
    JOB.DecodeImage(img);

    // scan();
}

document.getElementById("overlay").style.display = "block";
function off() {
    document.getElementById("overlay").style.display = "none";
}