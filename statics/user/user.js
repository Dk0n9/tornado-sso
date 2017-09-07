function checkSamePwd() {
    if ($('#pass_prefix').val() !== $('#confirm_pass_prefix').val()) {
        $('#confirm_pass_prefix').addClass('invalid');
        let labeObj = $('#confirm_pass_prefix').next();
        labeObj.attr('data-error', '两次输入密码不一致');
        labeObj.addClass('active');
    }
}

function checkNameExist() {
    let username = $('#name_prefix').val();
    if (username.length <= 0) {
        return true;
    }
    let _token = $('#registerForm').find('input[name=_xsrf]').val();
    $.ajax({
        url: '/check',
        type: 'post',
        data: {
            username: username,
            _xsrf: _token
        },
        success: function (response) {
            if (response.status) {
                return true;
            } else {
                $(this).attr('data-error', response.message);
                $(this).addClass('active');
            }
        }
    });
}

function checkMailExist() {
    let usermail = $('#email_prefix').val();
    if (usermail.length <= 0) {
        return true;
    }
    let _token = $('#registerForm').find('input[name=_xsrf]').val();
    $.ajax({
        url: '/check',
        type: 'post',
        data: {
            usermail: usermail,
            _xsrf: _token
        },
        success: function (response) {
            if (response.status) {
                return true;
            } else {
                $(this).attr('data-error', response.message);
                $(this).addClass('active');
            }
        }
    });
}

function login() {
    let usermail = $('#email_prefix').val();
    let password = $('#pass_prefix').val();
    let _token = $('input[name=_xsrf]').val();
    $.ajax({
        url: '/login' + location.search,
        type: 'post',
        data: {
            usermail: usermail,
            password: password,
            _xsrf: _token
        },
        success: function (response) {
            if (response.status) {
                Materialize.toast(response.message, 1700, '', function () {
                    window.location = response.result;
                });
            } else {
                Materialize.toast(response.message, 1500, 'error');
            }
        }
    })
}

function register() {
    let username = $('#name_prefix').val();
    let usermail = $('#email_prefix').val();
    let password = $('#pass_prefix').val();
    let confirm = $('#confirm_pass_prefix').val();
    let _token = $('#registerForm').find('input[name=_xsrf]').val();
    $.ajax({
        url: '/register',
        type: 'post',
        data: {
            v_username: username,
            v_usermail: usermail,
            v_password: password,
            v_confirm: confirm,
            _xsrf: _token
        },
        success: function (response) {
            if (response.status) {
                Materialize.toast('注册成功, 即将离开本页面...', 1700, '', function () {
                    window.location = response.result;
                });
            } else {
                Materialize.toast(response.message, 1500, 'error');
            }
        }
    })
}

$(document).ready(function () {
    let username = $('#username').text();
    if (username.length > 8) {
        $('#username').text(username.substring(0, 8) + '...');
    }

    $('#loginBtn').bind('click', login);
});
