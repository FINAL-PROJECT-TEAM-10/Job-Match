document.addEventListener('DOMContentLoaded', function () {
    let buttons = document.querySelectorAll('.button');

    buttons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            document.body.classList.add('loading');
            let loadingOverlay = document.createElement('div');
            loadingOverlay.classList.add('loading-overlay');
            let loader = document.createElement('div');
            loader.classList.add('loader');

            loadingOverlay.appendChild(loader);

            document.body.appendChild(loadingOverlay);

            setTimeout(function () {
                document.body.classList.remove('loading');
                loadingOverlay.remove();

                window.location.href = button.getAttribute('href');
            }, 1000);
        });
    });
});