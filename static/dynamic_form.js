$(document).ready(function(){
    $("#add-algorithm").click(function(){
        var algorithm = $("#algorithm-dropdown").val();
        if (algorithm == 'SIATEC') {
            $("#algorithms").append(siatec_div)
        } else if (algorithm == 'time-warp invariant'){
            $("#algorithms").append(timewarp_div)
        }

        // To show the tooltips of info tags, the tooltips have to be registered again
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
        })

        $(".remove-button").click(function(){
            $(this).parent().remove();
        });
    });
});

var siatec_div = '\
<div name="siatec-parameters" class="mb-3 form-control">\
    <h4 class="mb-3">SIATEC\
    <i class="bi bi-info-circle text-secondary" data-bs-toggle="tooltip" data-bs-placement="right" title="SIATEC finds the maximal translatable pattern (MTP) for every possible translation vector of a piece."></i>\
    </h4>\
    <input type="hidden" name="algorithm_name" value="SIATEC">\
    <div class="mb-2">\
        <input type=number class="form-control" name="siatec-min-pattern-length" value=2 min=1>\
        <label for="siatec-min-pattern-length" class="form-label">Minimum pattern length \
        <i class="bi bi-info-circle text-secondary" data-bs-toggle="tooltip" data-bs-placement="right" title="Patterns with less notes than this number are discarded. Raising this number can lead to shorter computation times."></i>\
        </label>\
    </div>\
    <button class="remove-button btn btn-outline-danger mb-2">Remove</button>\
</div>'

var timewarp_div = '\
<div name="timewarp-parameters" class="mb-3 form-control">\
    <h4 class="mb-3">time-warp and transposition invariant algorithm\
    <i class="bi bi-info-circle text-secondary" data-bs-toggle="tooltip" data-bs-placement="right" title="An algorithm that tolerates distortion in the note onsets, meaning that different instances of a pattern can have differing rhythms."></i>\
    </h4>\
    <input type="hidden" name="algorithm_name" value="time-warp-invariant">\
    <div class="mb-2">\
        <input type=number class="form-control" name="timewarp-window" value=0 min=0>\
        <label for="timewarp-window" class="form-label">window \
        <i class="bi bi-info-circle text-secondary" data-bs-toggle="tooltip" data-bs-placement="right" title="The number of notes (that don\'t belong to the pattern) there can be in between consecutive notes of a pattern instance. Notes played at the same time are counted as \'one note\' by this parameter. Setting window to 0 means unrestricted mode, where there can be arbitrary many notes in between notes of a pattern."></i>\
        </label>\
    </div>\
    <button class="remove-button btn btn-outline-danger mb-3">Remove</button>\
</div>'