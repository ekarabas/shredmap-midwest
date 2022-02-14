// Find out whether or not a user is signed in
function user_signed_in() {
    if (document.querySelector('#logged_in')) {
        return true;
    } else {
        return false;
    }
}

// Return a list of resorts the user has visited
function user_visited() {

    if (user_signed_in()) {
        fetch('/user_visited')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                return data;
            })
    }
}


// Get access to green and grey map icons
// https://github.com/pointhi/leaflet-color-markers
var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var greyIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});


// Initialize the leaflet map, centered around the midwest
map_on_page = document.querySelector('#map');
if (map_on_page) {
    var map = L.map('map').setView([44.3, -90], 6);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        maxZoom: 18,
        id: 'mapbox/light-v10', //https://docs.mapbox.com/api/maps/styles/
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiZXptb25leWV2YW4iLCJhIjoiY2t6OHVvbXd4MW55NDJ3bmY0dGdoeXFiNCJ9.F9crG3FgELm-OPtdFWuVpA'
    }).addTo(map);
}

// If a user is signed in, display his or her visited resorts as a blue marker
if (user_signed_in()) {
    fetch('/user_visited')
        .then(response => response.json())
        .then(visited_data => {
            fetch('/all-resorts')
                .then(response => response.json())
                .then(resorts_data => {
                    for (let i = 0; i < resorts_data.length; i++) {

                        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf
                        if (visited_data.indexOf(resorts_data[i].id) > -1) {
                            L.marker([resorts_data[i].x, resorts_data[i].y], {
                                    riseOnHover: true,
                                    icon: greenIcon,
                                }).addTo(map)
                                .bindPopup(
                                    `<h5 class="fw-normal"><a href="/${resorts_data[i].id}">${resorts_data[i].name}</a></h5>
                            <h6 class="fw-light text-muted">${resorts_data[i].city}, ${resorts_data[i].state}</h6>`
                                );
                        } else {
                            L.marker([resorts_data[i].x, resorts_data[i].y], {
                                    riseOnHover: true,
                                    icon: greyIcon,
                                }).addTo(map)
                                .bindPopup(
                                    `<h5 class="fw-normal"><a href="/${resorts_data[i].id}">${resorts_data[i].name}</a></h5>
                            <h6 class="fw-light text-muted">${resorts_data[i].city}, ${resorts_data[i].state}</h6>`
                                );
                        }
                    }
                })
        })


}
// Otherwise, display all markers as grey
else {
    fetch('/all-resorts')
        .then(response => response.json())
        .then(resorts_data => {
            for (let i = 0; i < resorts_data.length; i++) {
                L.marker([resorts_data[i].x, resorts_data[i].y], {
                        riseOnHover: true,
                        icon: greyIcon,
                    }).addTo(map)
                    .bindPopup(
                        `<h5 class="fw-normal"><a href="/${resorts_data[i].id}">${resorts_data[i].name}</a></h5>
                    <h6 class="fw-light text-muted">${resorts_data[i].city}, ${resorts_data[i].state}</h6>`
                    );
            }
        })
}






// Resort review: allow categories to be toggled on and off 
function toggle_park() {
    park_slider = document.querySelector('#park_range');
    if (park_slider.disabled) {
        park_slider.disabled = false;
    } else {
        park_slider.disabled = true;
    }
}

function toggle_groomer() {
    groomer_slider = document.querySelector('#groomer_range');
    if (groomer_slider.disabled) {
        groomer_slider.disabled = false;
    } else {
        groomer_slider.disabled = true;
    }
}

function toggle_lift() {
    lift_slider = document.querySelector('#lift_range');
    if (lift_slider.disabled) {
        lift_slider.disabled = false
    } else {
        lift_slider.disabled = true;
    }
}

function toggle_vibe() {
    vibe_slider = document.querySelector('#vibe_range');
    if (vibe_slider.disabled) {
        vibe_slider.disabled = false;
    } else {
        vibe_slider.disabled = true;
    }
}