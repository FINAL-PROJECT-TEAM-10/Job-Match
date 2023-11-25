function attachLoadingOverlay(element) {
    element.addEventListener('click', function (event) {
        event.preventDefault();

        let loadingOverlay = document.createElement('div');
        loadingOverlay.classList.add('loading-overlay');
        let loader = document.createElement('div');
        loader.classList.add('loader');
        loadingOverlay.appendChild(loader);
        document.body.appendChild(loadingOverlay);

        setTimeout(function () {
            loadingOverlay.remove();
            window.location.href = '/';
        }, 1000);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    let logo = document.querySelector('.site-logo');
    attachLoadingOverlay(logo);
});