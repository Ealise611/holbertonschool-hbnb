document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Page loaded:', window.location.pathname);

    // LOGIN FORM (login.html)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // INDEX PAGE (index.html)
    if (document.getElementById('places-list')) {
        initializePriceFilter();
        checkAuthentication();
    }

    // PLACE DETAILS PAGE (place.html)
    if (document.getElementById('place-details')) {
        const token = getCookie('token');
        const placeID = getPlaceIdFromURL();

        if (!placeID) {
            alert('No place id provided');
            return;
        }

        const ok = await fetchPlaceDetails(placeID);
        if (!ok) alert('Failed to load place details');

        addReviewButtonToPlacePage();
    }
});


// TASK 1 - login form
async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            showError('Login failed: Invalid credentials');
        }
    } catch (error) {
        showError('Error: Could not connect to server');
    }
}

// TASK 2 - index.html

function getCookie(name) {
    const cookies = document.cookie.split(';');
    let foundToken = null;

    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name && cookieValue) {
            foundToken = cookieValue;
        }
    }
    return foundToken;
}

function checkAuthentication() {
    if (!document.getElementById('places-list')) return;
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) {
        return;
    }

    if (!token) {
        loginLink.style.display = 'block';
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        fetchPlaces();
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token = null) {
    if (typeof fetch === 'undefined') {
        return showError('Browser not supported.');
    }

    console.log('Fetching places...');

    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        // Add authorization header if token exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://localhost:5000/api/v1/places/', {
            method: 'GET',
            headers: headers
        });

        if (!response) {
            return showError('No response from server.');
        }

        if (!response.ok) {
            const errorMessages = {
                401: 'Please log in to view places.',
                403: 'Access denied.',
                404: 'Places service unavailable.',
                500: 'Server error. Try again later.'
            };

            return showError(errorMessages[response.status] || `Error: ${response.status}`);
        }

        const places = await response.json();
        console.log('Success:', places);
        displayPlaces(places);

    } catch (error) {
        console.error('Error:', error);

        const errorMessage = error.message.includes('fetch')
            ? 'Cannot connect to server. Is the API running?'
            : 'Network error. Check your connection.';

        showError(errorMessage);
    }
}

function displayPlaces(places) {
    const placesContainer = document.getElementById('places-list');
    if (!placesContainer) {
        console.error('places-list container not found');
        return;
    }

    placesContainer.innerHTML = '';

    if (!places || places.length === 0) {
        placesContainer.innerHTML = '<p>No places available.</p>';
        return;
    }

    const row = document.createElement('div');
    row.className = 'row';

    places.forEach(place => {
        const column = document.createElement('div');
        column.className = 'column';

        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';

        placeCard.setAttribute('data-price', place.price || 0);

        placeCard.innerHTML = `
      <h3>${place.title || 'Unknown place'}</h3>
      <p>Price per night: $${place.price || 'N/A'}</p>
      <div class="button-container">
        <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
      </div>
    `;

        column.appendChild(placeCard);
        row.appendChild(column);
    });

    placesContainer.appendChild(row);

    const currentFilter = document.getElementById('price-filter').value;
    if (currentFilter !== 'all') {
        filterPlacesByPrice(currentFilter);
    }
}

function initializePriceFilter() {
    const filterSelect = document.getElementById('price-filter');
    if (!filterSelect) {
        return;
    }

    filterSelect.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        console.log('Filter changed to:', selectedPrice);
        filterPlacesByPrice(selectedPrice);
    });
}

function filterPlacesByPrice(maxPrice) {
    console.log('Filtering by max price:', maxPrice);

    const placeCards = document.querySelectorAll('.place-card');
    console.log('Found place cards:', placeCards.length);

    placeCards.forEach(card => {
        const placePrice = parseFloat(card.getAttribute('data-price')) || 0;
        console.log('Place price:', placePrice, 'Max price:', maxPrice);

        const column = card.parentElement;

        if (maxPrice === 'all' || placePrice <= parseFloat(maxPrice)) {
            column.style.display = 'flex';
        } else {
            column.style.display = 'none';
        }
    });
}

function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

