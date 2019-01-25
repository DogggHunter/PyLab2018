function showError(container, errorMessage) {
    let msgElem = document.createElement('p');
    msgElem.className = "err_msg";
    msgElem.innerHTML = errorMessage;
    container.insertBefore(msgElem, container.firstChild);
}

function resetError() {
    let paras = document.getElementsByClassName('err_msg');

    while(paras[0]) {
        paras[0].parentNode.removeChild(paras[0]);
    }
}

function validate_form() {
    const elements = document.form_new_adt.elements;

    resetError();
    if (!elements.title.value) {
        showError(elements.title.parentNode, 'Отсутствует название');
        return false;
    }

    if (!elements.description.value) {
        showError(elements.description.parentNode, 'Отсутствует описание');
        return false;
    }
}