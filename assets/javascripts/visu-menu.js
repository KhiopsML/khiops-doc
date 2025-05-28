function visuMenu(menu) {
    const menuContainer = document.getElementById('visu-menu');
    let isFirst = true;
    menu.map(item => {
        const button = document.createElement('buttton');
        const text = document.createTextNode(item.title);
        button.appendChild(text);
        button.setAttribute('title', item.description);
        button.dataset.file = item.file;
        button.classList.add('visu-menu-item','btn','btn-sm','btn-light','mb-2','me-2');
        button.addEventListener('click', (e) => loadData(item.file, e));
        if (isFirst) {
            isFirst = false;
            setTimeout(() => {
                button.click();
            },1000);
        }
        menuContainer.appendChild(button);
    });
}

function updateMenuActive(button) {
    let buttons = document.getElementsByClassName('visu-menu-item');

    Array.from(buttons).forEach(b => {
        b.classList.remove('btn-dark');
        b.classList.add('btn-light');
    });

    button.classList.remove('btn-light');
    button.classList.add('btn-dark');
}

async function loadData(file, e) {
    const visu = document.getElementById('visu-frame');
    
    fetch(file).then((response) => {
        response.json().then((data) => {
            if (visu && visu.contentWindow) {
                updateMenuActive(e.target);
                visu.contentWindow.postMessage(data);
            }
        })
    });
}
