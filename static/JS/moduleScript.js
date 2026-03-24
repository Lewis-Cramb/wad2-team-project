function showAdd(){
    document.getElementById("add").style.display = 'inline' ;
}

function showEdit(){
    document.getElementById("edit").style.display = 'inline' ;
}

function hideAdd(){
    document.getElementById("add").style.display = 'none' ;
}

function hideEdit(){
    document.getElementById("edit").style.display = 'none' ;
}

function registerEvent(event){
    // Ignore if clicking the edit button or inside the edit/add popups
    if (event.target.id == "editBttn" || event.target.closest('#edit') || event.target.closest('#add')) return; 

    if (event.target.id == "addBttn") {
        hideEdit();
        showAdd(); // Ensure add shows up when button is clicked
    } else {
        hideAll();
    }
}

function prepareEdit(id, rating, message) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-rating').value = rating;
    document.getElementById('edit-message').value = message;
    showEdit(); 
}

function hideAll(){
    hideEdit() ;
    hideAdd() ;
}