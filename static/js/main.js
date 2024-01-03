var homeSidebar = document.getElementById('home-sidebar')
var searchSidebar = document.getElementById('search-sidebar')
var addPlaylist = document.getElementById('add-playlist-sidebar')
var uploadMusic = document.getElementById('upload-music-sidebar')
var musicList = document.getElementById('music-list-sidebar')

const pageLoader = (page, target, className) => {
    var tempElement = document.createElement('div');
    tempElement.innerHTML = page.outerHTML;
    tempElement.querySelector(`.${className}`).style.display = '';  // Remove the "display: none" property

    target.innerHTML = tempElement.innerHTML;
}


const url = new URL(document.URL) 

if (url.hash.toLocaleLowerCase() == "#home" || url.hash.toLocaleLowerCase() == "") {

    var home = document.getElementById('card-home');
    var container = document.getElementById('container');

    pageLoader(home, container, 'home')
}

if (url.hash.toLocaleLowerCase() == "#search") {
    var home = document.getElementById('search-page');
    var container = document.getElementById('container');

    pageLoader(home, container, "search-page")
}

if (url.hash.toLocaleLowerCase() == "#music-list") {
    var home = document.getElementById('table-list-music');
    var container = document.getElementById('container');

    pageLoader(home, container, 'table-list-music')
}

if (url.hash.toLocaleLowerCase() == "#upload-music") {
    var home = document.getElementById('form-add-music');
    var container = document.getElementById('container');

    pageLoader(home, container, 'form-add-music')
}


homeSidebar.addEventListener('click', function () {
    var home = document.getElementById('card-home');
    var container = document.getElementById('container');

    pageLoader(home, container, 'home')
})

searchSidebar.addEventListener('click', function () {
    var home = document.getElementById('search-page');
    var container = document.getElementById('container');

    pageLoader(home, container, "search-page")
})

uploadMusic.addEventListener('click', function () {
    var home = document.getElementById('form-add-music');
    var container = document.getElementById('container');

    pageLoader(home, container, 'form-add-music')
})

musicList.addEventListener('click', function () {
    var home = document.getElementById('table-list-music');
    var container = document.getElementById('container');

    pageLoader(home, container, 'table-list-music')
})