async function getUsernameData() {
        const access_token = localStorage.getItem("access_token")
        fetch('http://127.0.0.1:8000/profile/info', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${access_token}`,
            },
        }).then(response => {
            if (response.ok) {
                return response.json()
            }
        }).
        then (data =>{
            const usernameHeader = document.getElementById('usernameHeader');
            usernameHeader.textContent = `Hello ${data.username}`;
        }).
        catch(error =>{
            console.error('Error', error)
        });
}
getUsernameData();