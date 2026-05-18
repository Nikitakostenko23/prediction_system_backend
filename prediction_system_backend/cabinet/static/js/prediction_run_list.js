document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('editModal')
    const input = document.getElementById('occlusionInput')
    const saveBtn = document.getElementById('saveBtn')
    const closeBtn = document.getElementById('closeBtn')
    let currentId = null;
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation()
            const row = e.target.closest('tr')
            const id = row.dataset.id
            if (!confirm('Удалить прогноз?')) return
            fetch(`/prediction_runs/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                }
            })
                .then(res => {
                    if (!res.ok) throw new Error('Ошибка удаления')
                    row.remove();
                })
                .catch(err => alert(err))
        })
    })
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation()
            const row = e.target.closest('tr')
            const id = row.dataset.id
            if (!confirm('Отменить прогноз?')) return
            fetch(`/prediction_runs/${id}/`, {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                }
            })
                .then(res => {
                    if (!res.ok) throw new Error('Ошибка отмены')
                    row.remove();
                })
                .catch(err => alert(err))
        })
    })

    function getCSRFToken() {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    }
});