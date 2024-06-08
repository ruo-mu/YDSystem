// 页面加载时检查是否有access_token，如果没有则跳转到登录页面
window.onload = function() {
    const token = localStorage.getItem('access_token');
    if (token == null) {
        window.location.href = 'http://127.0.0.1:8080/';
    }
};

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

function uploadImage() {
    let inputs = document.querySelectorAll('input[type="file"]');
    let data = new FormData();
    inputs.forEach(input => {
      for (let i = 0; i < input.files.length; i++) {
        data.append('files', input.files[i]);
      }
    });
    // 发送请求到服务器
    fetch('http://127.0.0.1:8080/picture/upload_picture', {
        method: 'POST',
        body: data,
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        // 处理响应
        console.log(data);
    })
    .catch(error => {
        // 处理错误
        console.error(error);
    });
}
