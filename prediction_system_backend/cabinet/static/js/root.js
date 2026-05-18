function confirmLogout(event) {
    const confirmed = confirm('Вы уверены, что хотите выйти из аккаунта?');

    if (!confirmed) {
        event.preventDefault();
    }
}

function confirmDeletion(event) {
    const confirmed = confirm('Вы уверены, что хотите удалить медицинскую карту?');
    if (!confirmed) {
        event.preventDefault();
    }
}