function showError(message) {
    const existingError = document.getElementById('error-message');
    if (existingError) {
        existingError.remove();
    }

    const errorDiv = document.createElement('div');
    errorDiv.id = 'error-message';
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
    background-color: #f8d7da;
    color: #721c24;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    text-align: center;
    position: relative;
    z-index: 1000;
  `;
    errorDiv.textContent = message;

    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(errorDiv, main.firstChild);
    } else {
        document.body.insertBefore(errorDiv, document.body.firstChild);
    }

    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Task 3 - Place details

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

async function fetchPlaceDetails(placeID) {
    try {
        const res = await fetch(`http://localhost:5000/api/v1/places/${placeID}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!res.ok) {
            // if response is not 2xx, failed
            return false;
        }
        const place = await res.json();
        displayPlaceDetails(place);
        return true;
    } catch (err) {
        console.error('Error fetching place details:', err);
        return false;
    }
}
function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;

    container.innerHTML = `
    <h2>${place.title || 'No title'}</h2>
    <p>${place.description || 'No description'}</p>
    <p>Price per night: $${place.price || 'N/A'}</p>
    <h3>Amenities:</h3>
    <ul>
        ${(place.amenities || []).map(a => `<li>${a.name}</li>`).join('')}
    </ul >
    <h3>Reviews:</h3>
    <div>
    ${(place.reviews || []).map(r => `<p>${r.comment} - ${r.user?.name || 'Anonymous'}</p>`).join('')}
    </div>
`;
}

// Task 4

if (window.location.pathname.includes('add_review.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('📝 Add review page detected');

        const token = getCookie('token');
        if (!token) {
            alert('You must be logged in to add a review.');
            window.location.href = 'index.html';
            return;
        }

        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id');

        if (!placeId) {
            alert('No place_id in URL. Expected: add_review.html?place_id=SOME_ID');
            window.location.href = 'index.html';
            return;
        }

        console.log('✅ Place ID found:', placeId);

        // Setup review form
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                const reviewText = document.getElementById('review').value.trim();
                const rating = document.getElementById('rating').value;

                if (!reviewText || !rating) {
                    alert('Please fill in both review text and rating.');
                    return;
                }

                try {
                    console.log('📤 Submitting review...');

                    const response = await fetch('http://localhost:5000/api/v1/reviews/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            text: reviewText,
                            rating: parseInt(rating),
                            place_id: placeId
                        })
                    });

                    if (response.ok) {
                        alert('Review submitted successfully!');
                        reviewForm.reset();
                        window.location.href = `place.html?id=${placeId}`;
                    } else {
                        const errorText = await response.text();
                        console.log('Error:', errorText);
                        alert(`Failed to submit review: ${errorText}`);
                    }
                } catch (error) {
                    console.log('Network error:', error);
                    alert('Network error. Please try again.');
                }
            });
        }

        // Load place info
        fetch(`http://localhost:5000/api/v1/places/${placeId}`)
            .then(response => response.json())
            .then(place => {
                const form = document.querySelector('#review-form');
                if (form && place) {
                    const infoDiv = document.createElement('div');
                    infoDiv.innerHTML = `
                        <div style="background: #f0f8ff; padding: 15px; margin: 15px 0; border-radius: 10px; border: 1px solid #ccc;">
                            <h3>Reviewing: ${place.title}</h3>
                            <p>Host: ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
                            <p>Price: $${place.price}/night</p>
                        </div>
                    `;
                    form.parentNode.insertBefore(infoDiv, form);
                }
            })
            .catch(error => console.log('Could not load place info:', error));
    });
}

function addReviewButtonToPlacePage() {
    if (!window.location.pathname.includes('place.html')) return;

    const token = getCookie('token');
    if (!token) return;

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) return;

    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;

    // CHECK: Prevent duplicate buttons
    if (document.getElementById('review-button-container')) {
        console.log('⚠️ Review button already exists, skipping...');
        return;
    }

    // Create the button
    const reviewButton = document.createElement('div');
    reviewButton.id = 'review-button-container';
    reviewButton.innerHTML = `
        <div style="text-align: center; margin: 30px 0;">
            <button 
                onclick="goToAddReview('${placeId}')" 
                style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                    transition: all 0.3s ease;
                "
                onmouseover="this.style.background='linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)'; this.style.transform='translateY(-2px)'"
                onmouseout="this.style.background='linear-gradient(135deg, #667eea 0%, #764ba2 100%)'; this.style.transform='translateY(0px)'"
            >
                Write a Review
            </button>
        </div>
    `;

    placeDetailsSection.appendChild(reviewButton);
    console.log('✅ Review button added to place page');
}

function goToAddReview(placeId) {
    const token = getCookie('token');
    if (!token) {
        alert('Please log in to write a review.');
        window.location.href = 'login.html';
        return;
    }

    window.location.href = `add_review.html?place_id=${placeId}`;
}