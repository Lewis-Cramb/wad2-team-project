function showEdit(){
    document.getElementById("edit-profile").style.display = 'flex' ;
}

function hideEdit(){
    document.getElementById("edit-profile").style.display = 'none' ;
}


function manageEvent(event){
    if (event.target.id=="editBttn" || event.target.closest('#edit-profile')){
        return ;
    }
    return hideEdit() ;
}