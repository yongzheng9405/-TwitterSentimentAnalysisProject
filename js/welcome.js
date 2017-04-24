// function search() {

// }

var suggestions = ["trumprussia", "brexit", "aprilfools", "georgiatech"];

// $('#sfield').autocomplete({
//     source: suggestions,
//     onSelect: function() {

//     }
// });

$(document).ready(
    function () {
        var suggestions = ["trumprussia", "brexit", "aprilfools", "georgiatech"];
        $("#sfield").autocomplete({
            source: suggestions,
            autoFocus: true,
        });
    }

);