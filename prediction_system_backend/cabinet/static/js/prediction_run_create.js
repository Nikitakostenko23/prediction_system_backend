// static/js/prediction_run_create.js

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const medicalCardId = urlParams.get('medical_card_id');
    if (medicalCardId) {
        const medicalCardSelect = document.querySelector('select[name="medical_card"]');

        if (medicalCardSelect) {
            const optionToSelect = Array.from(medicalCardSelect.options).find(option => option.value == medicalCardId);

            if (optionToSelect) {
                medicalCardSelect.value = medicalCardId;
                console.log(`Медкарта с ID ${medicalCardId} выбрана`);
            }
        }
    }
});
