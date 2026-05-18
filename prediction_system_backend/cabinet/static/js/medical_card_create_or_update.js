document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('delete-medical-card-form');
    console.log(form)
    if (form) {
        form.addEventListener('submit', function(event) {
            const confirmed = confirm('Вы уверены, что хотите удалить медицинскую карту?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }
});