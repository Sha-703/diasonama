document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.role-checkbox').forEach(function(cb){
    cb.addEventListener('change', function(e){
      const username = cb.dataset.username;
      const role = cb.value;
      const action = cb.checked ? 'add' : 'remove';
      if(!username) return;

      const data = new FormData();
      data.append('username', username.trim());
      data.append('role', role);
      data.append('action', action);

      fetch(new URL('ajax-toggle/', window.location.href).toString(), {
        method: 'POST',
        body: data,
        headers: {'X-Requested-With':'XMLHttpRequest'},
        credentials: 'same-origin'
      }).then(r => r.json()).then(json => {
        if(!json.ok){
          alert('Erreur lors de la mise à jour: ' + (json.error||''));
        }
      }).catch(err => { alert('Erreur réseau'); });
    });
  });
});
