/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
  });



// Star Rating Functionality
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    let currentRating = 0;

    stars.forEach(star => {
        // Add click event to each star
        star.addEventListener('click', function() {
            currentRating = parseInt(this.getAttribute('data-rating'));
            updateStarDisplay(currentRating);
            ratingInput.value = currentRating; // Set hidden input value
        });

        // Optional: Add hover effect
        star.addEventListener('mouseover', function() {
            const hoverRating = parseInt(this.getAttribute('data-rating'));
            updateStarDisplay(hoverRating);
        });
    });

    // Optional: Reset to current rating when mouse leaves star area
    document.querySelector('.star-rating').addEventListener('mouseleave', function() {
        updateStarDisplay(currentRating);
    });

    // Function to update star visual appearance
    function updateStarDisplay(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('selected'); // Highlight this star
            } else {
                star.classList.remove('selected'); // Remove highlight
            }
        });
    }
});