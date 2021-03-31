$(document).ready(function(){
    $("#add-algorithm").click(function(){
        var algorithm = $("#algorithm-dropdown").val();
        if (algorithm == 'SIATEC') {
            $("#algorithms").append(siatec_div)
        } else if (algorithm == 'time-warp invariant'){
            $("#algorithms").append(timewarp_div)
        }

        $(".remove-button").click(function(){
            $(this).parent().remove();
        });
    });
});

var siatec_div = '\
<div name="siatec-parameters" class="mb-3 form-control">\
    <h4 class="mb-3">SIATEC</h4>\
    <input type="hidden" name="algorithm_name" value="SIATEC">\
    <div class="mb-2">\
        <input type=number class="form-control" name="siatec-min-pattern-length" value=2 min=2>\
        <label for="siatec-min-pattern-length" class="form-label">Minimum pattern length</label>\
    </div>\
    <button class="remove-button btn btn-outline-danger mb-2">Remove</button>\
</div>'

var timewarp_div = '\
<div name="timewarp-parameters" class="mb-3 form-control">\
    <h4 class="mb-3">time-warp and transposition invariant algorithm</h4>\
    <input type="hidden" name="algorithm_name" value="time-warp-invariant">\
    <div class="mb-2">\
        <input type=number class="form-control" name="timewarp-window" value=0 min=0>\
        <label for="timewarp-window" class="form-label">window</label>\
    </div>\
    <button class="remove-button btn btn-outline-danger mb-3">Remove</button>\
</div>'