document.addEventListener('DOMContentLoaded', function() {
    getUsernameData();
});

async function getUsernameData() {
    const access_token = localStorage.getItem("access_token");

    if (!access_token) {
        
        const navList = document.querySelector('.navbar .nav-list');
        const loginListItem = document.createElement('li');
        const loginLink = document.createElement('a');
        loginLink.href = '/login';
        loginLink.textContent = 'Login';
        loginLink.classList.add('login-link');
        loginListItem.appendChild(loginLink);
        navList.appendChild(loginListItem);
        return;
    }

    fetch('http://127.0.0.1:8000/profile/info', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${access_token}`,
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        const usernameHeader = document.getElementById('usernameHeader');
        usernameHeader.textContent = `Your company: ${data.username}`;
    })
    .catch(error => {
        console.error('Error', error);
    });
}
