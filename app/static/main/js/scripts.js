// 加载图片并显示在对应的img元素中
function loadImage(event, previewId, textId1, textId2, buttonId) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        var img = document.getElementById(previewId);
        img.src = e.target.result;
        img.onload = function() {
            // 设置图片的宽度和高度以填充整个元素
            this.style.width = '100%';
            this.style.height = '100%';
            // 保持图片的纵横比
            this.style.objectFit = 'cover';
            // 显示图片，隐藏文字和按钮
            this.style.display = 'block';
            document.getElementById(textId1).style.display = 'none';
            document.getElementById(textId2).style.display = 'none';
            document.getElementById(buttonId).style.display = 'none';
        };
    };
    reader.readAsDataURL(file);
}

function loadDroidCamVideo(droidCamURL) {
    var video = document.getElementById('droidcam-video');
    var source = document.getElementById('droidcam-source');
    
    source.src = droidCamURL;  // 设置视频源URL
    video.load();  // 加载新的视频源
    video.play()  // 尝试播放视频
    .then(() => {
        console.log('视频播放成功');
    })
    .catch((error) => {
        console.error('播放视频时出错: ', error);
    });
}

// 当用户点击按钮后，加载 DroidCam 视频流并显示视频
document.getElementById('play-video').addEventListener('click', function() {
    console.log('按钮被点击');
    loadDroidCamVideo('http://10.90.15.88:4747/override');
    var video = document.getElementById('droidcam-video');
    video.style.display = 'block';
});



