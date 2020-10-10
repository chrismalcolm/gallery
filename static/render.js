function renderDisplay(h_frame) {
    var text = `<div class="photo-display">`;
    for (id = 1; id <= 9; id++) {
        text +=
        `<div class="photo-container">
            <a href="/photo/medium?id=${id}">
            <div>
                <img class="photo" src="/photo/small?id=${id}" align="middle" />
                <img class="frame" src="${h_frame}" />
            </div>
            </a>
            <div class="name">
                Picture ${id}
            </div>
            <div class="description">
                Hello, this is a short description of the image, quite nice eh?
            </div>
        </div>`
    }
    text += `</div>`;
    document.write(text);
}
