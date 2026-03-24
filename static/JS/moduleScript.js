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
    if (event.target.id == "addBttn" || event.target.closest('#add')) {
        return hideEdit() ;
    } else if (event.target.id == "editBttn" || event.target.closest('#edit')){
        return hideAdd() ;
    } else {
        return hideAll() ;
    }
}

function hideAll(){
    hideEdit() ;
    hideAdd() ;
}