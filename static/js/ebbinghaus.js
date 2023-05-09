// 点击单词发音
let icons = document.querySelectorAll('.icon-fayin');
icons.forEach(function (icon) {
    icon.addEventListener('click', function () {
        let audio = icon.nextElementSibling;
        audio.play();
    })
})