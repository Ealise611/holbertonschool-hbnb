window.onload = function() {
    fetch('http://127.0.0.1:5000/api/v1/places')
.then(response => response.json())
.then(data => {
    console.log(data);
    displayPlaces(data);
})
}
function displayPlaces(places) {
    for (place of places) {
        console.log(place);

        document.getElementById('places-details').innerHTML += `
        <div class="place">
            <div>` + place.title + `</div>
            <div>` + `$`+ place.price + `</div>
            <div>` + place.description +`</div>
        </div>`
    }
}