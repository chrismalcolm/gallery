function renderDisplay(h_frame, metadata) {
    var text = `<div class="photo-display">`;
    for (index = 0; index < metadata.length; index++) {
        var id = metadata[index].id
        text +=
        `<div class="photo-container">
            <a href="/photo/medium?id=${id}">
            <div>
                <img class="photo" src="/photo/small?id=${id}" align="middle" />
                <img class="frame" src="${h_frame}" />
            </div>
            </a>
            <div class="name">
                ${metadata[index].name}
            </div>
            <div class="description">
                ${metadata[index].description}
            </div>
        </div>`
    }
    text += `</div>`;
    document.write(text);
}
