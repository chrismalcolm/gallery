function renderDisplay(h_frame, metadata) {
    var text = `<div class="photo-display">`;
    for (id = 1; id <= metadata.length; id++) {
        text +=
        `<div class="photo-container">
            <a href="/photo/medium?id=${id}">
            <div>
                <img class="photo" src="/photo/small?id=${id}" align="middle" />
                <img class="frame" src="${h_frame}" />
            </div>
            </a>
            <div class="name">
                ${metadata[id-1].name}
            </div>
            <div class="description">
                ${metadata[id-1].description}
            </div>
        </div>`
    }
    text += `</div>`;
    document.write(text);
}
