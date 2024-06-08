async function login(event) {
    // 阻止表单的默认提交行为
    event.preventDefault();

    // 获取用户输入的用户名和密码
    const username = document.getElementById('email').value;
    const password = document.getElementById('password').value;

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

    // 处理响应
    if (response.status === 200) {
        // 登录成功，获取令牌
        const token = await response.json();
        // 保存令牌到 localStorage
        localStorage.setItem('access_token', token['access_token']);
        // 重定向到首页
        window.location.href = 'http://127.0.0.1:8080/main';
    } else {
        // 显示错误信息
        document.getElementById('login-error').textContent = '无效的用户名或密码';
    }
}
