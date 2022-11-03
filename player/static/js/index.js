var g = "campeonato123"
console.log(g.slice(-2))


var activeTableBtn = document.getElementById('tables');
// var inactiveTableBtn = document.getElementById('inactive-table')
// console.log(activeTableBtn)

activeTableBtn.addEventListener('click', tableClick);
// inactiveTableBtn.addEventListener('click', inactiveTableClick);


function tableClick(event) {

    if (event.target.classList.contains('deactivate-btn')) {
        console.log('Deactivate Pressed');
    }
    else if (event.target.classList.contains('unload-btn')) {
        console.log('Unload Pressed');
    }
    else if (event.target.classList.contains('activate-btn')) {
        console.log('Activate Pressed');
    }
    else return

    var action = event.target.className
    var send = JSON.stringify(action.slice(action.lastIndexOf(" ") + 1));
    console.log(send)

    $.ajax({
        url: "/update",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(send)
    });



}
