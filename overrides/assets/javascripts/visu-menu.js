function visuMenu(menu) {
    const menuContainer = document.getElementById('visu-menu');
    let isFirst = true;
    menu.map(item => {
        const button = document.createElement('button');
        const text = document.createTextNode(item.title);
        button.appendChild(text);
        button.type = 'button';
        button.setAttribute('title', item.description);
        button.dataset.file = item.file;
        button.classList.add('visu-menu-item', 'md-button');
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
        b.classList.remove('is-active');
        b.classList.remove('md-button--primary');
    });

    button.classList.add('is-active');
    button.classList.add('md-button--primary');
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
