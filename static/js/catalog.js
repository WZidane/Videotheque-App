const searchInput = document.getElementById('search-movie');
const searchFilter = document.getElementById('search-filter');
const searchButton = document.getElementById('search-button');
const resultsList = document.getElementById('results-list');

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function filterGenre() {
    const select = document.getElementById('genre-filter');
    const url = select.value;
    if (url) {
        window.location.href = url;
    }
}

function research() {
    const query = searchInput.value;
    const filter = searchFilter.value;

    if (query.trim() === '') {
        resultsList.innerHTML = '';
        return;
    }

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query, filter_type: filter })
    }) 
    .then(response => response.json())
    .then(data => {
        resultsList.innerHTML = '';
        if (data.error) {
            resultsList.innerHTML = `<li class="list-group-item text-danger">${data.error}</li>`;
        } else {
            const res = data.results.slice(0, 12);  // Récupère les 12 premiers éléments
            res.forEach(item => {
                let name = "";
                let poster = "";
                let id = item.id;  
                let route = `/movie/${id}`;

                if(item.title) {
                    name = item.title;
                } else if(item.name) {
                    name = item.name;
                }

                if(item.poster_path) {
                    poster = item.poster_path;
                } else if(item.profile_path) {
                    poster = item.profile_path;
                    route = `/person/${id}`;
                }

                if(poster && name && id) {
                    resultsList.innerHTML += `<div class="col-12 col-md-2">
                    <a href="${route}" style="text-decoration: none;">
                    <div class="card shadow-sm">
                      <img src="https://media.themoviedb.org/t/p/w220_and_h330_face/${poster}" class="card-img-top" alt="${name}">
                      <div class="card-body">
                        <h5 class="card-title">${name}</h5>
                      </div>
                    </div>
                    </a>
                  </div>`;
                }
            });
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        resultsList.innerHTML = '<p class="alert alert-danger">No result available.</p>';
    });
}

searchInput.addEventListener('input', () => {
    research();
});


document.addEventListener('DOMContentLoaded', function () {
    if(getQueryParam('input')) {
        research();
    }
});