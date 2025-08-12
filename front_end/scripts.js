// TASK 2  - index.html

function getCookie(name) {
  // Function to get a cookie value by its name -- reads cookies for JWT token
  const cookies = `; ${document.cookie}`;
  const cookieName = cookies.split(`; ${name}=`);
  console.log(cookieName)
  if (cookieName.length === 2) {
    return cookieName.pop().split(';').shift();
  }
  return null; // if cookie not foudn
}

//testing whether cookies function works -- DELETE LATER
console.log('getCookie works');
console.log('Current token:', getCookie('token'));

function checkAuthentication() {
  // Checks if user is logged in and controls the login link visibility 
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!loginLink) {
    return;
  }
  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    // Fetch places data if the user is authenticated ??????????????
    fetchPlaces(token);
  }
}
