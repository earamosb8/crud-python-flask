const btnDelete =  document.querySelectorAll('.btn-delete');
if(btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) =>{
        btn.addEventListener('click', (e) => {
            if(!confirm('Estas seguro de querer eliminar este cliente?, al hacerlo borrara todos los pagos asociados a este también')) {
                e.preventDefault();
            }
        });
    });
}



