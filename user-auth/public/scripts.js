const serverUrl = 'https://48da-42-110-166-131.ngrok-free.app';

// Function to validate email format
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Function to validate password format (at least 8 characters including lowercase, uppercase, numeric, and special characters)
function validatePassword(password) {
    const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;
    return regex.test(password);
}

// Function to generate random captcha
function generateCaptcha(formType) {
    const captcha = Math.floor(Math.random() * 9000) + 1000;
    document.getElementById(`${formType}-captcha`).textContent = captcha;
}

// Event listener for register form submission
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const captchaInput = document.getElementById('register-captcha-input').value;
    const captcha = document.getElementById('register-captcha').textContent;

    // Validations
    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (!validatePassword(password)) {
        alert('Password must contain at least 8 characters, including lowercase, uppercase, numeric, and special characters.');
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    if (captchaInput !== captcha) {
        alert('Captcha verification failed.');
        return;
    }

    try {
        const response = await fetch(`${serverUrl}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });

        if (response.status === 201) {
            alert('User registered successfully');
        } else {
            const errorData = await response.json();
            alert(`Registration failed: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration');
    }
});

// Event listener for login form submission
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const captchaInput = document.getElementById('login-captcha-input').value;
    const captcha = document.getElementById('login-captcha').textContent;

    // Validations
    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (captchaInput !== captcha) {
        alert('Captcha verification failed.');
        return;
    }

    try {
        const response = await fetch(`${serverUrl}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            alert('Login successful');
            localStorage.setItem('token', data.token);
        } else {
            const errorData = await response.json();
            alert(`Login failed: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login');
    }
});

// Event listener for refreshing captcha
document.querySelectorAll('.captcha button').forEach(button => {
    button.addEventListener('click', () => {
        const formType = button.parentElement.id.split('-')[0];
        generateCaptcha(formType);
    });
});

// Initial generation of captcha
generateCaptcha('register');
generateCaptcha('login');

const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
});
signupLink.onclick = (()=>{
  signupBtn.click();
  return false;
});
