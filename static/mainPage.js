const rows = document.getElementsByTagName('tr');

for (let i = 0; i < rows.length; i++){
    rows[i].addEventListener('click', function(e){
        unClickRow();
        rows[i].style.backgroundColor = '#7fcdcd';
        removeClickedAtt();
        rows[i].setAttribute('isClicked', 'true')
    })
}

function unClickRow(){
    for (let i = 0; i < rows.length; i++){
        rows[i].style.backgroundColor = 'white';
    }
}

function removeClickedAtt(){
    for (let i = 0; i < rows.length; i++){
        rows[i].setAttribute('isClicked', 'false');
    }
}

