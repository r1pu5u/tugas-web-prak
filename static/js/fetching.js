const registerButton = document.getElementById('register-button')
const loginButton = document.getElementById('login-button')

if (loginButton != null) {
    
    loginButton.addEventListener('click', function (e) {
        e.preventDefault();
        const email = document.getElementById('email').value
        const password = document.getElementById('password').value;

        const url = '/login'; // Replace with your API endpoint

        const requestData = {
            email: email,
            password: password,
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any other headers if required
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            console.log('Status Code:', response.status); // Get the status code
            var dialog = document.getElementById('dialog')
            if (response.status == 401) {
                
                dialog.style.display = ''
                dialog.innerHTML = "Password atau username salah"
            } else if (response.status != 200) {
                
                dialog.style.display = ''
                dialog.innerHTML = "Terdapat Error Pada Server"
            }

            return response.json();
            
        })
        .then(result => {
            console.log(result)
        })
        .catch(error => console.log('error', error));
    })
}

if (registerButton != null) {
    registerButton.addEventListener('click', function () {
        const username = document.getElementById('username').value
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const phone_number = document.getElementById('phone_number').value;

        const url = '/signup'; // Replace with your API endpoint

        const requestData = {
            username: username,
            email: email,
            password: password,
            phone_number: phone_number
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any other headers if required
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            console.log('Status Code:', response.status); // Get the status code
            var dialog = document.getElementById('dialog')
            if (response.status == 409) {
                
                dialog.style.display = ''
                dialog.innerHTML = "User sudah ada"
            } else if (response.status != 201) {
                
                dialog.style.display = ''
                dialog.innerHTML = "Terdapat Error Pada Server"
            }

            return response.json();
            
        })
        .then(result => {
            console.log(result)
        })
        .catch(error => console.log('error', error));
        })
}