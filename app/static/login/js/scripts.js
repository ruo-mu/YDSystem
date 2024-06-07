async function login(event) {
    // 阻止表单的默认提交行为
    event.preventDefault();

    // 获取用户输入的用户名和密码
    const username = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // // 创建请求的数据
    // const data = {
    //     username: username,
    //     password: password
    // };
    //
    // // 发送POST请求到登录接口
    // const response = await fetch('http://127.0.0.1:8080/user/login', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify(data)
    // });
    const data = new URLSearchParams({
        username: username,
        password: password
    });

    const response = await fetch('http://127.0.0.1:8080/user/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: data
});

    // console.log(response);
    // 处理响应
if (response.status === 200) {
    // 登录成功，重定向到www.baidu.com
    // window.location.href = 'http://www.baidu.com';
    // 登录成功，获取令牌
    const token = await response.json();
    console.log(token);
    // 保存令牌到 localStorage 或其他地方
    localStorage.setItem('token', token);
    // 重定向到首页
    window.location.href = 'http://127.0.0.1:8080/main';
} else {
    // 显示错误信息
    document.getElementById('login-error').textContent = '无效的用户名或密码';
}

}
