function showMod(){
    document.getElementById("addModule").style.display = 'inline' ;
}

function hideAdd(){
    document.getElementById("addModule").style.display = 'none' ;
}

function manageClick(event){
    if (event.target.id == "addMod" || event.target.closest('#addModule')){
        return ;
    }
    return hideAdd() ;
}