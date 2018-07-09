(function initialize() {
    $("#id_content").on("keypress", function(e) {
        $(".invalid-feedback").hide();
        $(this).removeClass("is-invalid");
    });
})();
