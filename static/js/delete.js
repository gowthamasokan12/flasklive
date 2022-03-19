var response;
function deletefunc(name, url, swaltitle) {
    var checkboxid = [];
    $("input:checkbox[name=" + name + "]:checked").each(function () {
        checkboxid.push($(this).val());
    });
    if (checkboxid.length>0) {
        deleteswal(checkboxid, url, swaltitle)
    }
}

function deleteswal(msg, url, swaltitle) {
    swal({
        title: "Are you sure to remove this " + swaltitle + "?",
        type: "warning",

        showCancelButton: true,
        confirmButtonColor: "#004e92",
        confirmButtonText: "Yes, Remove !",
        closeOnConfirm: false
    },
        function () {
            
            console.log(msg, 'checkboxid');
            apimethod(msg, url)
            if (response['status'] == 'success')
            {
            swal({
                title: swaltitle + " Removed !",
                type: "success",

                showCancelButton: false,
                confirmButtonColor: "#004e92",
                confirmButtonText: "Ok",
                closeOnConfirm: false

            },
                function () {
                    location.reload()
                })
            }
            else{
                swal({
                    title: "Failed !",
                    type: "info",
    
                    showCancelButton: false,
                    confirmButtonColor: "#004e92",
                    confirmButtonText: "Ok",
                    closeOnConfirm: false
    
                })
            }
        })
}

function apimethod(msg, url) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response = xhttp.responseText;
            response = JSON.parse(this.response);
            console.log(response, "apimethod")
        }
    };
    xhttp.open("DELETE", url, false);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(msg);
}